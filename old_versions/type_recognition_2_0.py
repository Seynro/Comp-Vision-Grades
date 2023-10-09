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
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=40, param1=50, param2=32, minRadius=15, maxRadius=50)
        
        # Filter out small circles as outliers
        if circles is not None:
            circles = [circle for circle in circles[0] if circle[2] > np.median([c[2] for c in circles[0]]) - 5]
        
        return np.array([circles])

    def circle_mean_value(self, circle, image):
        x, y, r = circle
        circle_img = image[y-r:y+r, x-r:x+r]
        return np.mean(circle_img)

    def get_digit_from_circle(self, circle, image):
        x, y, r = circle
        offset = int(r * 0.5)
        digit_img = image[y-r-offset:y+r+offset, x-r-offset:x+r+offset]
        return cv2.cvtColor(digit_img, cv2.COLOR_BGR2GRAY)

    def recognize_digit_advanced(self, digit_image):
        contours, _ = cv2.findContours(digit_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        x, y, w, h = cv2.boundingRect(contours[0])
        if w > digit_image.shape[1] * 0.6:
            return 11
        else:
            return self.recognize_digit(digit_image)

    def recognize_digit(self, digit_image):
        contours, _ = cv2.findContours(digit_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        x, y, w, h = cv2.boundingRect(contours[0])
        aspect_ratio = w / h
        if aspect_ratio > 0.8:
            return 1
        elif aspect_ratio < 0.5:
            return 3
        return None

    def find_nearest_left_circle_advanced(self, circles, filled_circle):
        sorted_circles = sorted(circles, key=lambda c: c[1])
        y_diffs = [sorted_circles[i+1][1] - sorted_circles[i][1] for i in range(len(sorted_circles)-1)]
        max_diff_index = y_diffs.index(max(y_diffs))
        threshold_y = (sorted_circles[max_diff_index][1] + sorted_circles[max_diff_index + 1][1]) / 2
        filled_circle_row = "top" if filled_circle[1] < threshold_y else "bottom"
        if filled_circle_row == "top":
            filtered_circles = [circle for circle in circles if circle[1] < threshold_y]
        else:
            filtered_circles = [circle for circle in circles if circle[1] > threshold_y]
        left_circles = [circle for circle in filtered_circles if circle[0] < filled_circle[0]]
        if not left_circles:
            return None
        nearest_left_circle = min(left_circles, key=lambda c: filled_circle[0] - c[0])
        return nearest_left_circle

    def visualize_circles(self, image, circles, highlight_circle=None):
        output = image.copy()
        for circle in circles:
            x, y, r = circle
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            if np.array_equal(circle, highlight_circle):
                cv2.circle(output, (x, y), r, (0, 0, 255), 4)
        plt.figure(figsize=(10, 10))
        plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()

    def __call__(self):
        cropped_image = self.image[int(self.image.shape[0]*0.87):, :]
        detected_circles = self.detect_circles(cropped_image)
        gray_cropped = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        filled_circle = None
        min_mean_value = 255
        if detected_circles is not None:
            circles = np.round(detected_circles[0, :]).astype("int")
            for circle in circles:
                current_mean = self.circle_mean_value(circle, gray_cropped)
                if current_mean < min_mean_value:
                    min_mean_value = current_mean
                    filled_circle = circle
            
            # Visualizing the filled circle
            self.visualize_circles(cropped_image, circles, filled_circle)
            
        nearest_left_circle_advanced = self.find_nearest_left_circle_advanced(circles, filled_circle)
        
        # Visualizing the nearest left circle
        self.visualize_circles(cropped_image, circles, nearest_left_circle_advanced)
        
        nearest_digit_image_advanced = self.get_digit_from_circle(nearest_left_circle_advanced, cropped_image)
        nearest_digit_advanced_method = self.recognize_digit_advanced(nearest_digit_image_advanced)
        if nearest_digit_advanced_method is not None:
            student_selected_option_advanced_method = nearest_digit_advanced_method + 1
        else:
            student_selected_option_advanced_method = None
        return student_selected_option_advanced_method


# Test the TypeIdentifier class
image_path = r"C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\main_test\test_7.jpg"
type_identifier = TypeIdentifier(image_path)
selected_option = type_identifier()
print(f"The selected type by the student is: {selected_option}")
