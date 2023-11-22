from typing import Any
from docx import Document
from docx.oxml.ns import qn


class Test_blank():
    def __init__(self, student_dictionary):
        self.student_dictionary = student_dictionary
        self.file_path = "sheet_3_1.docx"

    def add_text_after_in_textboxes(self, document, search_text, additional_text):
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

    def __call__(self):
        i = 0
        # Извлечение данных первого студента
        for type, students in self.student_dictionary.items():
            i += 1
            for full_name, st_id in students.items():
                name, surname = full_name.split()

                doc = Document(self.file_path)
                # Выполняем замену для каждого из текстов
                modified = self.add_text_after_in_textboxes(doc, "Type:", f"   {type}")
                modified |= self.add_text_after_in_textboxes(doc, "Name:", f" {name}")
                modified |= self.add_text_after_in_textboxes(doc, "Surname:", f" {surname}")
                modified |= self.add_text_after_in_textboxes(doc, "St ID:", f" {st_id}")

                if modified:
                    new_doc_path = f"blanks/studnet_{i}.docx"
                    doc.save(new_doc_path)
                    print(f"Document modified and saved as {new_doc_path}")
                else:
                    print("No matching text found to modify.")


# student_dict = {1: {"Alice Johnson": 12345}, 2: {"Bob Smith": 45678}}

# obj = Test_blank(student_dict)
# obj()


