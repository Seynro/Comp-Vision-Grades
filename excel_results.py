import openpyxl  # Убедитесь, что у вас установлена библиотека openpyxl

class StudentGrades:
    def __init__(self, grades, students):
        # Изменяем словарь для хранения ID студента и оценок
        self.grades = {students[key[1]]: (key[0], value) for key, value in grades.items()}

    def to_excel(self, filename):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Students's Grades"
        
        # Добавляем заголовки для новой колонки St ID и других колонок
        ws['A1'] = "St ID"
        ws['B1'] = "Name Surname"
        ws['C1'] = "Grade"
        
        # Заполняем строки данными
        for idx, (name, (st_id, grade)) in enumerate(self.grades.items(), start=2):
            ws[f'A{idx}'] = st_id
            ws[f'B{idx}'] = name
            ws[f'C{idx}'] = grade
            
        wb.save(filename)

# # Пример использования
# grades = {(1, 'student1'): 'A', (2, 'student2'): 'B'}
# students = {'student1': 'John Doe', 'student2': 'Jane Smith'}
# report = StudentGrades(grades, students)
# report.to_excel('example.xlsx')


# class StudentGrades:
#     def __init__(self, grades, students):
#         self.grades = {students[key]: value for key, value in grades.items()}

#     def to_excel(self, filename):
#         wb = openpyxl.Workbook()
#         ws = wb.active
#         ws.title = "Students's Grades"
        
#         ws['A1'] = "Name Surname"
#         ws['B1'] = "Grade"
        
#         for idx, (name, grade) in enumerate(self.grades.items(), start=2):
#             ws[f'A{idx}'] = name
#             ws[f'B{idx}'] = grade
            
#         wb.save(filename)