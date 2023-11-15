import openpyxl

class StudentGrades:
    def __init__(self, grades, students):
        self.grades = {students[key]: value for key, value in grades.items()}

    def to_excel(self, filename):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Students's Grades"
        
        ws['A1'] = "Name Surname"
        ws['B1'] = "Grade"
        
        for idx, (name, grade) in enumerate(self.grades.items(), start=2):
            ws[f'A{idx}'] = name
            ws[f'B{idx}'] = grade
            
        wb.save(filename)

# grades = {3:44, 6:12, 25:33}
# students = {3:"Mahmud Abdulaev", 6:"Alina Milka", 25:"Lena Unichko"}

# student_grades = StudentGrades(grades, students)
# student_grades.to_excel('grades.xlsx')
