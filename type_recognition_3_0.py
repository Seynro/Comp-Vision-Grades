import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

class TypeIdentifier:

    def __init__(self, image_path, reference_digits_dir="digits"):
        self.image_path = image_path
        self.image = cv2.imread(self.image_path)
        self.digit_images = self.load_reference_digits(reference_digits_dir)

    def load_reference_digits(self, dir_path):
        digit_images = {}
        for filename in os.listdir(dir_path):
            if filename.endswith(".png"):
                digit = int(filename.split("_")[1].split(".")[0])  # extracting the number from the filename
                image_path = os.path.join(dir_path, filename)
                digit_images[digit] = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        return digit_images

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

    def visualize_circles(self, image, circles, highlight_circle=None, mode=False, save_path="output.jpg"):
        output = image.copy()
        for circle in circles:
            x, y, r = circle
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            if np.array_equal(circle, highlight_circle):
                cv2.circle(output, (x, y), r, (0, 0, 255), 4)
        if mode:
            save_path = self.image_path.replace('.jpg', '_TYPE_RESULT.jpg')
            cv2.imwrite(save_path, output)
            plt.figure(figsize=(10, 10))
            plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
            plt.axis('off')
            plt.show()
        else:
            plt.figure(figsize=(10, 10))
            plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
            plt.axis('off')
            plt.show()

    def match_template(self, image, template):
        match_result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        _, match_value, _, _ = cv2.minMaxLoc(match_result)
        return match_value

    def recognize_digit_using_templates(self, digit_image):
        best_match_value = -1
        recognized_digit = None
        for digit, template in self.digit_images.items():
            current_match_value = self.match_template(digit_image, template)
            if current_match_value > best_match_value:
                best_match_value = current_match_value
                recognized_digit = digit
        return recognized_digit

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
            self.visualize_circles(cropped_image, circles, filled_circle, mode=True)
        try:
            nearest_left_circle_advanced = self.find_nearest_left_circle_advanced(circles, filled_circle)
            nearest_digit_image_advanced = self.get_digit_from_circle(nearest_left_circle_advanced, cropped_image)
            nearest_digit_advanced_method = self.recognize_digit_using_templates(nearest_digit_image_advanced)
            student_selected_option_advanced_method = nearest_digit_advanced_method + 1
        except TypeError:
            sorted_circles = sorted(circles, key=lambda c: c[1])
            y_diffs = [sorted_circles[i+1][1] - sorted_circles[i][1] for i in range(len(sorted_circles)-1)]
            max_diff_index = y_diffs.index(max(y_diffs))
            threshold_y = (sorted_circles[max_diff_index][1] + sorted_circles[max_diff_index + 1][1]) / 2
            if filled_circle[1] < threshold_y:
                student_selected_option_advanced_method = 1
            else:
                student_selected_option_advanced_method = 21
        return student_selected_option_advanced_method



# # Путь к изображению теста
# image_path = r"C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\main_test\test_7.jpg"

# # Создание экземпляра класса и запуск распознавания
# type_identifier = TypeIdentifier(image_path)
# selected_option = type_identifier()

# print(f"The selected type by the student is: {selected_option}")