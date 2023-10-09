import cv2
import numpy as np
import matplotlib.pyplot as plt

class ImageAligner:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(self.image_path)
    
    def find_lines(self, image):
        """
        Находит линии на изображении с помощью преобразования Хафа.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)

        return lines

    def plot_lines(self, lines):
        """
        Визуализирует найденные линии с использованием Matplotlib.
        """
        if lines is None or len(lines) < 2:
            print("Не удалось найти достаточно линий на изображении для выравнивания.")
            return

        # Создаем новое изображение для визуализации линий
        vis_image = self.image.copy()
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(vis_image, (x1, y1), (x2, y2), (0, 0, 255), 2)

        # Отображаем изображение с линиями с использованием Matplotlib
        plt.figure(figsize=(10, 10))
        plt.imshow(cv2.cvtColor(vis_image, cv2.COLOR_BGR2RGB))
        plt.title("Найденные линии")
        plt.axis('off')
        plt.show()

    def align_image(self):
        lines = self.find_lines(self.image)
        
        if lines is None or len(lines) < 2:
            print("Не удалось найти достаточно линий на изображении для выравнивания.")
            return None
        
        # Сортируем линии по угловому коэффициенту (наклону)
        lines = sorted(lines, key=lambda x: x[0][1])
        
        # Вычисляем угол наклона средних двух линий
        angle_radians = (lines[0][0][1] + lines[1][0][1]) / 2.0
        
        # Выполняем поворот изображения
        height, width = self.image.shape[:2]
        rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), np.degrees(angle_radians), 1)
        aligned_image = cv2.warpAffine(self.image, rotation_matrix, (width, height), flags=cv2.INTER_LINEAR)
        
        return aligned_image

    def save_aligned_image(self, save_path):
        aligned_image = self.align_image()
        if aligned_image is not None:
            cv2.imwrite(save_path, aligned_image)
            print(f"Изображение выровнено и сохранено по пути: {save_path}")

    def align_and_plot(self):
        lines = self.find_lines(self.image)
        self.plot_lines(lines)
        self.save_aligned_image("aligned_image.jpg")

# Пример использования:
# image_path = "path_to_your_image.jpg"
# aligner = ImageAligner(image_path)
# aligner.align_and_plot()


# Пример использования:
image_path = r"C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\main_test\test_5.jpg"
save_path = r"C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\main_test\test_5_scaled.jpg"
aligner = ImageAligner(image_path)
aligner.save_aligned_image(save_path)


