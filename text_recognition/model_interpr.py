from PIL import Image
import numpy as np
import tensorflow as tf

# Загрузка изображения
image_path = r"C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\final_test\jpgs\test_1_top.jpg"
image = Image.open(image_path)

# Измените размер изображения
desired_height, desired_width = 32, 100
image = image.resize((desired_width, desired_height))

# Преобразование изображения в оттенки серого, если это необходимо
image = image.convert('L')  # 'L' mode for grayscale

# Преобразование изображения в numpy массив и нормализация
input_array = np.asarray(image) / 255.0

# Приведение к типу float32 и добавление размерности батча и канала
input_data = np.expand_dims(input_array, axis=(0, 1)).astype(np.float32)

# Использование модели
interpreter = tf.lite.Interpreter(model_path=r"C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\text_recognition\crnn_float16.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Запуск интерпретатора
interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()
output_data = interpreter.get_tensor(output_details[0]['index'])


# Предположительный алфавит
alphabet = ['-', ' '] + list('ABCDEFGHIJKLMNOPQRSTUVWXYZ') + list('abcdefghijklmnopqrstuvwxyz') + list('0123456789')

def decode_predictions(predictions, alphabet):
    text = ""
    for prediction in predictions:
        # выбор символа с наибольшим значением вероятности
        max_index = np.argmax(prediction)
        text += alphabet[max_index]
    return text

# Декодирование предсказанных данных
predicted_text = decode_predictions(output_data[0], alphabet)
print(predicted_text)
