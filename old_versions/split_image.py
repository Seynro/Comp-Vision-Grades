import cv2
import numpy as np
from matplotlib import pyplot as plt

def split_image(image, split_at):
    """
    Splits the given image into two sections: the name_section (top) 
    and the questions_section (bottom) based on the provided split point.
    """
    name_section = image[:split_at, :]
    questions_section = image[split_at:, :]
    
    return name_section, questions_section

# Load the image
image_path = r'C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\images_name_surname\photo_test_1.jpg'
full_image = cv2.imread(image_path)

# Define the split point based on our discussions
split_point = int(full_image.shape[0] * 0.12)  # Roughly 12% from the top

# Split the image into two sections: name_section and questions_section
name_section, questions_section = split_image(full_image, split_point)

# Display the two sections for verification
fig, axs = plt.subplots(1, 2, figsize=(15, 10))

# Displaying the name_section on the left
axs[0].imshow(cv2.cvtColor(name_section, cv2.COLOR_BGR2RGB))
axs[0].axis('off')
axs[0].set_title("Name Section")

# Displaying the questions_section on the right
axs[1].imshow(cv2.cvtColor(questions_section, cv2.COLOR_BGR2RGB))
axs[1].axis('off')
axs[1].set_title("Questions Section")

plt.tight_layout()
plt.show()
