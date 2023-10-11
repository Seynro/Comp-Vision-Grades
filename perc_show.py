from PIL import Image, ImageDraw, ImageFont

def put_percent(image_path, percentage):
    # Открыть изображение
    img = Image.open(image_path)

    # Добавление текста в центр картинки
    draw = ImageDraw.Draw(img)
    text = str(percentage)

    # Выбор шрифта и размера
    font_path = fr"font\DejaVuSans-Bold.ttf"
    font_size = min(img.size) // 22
    font = ImageFont.truetype(font_path, font_size)

    # Вычисление позиции текста в центре картинки
    text_width, text_height = draw.textsize(text, font=font)
    text_x = (img.width - text_width) / 2
    text_y = (img.height - text_height) / 2

    # Нанесение текста на картинку
    draw.text((text_x, text_y), text, font=font, fill="black")

    # Сохранение или показать результат
    img.save(image_path)
