import cv2
import numpy as np
from matplotlib import pyplot as plt

class TestGrader:

    def __init__(self, image_path, output_path, answer_key):
        self.answer_key = answer_key
        self.image_path = image_path
        self.output_path = output_path
        self.image = cv2.imread(self.image_path)
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def is_filled(self, c, thresh_img):
        mask = np.zeros(thresh_img.shape, dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)
        mask = cv2.bitwise_and(thresh_img, thresh_img, mask=mask)
        total = cv2.countNonZero(mask)
        area = cv2.contourArea(c)
        if total / float(area) >= 0.35:
            return True
        return False

    def filter_by_mean_size(self, cnts, deviation_factor=0.5):
        areas = [cv2.contourArea(c) for c in cnts]
        mean_area = np.mean(areas)
        lower_threshold = mean_area * (1 - deviation_factor)
        upper_threshold = mean_area * (1 + deviation_factor)
        return [c for c in cnts if lower_threshold < cv2.contourArea(c) < upper_threshold]

    def is_circle(self, c):
        perimeter = cv2.arcLength(c, True)
        area = cv2.contourArea(c)
        if perimeter == 0:
            return False
        circularity = 4 * np.pi * (area / (perimeter * perimeter))
        return circularity > 0.7

    def sort_bubbles(self, bubble_cnts):
        bubble_cnts_left = sorted([c for c in bubble_cnts if cv2.boundingRect(c)[0] < self.image.shape[1] / 2], key=lambda c: cv2.boundingRect(c)[1])
        bubble_cnts_right = sorted([c for c in bubble_cnts if cv2.boundingRect(c)[0] >= self.image.shape[1] / 2], key=lambda c: cv2.boundingRect(c)[1])
        return bubble_cnts_left + bubble_cnts_right

    def score_test(self, bubble_cnts, thresh, answer_key):
        correct = 0
        for q, i in enumerate(range(0, len(bubble_cnts), 4)):
            cnts = sorted(bubble_cnts[i:i+4], key=lambda c: cv2.boundingRect(c)[0])
            if len(cnts) != 4:
                continue
            filled = [self.is_filled(c, thresh) for c in cnts]
            if sum(filled) == 1:
                filled_index = filled.index(True)
                correct_index = answer_key[q]
                if filled_index == correct_index:
                    correct += 1
                    color = (0, 255, 0)
                    cv2.drawContours(self.image, [cnts[filled_index]], -1, color, 2)
                else:
                    cv2.drawContours(self.image, [cnts[filled_index]], -1, (0, 0, 255), 2)
                    if correct_index < len(cnts):
                        cv2.drawContours(self.image, [cnts[correct_index]], -1, (0, 165, 255), 2)
        return correct

    def grade_test(self):
        blurred = cv2.GaussianBlur(self.gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        bubble_cnts = [c for c in cnts if self.is_circle(c)]
        bubble_cnts = self.filter_by_mean_size(bubble_cnts)


        sorted_bubble_cnts = self.sort_bubbles(bubble_cnts)
        correct = self.score_test(sorted_bubble_cnts, thresh, self.answer_key)
        score_percentage = (correct / 40.0) * 100

        # Save the processed image
        cv2.imwrite(self.output_path, self.image)

        # Display the scored test
        plt.figure(figsize=(10, 10))
        plt.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title(f"Scored Test: {score_percentage:.2f}% Correct")
        plt.show()

        return score_percentage

    def __call__(self):
        
        return self.grade_test()


# image_path = r"C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\images_name_surname\scan_2.jpg"
# output_path = r"C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\images_name_surname\scan_2_RESULT_test.png"
# # Usage:
# grader = TestGrader(image_path, output_path)
# grader()
