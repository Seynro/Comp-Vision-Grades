import tkinter
import customtkinter
from main import Grading
import pickle
import sys
from excel_results import StudentGrades
import threading
from tkinter import ttk
from doc_creating import Test_blank
from tkinter import Toplevel, Event
from tkinter import filedialog
from dictionary_creation import parse_questions, parse_students
from gmail_sender import email_sender
import pandas as pd
import glob
import os


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class OutputRedirector:
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, string):
        self.textbox.insert(tkinter.END, string)
        self.textbox.see(tkinter.END)

    def flush(self):
        pass

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Окно
        self.title("Grader")
        self.geometry(f"{1200}x{580}")


        # configure grid layout (4x4)
        # self.grid_columnconfigure(1, weight=1)
        # self.grid_columnconfigure((2, 3), weight=0)
        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # Первое поле ввода
        self.input_field_1 = tkinter.StringVar()
        self.input_field_1_label = customtkinter.CTkEntry(self, textvariable=self.input_field_1, state='disabled')
        self.input_field_1_label.grid(row=0, column=0, columnspan=4, padx=(40, 40), pady=(10, 10), sticky="nsew")
        self.input_field_1_button = customtkinter.CTkButton(self, text="Choose Image", command=self.choose_image, width=50)
        self.input_field_1_button.grid(row=0, column=4, columnspan=1,padx=(0,10), pady=(10, 10), sticky="nsew")

#----------------------------------------------------------------------------------------------------------------------


        # # Второе.1 поле ввода
        # self.input_field_2 = customtkinter.CTkEntry(self, placeholder_text="Answers' Dictionary Name")
        # self.input_field_2.grid(row=1, column=0, columnspan=1, padx=(40, 40), pady=(10, 10), sticky="nsew")
        self.input_field_2 = tkinter.StringVar()
        self.input_field_2_label = customtkinter.CTkEntry(self, textvariable=self.input_field_2, state='disabled', width=160)
        self.input_field_2_label.grid(row=1, column=0, columnspan=1, padx=(40,10), pady=(10, 10), sticky="nsew")
        self.input_field_2_button = customtkinter.CTkButton(self, text="Answers File", command=self.choose_questions_dict, width=50)
        self.input_field_2_button.grid(row=1, column=1, columnspan=1, pady=(10, 10), sticky="nsew")
#----------------------------------------------------------------------------------------------------------------------

        # Второе.2 поле ввода
        # self.input_field_2_2 = customtkinter.CTkEntry(self, placeholder_text="Students' Dictionary Name")
        # self.input_field_2_2.grid(row=1, column=2, columnspan=1, padx=(40, 40), pady=(10, 10), sticky="nsew")
        self.input_field_2_2 = tkinter.StringVar()
        self.input_field_2_2_label = customtkinter.CTkEntry(self, textvariable=self.input_field_2_2, state='disabled', width=160)
        self.input_field_2_2_label.grid(row=1, column=2, columnspan=1, padx=(40,10), pady=(10, 10), sticky="nsew")
        self.input_field_2_2_button = customtkinter.CTkButton(self, text="Students File", command=self.choose_students_dict, width=50)
        self.input_field_2_2_button.grid(row=1, column=3, columnspan=1, padx=(0, 40), pady=(10, 10), sticky="nsew")



