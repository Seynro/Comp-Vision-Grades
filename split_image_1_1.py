import cv2
import numpy as np
from matplotlib import pyplot as plt

class ImageSplitter:

    def __init__(self, image_path, save_path):
        self.image_path = image_path
        self.save_path = save_path
        self.image = cv2.imread(self.image_path)

    def split_image(self, split_at):
        """
        Splits the given image into two sections: the info_section (top) 
        and the ans_section (bottom) based on the provided split point.
        """
        info_section = self.image[:split_at, :]
        ans_section = self.image[split_at:, :]
        return info_section, ans_section

    def save_images(self, info_section, ans_section):
        info_save_path = f"{self.save_path}_info.jpg"
        ans_save_path = f"{self.save_path}_ans.jpg"
        
        cv2.imwrite(info_save_path, info_section)
        cv2.imwrite(ans_save_path, ans_section)

    def display_images(self, info_section, ans_section):
        fig, axs = plt.subplots(1, 2, figsize=(15, 10))
        
        # Displaying the info_section on the left
        axs[0].imshow(cv2.cvtColor(info_section, cv2.COLOR_BGR2RGB))
        axs[0].axis('off')
        axs[0].set_title("Info Section")
        
        # Displaying the ans_section on the right
        axs[1].imshow(cv2.cvtColor(ans_section, cv2.COLOR_BGR2RGB))
        axs[1].axis('off')
        axs[1].set_title("Ans Section")
        
        plt.tight_layout()
        plt.show()

    def __call__(self):
        split_point = int(self.image.shape[0] * 0.11)  # Roughly 11% from the top
        info_section, ans_section = self.split_image(split_point)
        self.save_images(info_section, ans_section)
        self.display_images(info_section, ans_section)

# Usage:

# image_path = r"C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\images_name_surname\scan_2.jpg"
# save_path = r"C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\images_name_surname\scan_2"
# splitter = ImageSplitter(image_path, save_path)
# splitter()
