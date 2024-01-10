import cv2
import numpy as np
from matplotlib import pyplot as plt

class TestGrader:

    def __init__(self, image_path, output_path, answer_key, n_questions):
        self.answer_key = answer_key
        self.n_questions = n_questions
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
        fill_threshold = 0.5

        if total / float(area) >= fill_threshold:
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
        return circularity > 0.3

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

#TEST
#------------------------------------------------------------------------------------
 # Plotting each question's bubbles
            # question_img = self.image.copy()
            # for j, c in enumerate(cnts):
            #     color = (0, 255, 0) if filled[j] else (0, 0, 255)
            #     cv2.drawContours(question_img, [c], -1, color, 3)
            # plt.figure(figsize=(6, 6))
            # plt.imshow(cv2.cvtColor(question_img, cv2.COLOR_BGR2RGB))
            # plt.title(f"Question {q+1}")
            # plt.axis('off')
            # plt.show()
#------------------------------------------------------------------------------------

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
#TEST
#------------------------------------------------------------------------------------
        # plt.figure(figsize=(6, 6))
        # plt.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        # plt.title("Original Image")
        # plt.axis('off')
        # plt.show()
#------------------------------------------------------------------------------------
        blurred = cv2.GaussianBlur(self.gray, (5, 5), 0)

#TEST        
#------------------------------------------------------------------------------------
        # plt.figure(figsize=(6, 6))
        # plt.imshow(cv2.cvtColor(blurred, cv2.COLOR_GRAY2RGB))
        # plt.title("Blurred Image")
        # plt.axis('off')
        # plt.show()
#------------------------------------------------------------------------------------
        thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

#TEST
#------------------------------------------------------------------------------------
        # plt.figure(figsize=(6, 6))
        # plt.imshow(cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB))
        # plt.title("Thresholded Image")
        # plt.axis('off')
        # plt.show()
#------------------------------------------------------------------------------------
        cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#TEST
#------------------------------------------------------------------------------------
        # contour_img = self.image.copy()
        # cv2.drawContours(contour_img, cnts, -1, (0, 255, 0), 3)
        # plt.figure(figsize=(6, 6))
        # plt.imshow(cv2.cvtColor(contour_img, cv2.COLOR_BGR2RGB))
        # plt.title("Contours Detected")
        # plt.axis('off')
        # plt.show()
#------------------------------------------------------------------------------------

        bubble_cnts = [c for c in cnts if self.is_circle(c)]
#TEST
#------------------------------------------------------------------------------------
        # circle_img = self.image.copy()
        # cv2.drawContours(circle_img, bubble_cnts, -1, (255, 0, 0), 3)
        # plt.figure(figsize=(6, 6))
        # plt.imshow(cv2.cvtColor(circle_img, cv2.COLOR_BGR2RGB))
        # plt.title("Filtered by Circle")
        # plt.axis('off')
        # plt.show()
#------------------------------------------------------------------------------------
        bubble_cnts = self.filter_by_mean_size(bubble_cnts)
#TEST
#------------------------------------------------------------------------------------
        # size_img = self.image.copy()
        # cv2.drawContours(size_img, bubble_cnts, -1, (0, 0, 255), 3)
        # plt.figure(figsize=(6, 6))
        # plt.imshow(cv2.cvtColor(size_img, cv2.COLOR_BGR2RGB))
        # plt.title("Filtered by Mean Size")
        # plt.axis('off')
        # plt.show()
#------------------------------------------------------------------------------------

        sorted_bubble_cnts = self.sort_bubbles(bubble_cnts)
        correct = self.score_test(sorted_bubble_cnts, thresh, self.answer_key)
        score_percentage = (correct / self.n_questions) * 100

        # Save the processed image
        cv2.imwrite(self.output_path, self.image)

#TEST
#------------------------------------------------------------------------------------
        # Display the scored test
        # plt.figure(figsize=(10, 10))
        # plt.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        # plt.axis('off')
        # plt.title(f"Scored Test: {score_percentage:.2f}% Correct")
        # plt.show()
#------------------------------------------------------------------------------------
        return score_percentage

    def __call__(self):
        
        return self.grade_test()



# import pickle
# dict_ans = 'bs_stst_questions'
# image_path = r"C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\business_stat_test_2\file (10)_file (9)_merged_29_middle.jpg"
# output_path = r"C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\business_stat_test_2\file (10)_file (9)_merged_29_RESULT.jpg"
# with open(dict_ans, 'rb') as f:
#     answers = pickle.load(f)

# # Usage:
# grader = TestGrader(image_path, output_path, answers[16], 40)
# grader()
