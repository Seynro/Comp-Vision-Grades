import cv2
import numpy as np
from matplotlib import pyplot as plt

def is_filled(c, thresh_img):
    mask = np.zeros(thresh_img.shape, dtype="uint8")
    cv2.drawContours(mask, [c], -1, 255, -1)
    mask = cv2.bitwise_and(thresh_img, thresh_img, mask=mask)
    total = cv2.countNonZero(mask)
    area = cv2.contourArea(c)
    if total / float(area) >= 0.5:   # percentage the circle is filled in
        return True
    return False

def get_bubble_size_threshold_v2(cnts):
    areas = [cv2.contourArea(c) for c in cnts]
    mean_area = np.mean(areas)
    std_dev_area = np.std(areas)
    lower_bound = mean_area - (0.8 * std_dev_area)
    upper_bound = mean_area + (0.8 * std_dev_area)
    return lower_bound, upper_bound

#---------------------------------------------------------------------------------

def score_test(bubble_cnts, thresh, answer_key, image):
    correct = 0
    for q, i in enumerate(range(0, len(bubble_cnts), 4)):
        cnts = sorted(bubble_cnts[i:i+4], key=lambda c: cv2.boundingRect(c)[0])
        
        # Ensure that there are exactly 4 contours in the group
        if len(cnts) != 4:
            continue

        filled = [is_filled(c, thresh) for c in cnts]
        if sum(filled) == 1:
            filled_index = filled.index(True)
            correct_index = answer_key[q]
            if filled_index == correct_index:
                correct += 1
                color = (0, 255, 0)  # Correct answer in green
                cv2.drawContours(image, [cnts[filled_index]], -1, color, 2)
            else:
                # Incorrect answer in red
                cv2.drawContours(image, [cnts[filled_index]], -1, (0, 0, 255), 2)
                # Check if the correct index exists in the cnts list
                if correct_index < len(cnts):
                    # Highlight the correct answer in orange
                    cv2.drawContours(image, [cnts[correct_index]], -1, (0, 165, 255), 2)
    return correct



# def score_test(bubble_cnts, thresh, answer_key, image):
#     correct = 0
#     for q, i in enumerate(range(0, len(bubble_cnts), 4)):
#         cnts = sorted(bubble_cnts[i:i+4], key=lambda c: cv2.boundingRect(c)[0])
#         filled = [is_filled(c, thresh) for c in cnts]
#         if sum(filled) == 1:
#             filled_index = filled.index(True)
#             if filled_index == answer_key[q]:
#                 correct += 1
#                 color = (0, 255, 0)  # Correct answer in green
#             else:
#                 color = (0, 0, 255)  # Incorrect answer in red
#             cv2.drawContours(image, [cnts[filled_index]], -1, color, 2)
#     return correct


#---------------------------------------------------------------------------------

image_path = r'C:\Users\user\Desktop\Programs\Python\test_grading_computer_vision\images_40_quest\5_ans.jpg'
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur and Otsu's thresholding
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# Find contours in the thresholded image
cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Dynamically determine bubble size
lower_bound, upper_bound = get_bubble_size_threshold_v2(cnts)

# Filter the contours based on dynamically calculated bubble size
bubble_cnts = [c for c in cnts if lower_bound <= cv2.contourArea(c) <= upper_bound]

# Sort bubbles first into two columns, then top-to-bottom within each column
bubble_cnts_left = sorted([c for c in bubble_cnts if cv2.boundingRect(c)[0] < image.shape[1] / 2], key=lambda c: cv2.boundingRect(c)[1])
bubble_cnts_right = sorted([c for c in bubble_cnts if cv2.boundingRect(c)[0] >= image.shape[1] / 2], key=lambda c: cv2.boundingRect(c)[1])
bubble_cnts = bubble_cnts_left + bubble_cnts_right

DEMO_ANSWER_KEY = {
 0: 1,  1: 1,  2: 1,  3: 1,  4: 2,
 5: 2,  6: 3,  7: 3,  8: 1,  9: 1,
10: 2, 11: 3, 12: 1, 13: 3, 14: 2,
15: 2, 16: 3, 17: 3, 18: 2, 19: 1,
20: 2, 21: 2, 22: 1, 23: 3, 24: 2,
25: 2, 26: 3, 27: 3, 28: 3, 29: 1,
30: 2, 31: 4, 32: 1, 33: 3, 34: 2,
35: 2, 36: 3, 37: 3, 38: 3, 39: 1
}

# Score the test and highlight the answers
correct = score_test(bubble_cnts, thresh, DEMO_ANSWER_KEY, image)
score = (correct / 40.0) * 100

# Save the processed image to a location accessible to the user
output_path = r'C:\Users\user\Desktop\Programs\Python\test_grading_computer_vision\images_40_quest\5_ans_RESULT.jpg'
cv2.imwrite(output_path, image)

# Display the processed image
plt.figure(figsize=(10, 10))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.title(f"Score: {score:.2f}%")
plt.show()
