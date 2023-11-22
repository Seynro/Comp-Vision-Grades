import tensorflow as tf
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

a = tf.__version__


model = ocr_predictor(pretrained=True)

def numbers_recognition(image_path):
    # Load the document
    # print(image_path)
    doc = DocumentFile.from_images(image_path)
    # Analyze
    result = model(doc)

    # result.show(doc)
    
    json_output = result.export()

    words_after_st = []
    st_found = False

    for page in json_output['pages']:
        for block in page['blocks']:
            for line in block['lines']:
                for word in line['words']:
                    if st_found:
                        words_after_st.append(word['value'])
                    if 'St' in word['value'] and not st_found:
                        st_found = True

    # Объединяем слова в одну строку
    result_string = ' '.join(words_after_st)
    
    # Возвращаем последние 5 символов, если строка больше 5 символов
    if len(result_string) > 5:
        try:
            return int(result_string[-5:])
        except:
            print('Int error')
            return str(result_string[-5:])
    else:
        return result_string

# print(numbers_recognition(r'C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\final_test\file (1)_page-0001_top.jpg'))

def number_after_type(image_path):
    # Load the document
    # print(image_path)
    doc = DocumentFile.from_images(image_path)
    # Analyze
    result = model(doc)
    # result.show(doc)
    json_output = result.export()

    type_found = False
    number_after_type = None

    for page in json_output['pages']:
        for block in page['blocks']:
            for line in block['lines']:
                for word in line['words']:
                    if type_found:
                        # Проверяем, является ли следующее слово числом
                        if word['value'].isdigit():
                            number_after_type = word['value']
                            break
                    if 'Type:' in word['value']:
                        type_found = True
                if number_after_type is not None:
                    break
            if number_after_type is not None:
                break
        if number_after_type is not None:
            break
    try:
        return int(number_after_type)
    except:
        print('Int error')
        return str(number_after_type)

# Пример использования
# print(number_after_type(r"C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\new_test\file (8)_page-0005_top.jpg"))