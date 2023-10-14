import tkinter
import customtkinter
from main import Grading
import pickle


# Для демонстрации добавлю импорт простого класса. В вашем реальном коде это будет из файла main.py.
class SampleClass:
    def __init__(self, var1, var2):
        print(f"Received variables: {var1}, {var2}")

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Окно
        self.title("Input Data")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Первое поле ввода
        self.input_field_1 = customtkinter.CTkEntry(self, placeholder_text="Image path")
        self.input_field_1.grid(row=0, column=0, columnspan=2, padx=(40, 40), pady=(40, 40), sticky="nsew")  # Увеличенные padx и pady

        # Второе поле ввода
        self.input_field_2 = customtkinter.CTkEntry(self, placeholder_text="Answers Path")
        self.input_field_2.grid(row=1, column=0, columnspan=2, padx=(40, 40), pady=(40, 40), sticky="nsew")  # Увеличенные padx и pady

        # Кнопка для отправки данных
        self.submit_button = customtkinter.CTkButton(master=self, text="Submit", command=self.submit_data)
        self.submit_button.grid(row=2, column=0, padx=40, pady=20, sticky="nsew")  # Увеличенные padx и pady

        # Виджет для вывода данных из командной строки
        self.output_textbox = customtkinter.CTkTextbox(self)
        self.output_textbox.grid(row=3, column=0, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")


    # Функция для отправки данных из полей ввода
    def submit_data(self):
        image_path_input = self.input_field_1.get()
        dict_ans = self.input_field_2.get()

#------------------------------------------------------------------------------------------------------
        with open(dict_ans, 'rb') as f:
            answers = pickle.load(f)


        final_results = {}

        for i in range(1, 10):
            image_path = image_path_input + fr"0{i}.jpg"
            save_path = image_path.replace(".jpg","")
            obj = Grading(image_path, save_path, answers)
            final_results = final_results | obj()
            self.output_textbox.insert(tkinter.END, final_results + "\n")

        for i in range(10, 23):
            image_path = image_path_input + fr"{i}.jpg"
            save_path = image_path.replace(".jpg","")
            obj = Grading(image_path, save_path, answers)
            final_results = final_results | obj()
            self.output_textbox.insert(tkinter.END, final_results + "\n")


        self.output_textbox.insert(tkinter.END, final_results + "\n")



if __name__ == "__main__":
    app = App()
    app.mainloop()
