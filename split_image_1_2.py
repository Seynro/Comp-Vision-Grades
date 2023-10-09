import cv2
import numpy as np
from matplotlib import pyplot as plt

class ImageSplitter:

    def __init__(self, image_path, save_path):
        self.image_path = image_path
        self.save_path = save_path
        self.image = cv2.imread(self.image_path)

    def split_image(self, top_split, bottom_split):
        """
        Splits the given image into three sections: 
        1. The top section
        2. The middle section between top and bottom splits
        3. The bottom section
        
        Args:
        - top_split: The percentage (0-1) to split from the top.
        - bottom_split: The percentage (0-1) to split from the bottom.
        """
        img_height = self.image.shape[0]
        top_split_point = int(img_height * top_split)
        bottom_split_point = int(img_height * (1 - bottom_split))
        
        top_section = self.image[:top_split_point, :]
        middle_section = self.image[top_split_point:bottom_split_point, :]
        bottom_section = self.image[bottom_split_point:, :]
        
        return top_section, middle_section, bottom_section

    def save_images(self, top_section, middle_section, bottom_section):
        top_save_path = f"{self.save_path}_top.jpg"
        middle_save_path = f"{self.save_path}_middle.jpg"
        bottom_save_path = f"{self.save_path}_bottom.jpg"
        
        cv2.imwrite(top_save_path, top_section)
        cv2.imwrite(middle_save_path, middle_section)
        cv2.imwrite(bottom_save_path, bottom_section)

    def combine_images(self, top_section, middle_section, bottom_section):
        combined_image = np.vstack([top_section, middle_section, bottom_section])
        return combined_image

    def display_images(self, top_section, middle_section, bottom_section, combined_image):
        fig, axs = plt.subplots(2, 2, figsize=(15, 10))
        
        # Displaying the top_section on the top-left
        axs[0, 0].imshow(cv2.cvtColor(top_section, cv2.COLOR_BGR2RGB))
        axs[0, 0].axis('off')
        axs[0, 0].set_title("Top Section")
        
        # Displaying the middle_section on the top-right
        axs[0, 1].imshow(cv2.cvtColor(middle_section, cv2.COLOR_BGR2RGB))
        axs[0, 1].axis('off')
        axs[0, 1].set_title("Middle Section")
        
        # Displaying the bottom_section on the bottom-left
        axs[1, 0].imshow(cv2.cvtColor(bottom_section, cv2.COLOR_BGR2RGB))
        axs[1, 0].axis('off')
        axs[1, 0].set_title("Bottom Section")
        
        # Displaying the combined_image on the bottom-right
        axs[1, 1].imshow(cv2.cvtColor(combined_image, cv2.COLOR_BGR2RGB))
        axs[1, 1].axis('off')
        axs[1, 1].set_title("Combined Image")
        
        plt.tight_layout()
        plt.show()

    def __call__(self, top_split=0.1, bottom_split=0.13):
        top_section, middle_section, bottom_section = self.split_image(top_split, bottom_split)
        self.save_images(top_section, middle_section, bottom_section)
        combined_image = self.combine_images(top_section, middle_section, bottom_section)
        self.display_images(top_section, middle_section, bottom_section, combined_image)
        self.save_images(top_section, middle_section, bottom_section)

# Usage:

# image_path = r"C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\main_test\test_2.jpg"
# save_path = r"C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\main_test\test_2"
# splitter = ImageSplitter(image_path, save_path)
# splitter()
