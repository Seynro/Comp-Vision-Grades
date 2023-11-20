from PIL import Image, ImageDraw, ImageFont

def put_percent(image_path, percentage, type_num):
    # Открыть изображение
    img = Image.open(image_path)

    # Добавление текста в центр картинки
    draw = ImageDraw.Draw(img)
    text = f"{percentage}%, {type_num}"

    # Выбор шрифта и размера
    font_path = "font/DejaVuSans-Bold.ttf"  # Убедитесь, что путь к шрифту корректен
    font_size = min(img.size) // 22
    font = ImageFont.truetype(font_path, font_size)

    # Вычисление позиции текста в центре картинки
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
    text_x = (img.width - text_width) / 2
    text_y = (img.height - text_height) / 2

    # Нанесение текста на картинку
    draw.text((text_x, text_y), text, font=font, fill="black")

    # Сохранение или показать результат
    img.save(image_path)

# Пример использования
# put_percent("path_to_your_image.jpg", 50, "Type1")
