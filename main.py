# from scaling_image import SquareDetector, ImageSplitter
from Grading_2_1 import TestGrader
from type_recognition_3_0 import TypeIdentifier
from split_image_1_2 import ImageSplitter
import cv2
import numpy as np
from matplotlib import pyplot as plt
from perc_show import put_percent
# from converter import PDF_JPG_converter
from dig_rec import numbers_recognition

class Grading:

    def __init__(self,image_path: str, save_path: str, answer_key, n_questions):
        self.image_path = image_path
        self.save_path = save_path
        self.answer_key = answer_key
        self.n_questions = n_questions
    

    def combine_images(self, top_image, middle_image, bottom_image, save_result):
        """
        Combines three images (top, middle, and bottom) vertically and saves the result.

        Args:
        - top_image: The top image.
        - middle_image: The middle image.
        - bottom_image: The bottom image.
        - save_result: The path to save the combined image.
        """
        # Ensure all images have the same width
        width = max(top_image.shape[1], middle_image.shape[1], bottom_image.shape[1])
        top_image = cv2.resize(top_image, (width, top_image.shape[0]))
        middle_image = cv2.resize(middle_image, (width, middle_image.shape[0]))
        bottom_image = cv2.resize(bottom_image, (width, bottom_image.shape[0]))

        # Combine images vertically
        combined_image = np.vstack([top_image, middle_image, bottom_image])

        # Save the combined image
        cv2.imwrite(save_result, combined_image)

    def __call__(self):
        
        

        type_identifier = TypeIdentifier(self.image_path)
        selected_option = type_identifier()
        print(f"The selected type by the student is: {selected_option}")
        
        splitter = ImageSplitter(self.image_path, self.save_path)
        splitter()

        if self.image_path.endswith(".png"):
            image_path_ans = self.image_path.replace(".png", f"_middle.png")
            output_path = self.image_path.replace(".png", f"_RESULT.png")
        elif self.image_path.endswith(".jpg"):
            image_path_ans = self.image_path.replace(".jpg", f"_middle.jpg")
            output_path = self.image_path.replace(".jpg", f"_RESULT.jpg")

        answer_key = self.answer_key[selected_option]
        grader = TestGrader(image_path_ans, output_path, answer_key, self.n_questions)
        test_grader = grader()
        print(f'Scored Test: {test_grader}%')

        # Загрузим три изображения
        top_image = cv2.imread(self.image_path.replace(".jpg", "_top.jpg"))
        middle_image = cv2.imread(output_path)
        bottom_image = cv2.imread(self.image_path.replace(".jpg", "_TYPE_RESULT.jpg"))

        # Укажем путь для сохранения результата
        save_result = self.image_path.replace(".jpg", "_TOTAL_RESULT.jpg")

        # Вызовем функцию для объединения и сохранения
        self.combine_images(top_image, middle_image, bottom_image, save_result)

        st_id = numbers_recognition(top_image)

        result_dict = {selected_option: test_grader}

        put_percent(save_result, test_grader, selected_option)

        return result_dict

# answers = {1:
#             {0: 0,  1: 1,  2: 1,  3: 1,  4: 2,
#             5: 2,  6: 3,  7: 3,  8: 1,  9: 1,
#             10: 2, 11: 3, 12: 1, 13: 3, 14: 2,
#             15: 2, 16: 3, 17: 3, 18: 2, 19: 1,
#             20: 2, 21: 2, 22: 1, 23: 3, 24: 2,
#             25: 2, 26: 3, 27: 3, 28: 3, 29: 1,
#             30: 2, 31: 3, 32: 1, 33: 3, 34: 2,
#             35: 2, 36: 3, 37: 3, 38: 3, 39: 1},
            
#             29:{0: 1,  1: 1,  2: 1,  3: 1,  4: 2,
#             5: 2,  6: 3,  7: 3,  8: 1,  9: 1,
#             10: 2, 11: 3, 12: 1, 13: 3, 14: 2,
#             15: 2, 16: 3, 17: 3, 18: 2, 19: 1,
#             20: 2, 21: 2, 22: 1, 23: 3, 24: 2,
#             25: 2, 26: 3, 27: 3, 28: 3, 29: 1,
#             30: 2, 31: 3, 32: 1, 33: 3, 34: 2,
#             35: 2, 36: 3, 37: 3, 38: 3, 39: 1},

#             7:{0: 2,  1: 1,  2: 1,  3: 1,  4: 2,
#             5: 2,  6: 3,  7: 3,  8: 1,  9: 1,
#             10: 2, 11: 3, 12: 1, 13: 3, 14: 2,
#             15: 2, 16: 3, 17: 3, 18: 2, 19: 1,
#             20: 2, 21: 2, 22: 1, 23: 3, 24: 2,
#             25: 2, 26: 3, 27: 3, 28: 3, 29: 1,
#             30: 2, 31: 3, 32: 1, 33: 3, 34: 2,
#             35: 2, 36: 3, 37: 3, 38: 3, 39: 1},

#             40:{0: 3,  1: 1,  2: 1,  3: 1,  4: 2,
#             5: 2,  6: 3,  7: 3,  8: 1,  9: 1,
#             10: 2, 11: 3, 12: 1, 13: 3, 14: 2,
#             15: 2, 16: 3, 17: 3, 18: 2, 19: 1,
#             20: 2, 21: 2, 22: 1, 23: 3, 24: 2,
#             25: 2, 26: 3, 27: 3, 28: 3, 29: 1,
#             30: 2, 31: 3, 32: 1, 33: 3, 34: 2,
#             35: 2, 36: 3, 37: 3, 38: 3, 39: 1},

#             21:{0: 0,  1: 2,  2: 1,  3: 1,  4: 2,
#             5: 2,  6: 3,  7: 3,  8: 1,  9: 1,
#             10: 2, 11: 3, 12: 1, 13: 3, 14: 2,
#             15: 2, 16: 3, 17: 3, 18: 2, 19: 1,
#             20: 2, 21: 2, 22: 1, 23: 3, 24: 2,
#             25: 2, 26: 3, 27: 3, 28: 3, 29: 1,
#             30: 2, 31: 3, 32: 1, 33: 3, 34: 2,
#             35: 2, 36: 3, 37: 3, 38: 3, 39: 1}
#         }

# import pickle

# with open('dictionary', 'rb') as f:
#     answers = pickle.load(f)


# final_results = {}

# # PDF_JPG_converter(fr"C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\final_test\file (1).jpg")

# for i in range(1, 10):
#     image_path = fr"C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\final_test\file (1)_page-000{i}.jpg"
#     save_path = image_path.replace(".jpg","")
#     obj = Grading(image_path, save_path, answers)
#     final_results = final_results | obj()

# for i in range(10, 23):
#     image_path = fr"C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\final_test\file (1)_page-00{i}.jpg"
#     save_path = image_path.replace(".jpg","")
#     obj = Grading(image_path, save_path, answers)
#     final_results = final_results | obj()

# print(final_results)
