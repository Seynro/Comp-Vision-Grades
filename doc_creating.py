from typing import Any
from docx import Document
from docx.oxml.ns import qn
import os
from PyPDF2 import PdfWriter
from docx2pdf import convert

class Test_blank():
    def __init__(self, student_dictionary, folder_path):
        self.student_dictionary = student_dictionary
        self.file_path = "sheet_3_1.docx"
        self.folder_path = folder_path

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
                    folder_path = os.path.join(self.folder_path[:-1], "blanks")
                    # Проверяем, существует ли папка
                    if not os.path.exists(folder_path):
                        # Если папки нет, создаем ее
                        os.makedirs(folder_path)
                        print(f"Папка '{folder_path}' создана.")
                    else:
                        print(f"Папка '{folder_path}' уже существует.")

                    new_doc_path = self.folder_path + f"blanks/studnet_{i}.docx"
                    doc.save(new_doc_path)
                    print(f"Document modified and saved as {new_doc_path}")
                    convert(new_doc_path)
                else:
                    print("No matching text found to modify.")
        
        merger = PdfWriter()
        pdf_list = [i for i in os.listdir(self.folder_path + "blanks") if i.endswith(".pdf")]
        pdf_list = sorted(pdf_list, key=lambda x: int(x.split("_")[1].split(".")[0]))
        for pdf in pdf_list:
            merger.append(self.folder_path + "blanks\\" + pdf)

        merger.write(self.folder_path + "students_merged_pdf.pdf")
        merger.close()


# student_dict = {1: {"Alice Johnson": 12345}, 2: {"Bob Smith": 45678}}

# obj = Test_blank(student_dict)
# obj()


