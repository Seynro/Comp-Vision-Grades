from docx import Document
from docx.oxml.ns import qn

file_path = r"C:\Users\user\Downloads\sheet_3_1.docx"

# Загрузка документа
doc = Document(file_path)

def add_text_after_in_textboxes(document, search_text, additional_text):
    """ Добавляет текст после указанного фрагмента в текстовых полях. """
    modified = False
    for shape in document.element.xpath('//w:txbxContent//w:p'):
        full_text = ''.join(e.text for e in shape.iter() if e.tag == qn('w:t') and e.text)
        if search_text in full_text:
            # Теперь замена происходит в собранном тексте
            modified_text = full_text.replace(search_text, search_text + additional_text)
            text_elements = [e for e in shape.iter() if e.tag == qn('w:t')]
            if text_elements:
                text_elements[0].text = modified_text # Заменяем текст в первом элементе
                for e in text_elements[1:]:
                    e.text = '' # Очищаем остальные элементы
                modified = True
    return modified

# Выполняем замену для каждого из текстов
modified = add_text_after_in_textboxes(doc, "Type:", "   4")
modified |= add_text_after_in_textboxes(doc, "Name:", " Gulnarabinistaliz")
modified |= add_text_after_in_textboxes(doc, "Surname:", " Gulnarabinistalizhanovna")
modified |= add_text_after_in_textboxes(doc, "St ID:", " 12345")

if modified:
    new_doc_path = r"C:\Users\user\Downloads\sheet_3_2.docx"
    doc.save(new_doc_path)
    print(f"Document modified and saved as {new_doc_path}")
else:
    print("No matching text found to modify.")
