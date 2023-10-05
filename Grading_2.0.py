image_path = r'C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\images_name_surname\photo_test_crop_full_2.jpg'
output_path = r'C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\images_name_surname\photo_test_crop_full_2_RESULT.jpg'

import cv2
import numpy as np
from matplotlib import pyplot as plt

def is_filled(c, thresh_img):
    mask = np.zeros(thresh_img.shape, dtype="uint8")
    cv2.drawContours(mask, [c], -1, 255, -1)
    mask = cv2.bitwise_and(thresh_img, thresh_img, mask=mask)
    total = cv2.countNonZero(mask)
    area = cv2.contourArea(c)
    if total / float(area) >= 0.5:
        return True
    return False

def filter_by_mean_size(cnts, deviation_factor=0.5):
    areas = [cv2.contourArea(c) for c in cnts]
    mean_area = np.mean(areas)
    lower_threshold = mean_area * (1 - deviation_factor)
    upper_threshold = mean_area * (1 + deviation_factor)
    return [c for c in cnts if lower_threshold < cv2.contourArea(c) < upper_threshold]

def is_circle(c):
    perimeter = cv2.arcLength(c, True)
    area = cv2.contourArea(c)
    if perimeter == 0:
        return False
    circularity = 4 * np.pi * (area / (perimeter * perimeter))
    return circularity > 0.7

def sort_bubbles(bubble_cnts, image):
    bubble_cnts_left = sorted([c for c in bubble_cnts if cv2.boundingRect(c)[0] < image.shape[1] / 2], key=lambda c: cv2.boundingRect(c)[1])
    bubble_cnts_right = sorted([c for c in bubble_cnts if cv2.boundingRect(c)[0] >= image.shape[1] / 2], key=lambda c: cv2.boundingRect(c)[1])
    return bubble_cnts_left + bubble_cnts_right

def score_test(bubble_cnts, thresh, answer_key, image):
    correct = 0
    for q, i in enumerate(range(0, len(bubble_cnts), 4)):
        cnts = sorted(bubble_cnts[i:i+4], key=lambda c: cv2.boundingRect(c)[0])
        if len(cnts) != 4:
            continue
        filled = [is_filled(c, thresh) for c in cnts]
        if sum(filled) == 1:
            filled_index = filled.index(True)
            correct_index = answer_key[q]
            if filled_index == correct_index:
                correct += 1
                color = (0, 255, 0)
                cv2.drawContours(image, [cnts[filled_index]], -1, color, 2)
            else:
                cv2.drawContours(image, [cnts[filled_index]], -1, (0, 0, 255), 2)
                if correct_index < len(cnts):
                    cv2.drawContours(image, [cnts[correct_index]], -1, (0, 165, 255), 2)
    return correct

# Load the image

image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
bubble_cnts = [c for c in cnts if is_circle(c)]
bubble_cnts = filter_by_mean_size(bubble_cnts)

DEMO_ANSWER_KEY = {
    0: 1,  1: 1,  2: 1,  3: 1,  4: 2,
    5: 2,  6: 3,  7: 3,  8: 1,  9: 1,
    10: 2, 11: 3, 12: 1, 13: 3, 14: 2,
    15: 2, 16: 3, 17: 3, 18: 2, 19: 1,
    20: 2, 21: 2, 22: 1, 23: 3, 24: 2,
    25: 2, 26: 3, 27: 3, 28: 3, 29: 1,
    30: 2, 31: 3, 32: 1, 33: 3, 34: 2,
    35: 2, 36: 3, 37: 3, 38: 3, 39: 1
}

sorted_bubble_cnts = sort_bubbles(bubble_cnts, image)
correct = score_test(sorted_bubble_cnts, thresh, DEMO_ANSWER_KEY, image)
score_percentage = (correct / 40.0) * 100

# Display the scored test
plt.figure(figsize=(10, 10))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.title(f"Scored Test: {score_percentage:.2f}% Correct")
plt.show()
