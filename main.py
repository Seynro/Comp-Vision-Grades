# from scaling_image import SquareDetector, ImageSplitter
from Grading_2_1 import TestGrader
from type_recognition_3_0 import TypeIdentifier
from split_image_1_2 import ImageSplitter
import cv2
import numpy as np
from matplotlib import pyplot as plt


class Grading:

    def __init__(self,image_path: str, save_path: str):
        self.image_path = image_path
        self.save_path = save_path
    

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
        
        type_identifier = TypeIdentifier(image_path)
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

        grader = TestGrader(image_path_ans, output_path)
        grader()

        # Загрузим три изображения
        top_image = cv2.imread(self.image_path.replace(".jpg", "_top.jpg"))
        middle_image = cv2.imread(output_path)
        bottom_image = cv2.imread(self.image_path.replace(".jpg", "_TYPE_RESULT.jpg"))

        # Укажем путь для сохранения результата
        save_result = self.image_path.replace(".jpg", "_TOTAL_RESULT.jpg")

        # Вызовем функцию для объединения и сохранения
        self.combine_images(top_image, middle_image, bottom_image, save_result)


image_path = r"C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\main_test\test_9.jpg"
save_path = r"C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\main_test\test_9"

obj = Grading(image_path, save_path)
obj()