#----------------------------------------------------------------------------------------------------------------------


        # Второе.3 поле ввода
        self.input_field_2_3 = customtkinter.CTkEntry(self, placeholder_text="Excel Name")
        self.input_field_2_3.grid(row=1, column=4, columnspan=1, padx=(0, 20), pady=(10, 10), sticky="nsew")

        # Третье поле ввода
        self.input_field_3 = customtkinter.CTkEntry(self, placeholder_text="Number of students")
        self.input_field_3.grid(row=2, column=0, columnspan=4, padx=(40, 40), pady=(10, 10), sticky="nsew")

        # Четвёртое поле ввода
        self.input_field_4 = customtkinter.CTkEntry(self, placeholder_text="Number of questions")
        self.input_field_4.grid(row=3, column=0, columnspan=4, padx=(40, 40), pady=(10, 10), sticky="nsew")

        # Кнопка для отправки данных
        self.submit_button = customtkinter.CTkButton(master=self, text="Submit", command=self.submit_data)
        self.submit_button.grid(row=4, column=0, padx=40, pady=20, sticky="nsew")

        # Кнопка для генерации Ворд документов
        self.generate_button = customtkinter.CTkButton(master=self, text="Generate buble sheets", command=self.test_docx)
        self.generate_button.grid(row=4, column=2, padx=40, pady=20, sticky="nsew")

        # Кнопка для генерации Dictionaries
        self.generate_dict_button = customtkinter.CTkButton(master=self, text="Generate test", command=self.generate_dicts)
        self.generate_dict_button.grid(row=4, column=3, padx=40, pady=20, sticky="nsew")

        # Кнопка для отправки mails
        self.mails_sent_button = customtkinter.CTkButton(master=self, text="Send emails", command=self.sent_mails)
        self.mails_sent_button.grid(row=4, column=4, padx=(0, 20), pady=20, sticky="nsew")
        
        # Ввод темы письма
        self.email_subject = customtkinter.CTkEntry(self, placeholder_text="Email subject") 
        self.email_subject.grid(row=2, column=4, columnspan=1, padx=(0, 20), pady=(10, 10), sticky="nsew")

        # Ввод тела письма
        self.email_body =  customtkinter.CTkEntry(self, placeholder_text="Email body") 
        self.email_body.grid(row=3, column=4, columnspan=1, padx=(0, 20), pady=(10, 10), sticky="nsew")

        # Виджет для вывода данных из командной строки
        self.output_textbox = customtkinter.CTkTextbox(self)
        self.output_textbox.grid(row=5, column=0, columnspan=5, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Перенаправление stdout и stderr в textbox
        sys.stdout = OutputRedirector(self.output_textbox)
        sys.stderr = OutputRedirector(self.output_textbox)

        # Создание прогресс бара, но пока не отображаем его
        self.progress_bar = customtkinter.CTkProgressBar(self)
        # Разместить прогресс бар справа от кнопки сабмит и сделать его такого же размера
        self.progress_bar.grid(row=4, column=1, padx=10, pady=40, sticky="nsew")
        self.progress_bar.grid_remove()  # Скрыть прогресс бар при запуске


        # Кнопка для отображения/скрытия боковой панели
        self.sidebar_button = customtkinter.CTkButton(self, text="☰", command=self.toggle_sidebar, width=20, height=20)
        self.sidebar_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        # Создание боковой панели
        self.sidebar = customtkinter.CTkFrame(self, width=200)
        self.sidebar.grid(row=0, column=0, rowspan=1, sticky="nw", padx=10, pady= 30)
        self.sidebar.grid_propagate(False)  # Запретить изменение размера
        self.sidebar.grid_remove()  # Скрыть боковую панель по умолчанию

        # Добавление кнопок в боковую панель
        self.grading_button = customtkinter.CTkButton(self.sidebar, text="Grading", command=self.grading_menu)
        self.grading_button.pack(padx = 10, pady=10)

        self.generating_button = customtkinter.CTkButton(self.sidebar, text="Generating", command=self.generating_menu)
        self.generating_button.pack(padx = 10, pady=10)

        # Дополнительные поля ввода и кнопки для режима "Generating"
        self.students_dict_path = tkinter.StringVar()
        self.questions_dict_path = tkinter.StringVar()

        self.students_dict_label = customtkinter.CTkEntry(self, textvariable=self.students_dict_path, state='disabled', width=200)
        self.questions_dict_label = customtkinter.CTkEntry(self, textvariable=self.questions_dict_path, state='disabled', width=200)



        # self.students_dict_entry = customtkinter.CTkEntry(self, placeholder_text="Students")
        # self.questions_dict_entry = customtkinter.CTkEntry(self, placeholder_text="Questions")
        self.students_dict_button = customtkinter.CTkButton(self, text="Choose Students Dictionary", command=self.choose_students_dict)
        self.questions_dict_button = customtkinter.CTkButton(self, text="Choose Questions Dictionary", command=self.choose_questions_dict)


        # Скрываем дополнительные элементы при инициализации
        self.hide_generating_elements()


    def choose_students_dict(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel list", "*.xlsx")])
        if file_path:
            self.input_field_2_2.set(file_path)
        

    def choose_questions_dict(self):
        file_path = filedialog.askopenfilename(filetypes=[("Word documents", "*.docx")])
        if file_path:
            self.input_field_2.set(file_path)
        

    def choose_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("image", "*jpg")])
        if file_path:
            self.input_field_1.set(file_path)
    
    def generate_dicts(self):
        self.generate_dict_button.configure(state='disabled')
        threading.Thread(target=self.sub_generate_dicts, daemon=True).start()

    def sent_mails(self):
        self.mails_sent_button.configure(state='disabled')
        threading.Thread(target=self.sub_sent_mails, daemon=True).start()

    def sub_sent_mails(self):
        try:
            dict_stud_path_exel = self.input_field_2_2.get()
            df = pd.read_excel(dict_stud_path_exel)
            subject = self.email_subject.get()
            body = self.email_body.get()
            for full_name in df['Students']:
                student_row = df[df['Students'].str.lower() == full_name.lower()]
                # Возвращение почты, если студент найден
                if not student_row.empty:
                    student_mail = student_row['Mails'].values[0]
                    print(full_name)
                    print(student_mail)
                
                    image_path = self.input_field_1.get()
                    last_slash_index = image_path.rfind("/")
                    if last_slash_index != -1:
                        trimmed_path = image_path[:last_slash_index+1]
                    else:
                        trimmed_path = image_path
                        print('Error: no slash found in path')
                    file_part = f"_TOTAL_RESULT_{full_name}.jpg"
                    # Поиск всех файлов, которые соответствуют шаблону
                    files = glob.glob(os.path.join(trimmed_path[:-1], f'*{file_part}'))
                    
                    for i in files:
                        student_file = i
                    email_sender(student_mail, subject, body, student_file)
                else:
                    print('Студент не найден')
            
        finally:
            self.after(0, lambda: self.mails_sent_button.configure(state='normal'))


    def sub_generate_dicts(self):
        try:
            dict_quest = self.input_field_2.get()
            n_students = int(self.input_field_3.get())
            n_questions = int(self.input_field_4.get())
            print(dict_quest)
            print(parse_questions(dict_quest, n_students, n_questions))
            dict_stud = self.input_field_2_2.get()
            print(dict_stud)
            print(parse_students(dict_stud))
        finally:
            self.after(0, lambda: self.generate_dict_button.configure(state='normal'))


    def generate_ques_dictionary(self):
        print("Hello")
        quest_dict_inp = self.questions_dict_label.get()
        print(parse_questions(quest_dict_inp))


    def generate_st_dictionary(self):
        print("Hello")
        st_dict_inp = self.students_dict_label.get()

    # Функция для показа элементов режима "Generating"
    def show_generating_elements(self):
        # self.students_dict_entry.grid(row=0, column=0, columnspan=4, padx=(40, 40), pady=(10, 10), sticky="nsew")
        # self.questions_dict_entry.grid(row=1, column=0, columnspan=4, padx=(40, 40), pady=(10, 10), sticky="nsew")
        self.students_dict_button.grid(row=2, column=0, padx=40, pady=20, sticky="nsew")
        self.questions_dict_button.grid(row=3, column=0, padx=40, pady=20, sticky="nsew")
        self.students_dict_label.grid(row=0, column=0, columnspan=4, padx=(40, 40), pady=(10, 10), sticky="nsew")
        self.questions_dict_label.grid(row=1, column=0, columnspan=4, padx=(40, 40), pady=(10, 10), sticky="nsew")
        self.hide_default_elements()

    # Функция для скрытия элементов режима "Generating"
    def hide_generating_elements(self):
        # self.students_dict_entry.grid_remove()
        # self.questions_dict_entry.grid_remove()
        self.students_dict_button.grid_remove()
        self.questions_dict_button.grid_remove()
        self.students_dict_label.grid_remove()
        self.questions_dict_label.grid_remove()

    # Функция для показа стандартных элементов
    def show_default_elements(self):
        # Показываем все стандартные элементы
        self.input_field_1.grid()
        self.input_field_2.grid()
        self.input_field_2_2.grid()
        self.input_field_2_3.grid()
        self.input_field_3.grid()
        self.input_field_4.grid()
        self.submit_button.grid()
        self.generate_button.grid()
        self.output_textbox.grid(row=5, column=0, columnspan=4, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.hide_generating_elements()

    # Функция для скрытия стандартных элементов
    def hide_default_elements(self):
        self.input_field_1.grid_remove()
        self.input_field_2.grid_remove()
        self.input_field_2_2.grid_remove()
        self.input_field_2_3.grid_remove()
        self.input_field_3.grid_remove()
        self.input_field_4.grid_remove()
        self.submit_button.grid_remove()
        self.generate_button.grid_remove()
        self.output_textbox.grid(row=2, column=1, rowspan=2, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

    # Функции-заглушки для кнопок меню
    def grading_menu(self):
        self.show_default_elements()

    def generating_menu(self):
        self.show_generating_elements()



    def toggle_sidebar(self):
        if self.sidebar.winfo_ismapped():
            self.sidebar.grid_remove()
        else:
            self.sidebar.grid()

    # Функции для обработки показа и скрытия боковой панели
    def show_sidebar(self, event: Event):
        self.sidebar.grid()

    def hide_sidebar(self, event: Event):
        self.sidebar.grid_remove()

    def test_docx(self):
        # Отключение кнопки, чтобы избежать повторного нажатия
        self.generate_button.configure(state='disabled')

        # Запускаем прогресс бар
        self.progress_bar.grid()
        self.progress_bar.set(0)  # Начать с нуля
        self.progress_bar.start()  # Запустить анимацию прогресс бара

        # Запуск длительной операции в отдельном потоке
        threading.Thread(target=self.create_tests, daemon=True).start()

    def create_tests(self):
        try:
            dict_stud = self.input_field_2_2.get()
            parse_students(dict_stud) 
            with open(dict_stud.replace('.xlsx', ''), 'rb') as f:
                    students = pickle.load(f)
            
            dict_stud = self.input_field_2_2.get()
            dict_stud = dict_stud.replace(".docx", "")

            last_slash_index = dict_stud.rfind("/")
            if last_slash_index != -1:
                trimmed_path = dict_stud[:last_slash_index+1]
            else:
                trimmed_path = dict_stud
                print('Error: no slash found in path')


            blank = Test_blank(students, trimmed_path)
            blank()
        finally:
            
            self.progress_bar.stop()
            self.progress_bar.set(100)  # Установить прогресс бар в конечное положение
            self.progress_bar.grid_remove()  # Скрыть прогресс бар
            # Возвращаем кнопку в обычное состояние в главном потоке
            self.after(0, lambda: self.generate_button.configure(state='normal'))
            

    # Функция для отправки данных из полей ввода
    def submit_data(self):
        # Отключение кнопки, чтобы избежать повторного нажатия
        self.submit_button.configure(state='disabled')

        # Запускаем прогресс бар
        self.progress_bar.grid()
        self.progress_bar.set(0)  # Начать с нуля
        self.progress_bar.start()  # Запустить анимацию прогресс бара

        # Запуск длительной операции в отдельном потоке
        threading.Thread(target=self.process_data, daemon=True).start()


    def process_data(self):
        try:
            image_path_input = self.input_field_1.get()
            
            dict_ans = self.input_field_2.get()
            dict_ans = dict_ans.replace(".docx", "")
            n_students = int(self.input_field_3.get())
            n_questions = int(self.input_field_4.get())

            dict_stud = self.input_field_2_2.get()
            dict_stud = dict_stud.replace(".xlsx", "")
            excel_name = self.input_field_2_3.get()

            image_path_input = image_path_input[:-6]
            

            with open(dict_ans, 'rb') as f:
                answers = pickle.load(f)

            with open(dict_stud, 'rb') as f:
                students = pickle.load(f)

            final_results = {}

#---------------------------------------------------------------------------------------------


            for i in range(1, n_students + 1):
                if i < 10:
                    image_path = image_path_input + fr"0{i}.jpg"
                else:
                    image_path = image_path_input + fr"{i}.jpg"
                save_path = image_path.replace(".jpg","")
                obj = Grading(image_path, save_path, answers, n_questions, students)
                final_results = final_results | obj()
                self.output_textbox.insert(tkinter.END, str(final_results) + "\n")

#---------------------------------------------------------------------------------------------

            # for i in range(1, 10):
            #     image_path = image_path_input + fr"0{i}.jpg"
            #     save_path = image_path.replace(".jpg","")
            #     obj = Grading(image_path, save_path, answers, n_questions)
            #     final_results = final_results | obj()
            #     self.output_textbox.insert(tkinter.END, str(final_results) + "\n")

            # for i in range(10, n_students + 1):
            #     image_path = image_path_input + fr"{i}.jpg"
            #     save_path = image_path.replace(".jpg","")
            #     obj = Grading(image_path, save_path, answers, n_questions)
            #     final_results = final_results | obj()
            #     self.output_textbox.insert(tkinter.END, str(final_results) + "\n")

            create_excel = StudentGrades(final_results, students)

            last_slash_index = dict_ans.rfind("/")
            if last_slash_index != -1:
                trimmed_path = dict_ans[:last_slash_index+1]
            else:
                trimmed_path = dict_ans
                print('Error: no slash found in path')

            excel_name = trimmed_path + excel_name + ".xlsx"

            create_excel.to_excel(excel_name)

            self.output_textbox.insert(tkinter.END, str(final_results) + "\n")
        finally:
            self.progress_bar.stop()
            self.progress_bar.set(100)  # Установить прогресс бар в конечное положение
            self.progress_bar.grid_remove()  # Скрыть прогресс бар
            # Возвращаем кнопку в обычное состояние в главном потоке
            self.after(0, lambda: self.submit_button.configure(state='normal'))

    def on_closing(self):
        # Восстановление стандартного вывода при закрытии приложения
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)  # Обработка закрытия окна
    app.mainloop()
