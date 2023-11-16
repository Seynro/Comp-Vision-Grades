import tkinter
import customtkinter
from main import Grading
import pickle
import sys
from excel_results import StudentGrades
import threading
from tkinter import ttk

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
        self.title("Input Data")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        # self.grid_columnconfigure(1, weight=1)
        # self.grid_columnconfigure((2, 3), weight=0)
        self.grid_columnconfigure((0, 1,2,3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # Первое поле ввода
        self.input_field_1 = customtkinter.CTkEntry(self, placeholder_text="Image path")
        self.input_field_1.grid(row=0, column=0, columnspan=4, padx=(40, 40), pady=(10, 10), sticky="nsew")

        # Второе.1 поле ввода
        self.input_field_2 = customtkinter.CTkEntry(self, placeholder_text="Answers' Dictionary Name")
        self.input_field_2.grid(row=1, column=0, columnspan=1, padx=(40, 40), pady=(10, 10), sticky="nsew")

        # Второе.2 поле ввода
        self.input_field_2_2 = customtkinter.CTkEntry(self, placeholder_text="Students' Dictionary Name")
        self.input_field_2_2.grid(row=1, column=1, columnspan=1, padx=(40, 40), pady=(10, 10), sticky="nsew")

        # Второе.3 поле ввода
        self.input_field_2_3 = customtkinter.CTkEntry(self, placeholder_text="Excel Name")
        self.input_field_2_3.grid(row=1, column=2, columnspan=1, padx=(40, 40), pady=(10, 10), sticky="nsew")

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
        self.generate_button = customtkinter.CTkButton(master=self, text="Generate tests", command=self.test_docx)
        self.generate_button.grid(row=4, column=2, padx=40, pady=20, sticky="nsew")

        # Виджет для вывода данных из командной строки
        self.output_textbox = customtkinter.CTkTextbox(self)
        self.output_textbox.grid(row=5, column=0, columnspan=4, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Перенаправление stdout и stderr в textbox
        sys.stdout = OutputRedirector(self.output_textbox)
        sys.stderr = OutputRedirector(self.output_textbox)

        # Создание прогресс бара, но пока не отображаем его
        self.progress_bar = customtkinter.CTkProgressBar(self)
        # Разместить прогресс бар справа от кнопки сабмит и сделать его такого же размера
        self.progress_bar.grid(row=4, column=1, padx=10, pady=40, sticky="nsew")
        self.progress_bar.grid_remove()  # Скрыть прогресс бар при запуске

    def test_docx(self):
        # Отключение кнопки, чтобы избежать повторного нажатия
        self.generate_button.configure(state='disabled')

        # Запускаем прогресс бар
        self.progress_bar.grid()
        self.progress_bar.set(0)  # Начать с нуля
        self.progress_bar.start()  # Запустить анимацию прогресс бара
        
        # Запуск длительной операции в отдельном потоке
        threading.Thread(target=self.process_data, daemon=True).start()

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
            n_students = int(self.input_field_3.get())
            n_questions = int(self.input_field_4.get())
            
            dict_stud = self.input_field_2_2.get()
            excel_name = self.input_field_2_3.get()

            with open(dict_ans, 'rb') as f:
                answers = pickle.load(f)

            with open(dict_stud, 'rb') as f:
                students = pickle.load(f)

            final_results = {}

            for i in range(1, 10):
                image_path = image_path_input + fr"0{i}.jpg"
                save_path = image_path.replace(".jpg","")
                obj = Grading(image_path, save_path, answers, n_questions)
                final_results = final_results | obj()
                self.output_textbox.insert(tkinter.END, str(final_results) + "\n")

            for i in range(10, n_students + 1):
                image_path = image_path_input + fr"{i}.jpg"
                save_path = image_path.replace(".jpg","")
                obj = Grading(image_path, save_path, answers, n_questions)
                final_results = final_results | obj()
                self.output_textbox.insert(tkinter.END, str(final_results) + "\n")

            create_excel = StudentGrades(final_results, students)
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
