import cv2
import numpy as np
from matplotlib import pyplot as plt

class TypeIdentifier:

    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(self.image_path)

    def detect_circles(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Detect circles using HoughCircles method
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=40, param1=50, param2=32, minRadius=15, maxRadius=50)
        
        return circles

    def circle_mean_value(self, circle, image):
        x, y, r = circle
        circle_img = image[y-r:y+r, x-r:x+r]
        return np.mean(circle_img)

    def identify_filled_circle(self, circles, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            filled_index = None
            min_mean_value = 255  # max possible value for a grayscale image
            for idx, circle in enumerate(circles):
                current_mean = self.circle_mean_value(circle, gray)
                if current_mean < min_mean_value:
                    min_mean_value = current_mean
                    filled_index = idx
            for idx, (x, y, r) in enumerate(circles):
                if idx == filled_index:
                    cv2.circle(image, (x, y), r, (0, 0, 255), 4)
                else:
                    cv2.circle(image, (x, y), r, (0, 255, 0), 4)
            print(f"The selected type index is: {filled_index + 1}")
        else:
            print("No circles detected.")

        # Save the image with highlighted circles
        cv2.imwrite(self.image_path.replace(".jpg", "_TYPE_RESULT.jpg"), image)

    def __call__(self):
        cropped_image = self.image[int(self.image.shape[0]*0.9):, :]
        detected_circles = self.detect_circles(cropped_image)
        self.identify_filled_circle(detected_circles, cropped_image)
        
        # Visualization
        plt.figure(figsize=(10, 10))
        plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
        plt.title(f"Detected Circles")
        plt.axis('off')
        plt.show()

# Test the TypeIdentifier class on the provided image
image_path = r"C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\main_test\test_6_2.jpg"
type_identifier = TypeIdentifier(image_path)
type_identifier()