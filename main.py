import tkinter as tk
from PIL import Image, ImageTk


class TemperamentTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Тест на темперамент")
        self.root.geometry("400x600")

        self.questions = {
            "Вам легко заводить новые знакомства?": ["Абсолютно нет", "Не очень", "Довольно легко", "Очень легко",
                                                     "Абсолютно да"],
            "Как часто вы проявляете эмоции?": ["Почти никогда", "Иногда", "Часто", "Почти всегда", "Абсолютно да"],
            "Склонны ли вы к переживаниям и анализу прошлых событий?": ["Абсолютно нет", "Не очень", "Довольно сильно",
                                                                        "Очень сильно", "Абсолютно да"],
            "Вы легко поддаетесь влиянию окружающих?": ["Абсолютно нет", "Не очень", "Довольно легко", "Очень легко",
                                                        "Абсолютно да"],
            "Предпочитаете ли вы планировать свое время заранее?": ["Абсолютно нет", "Не очень", "Довольно легко",
                                                                    "Очень легко", "Абсолютно да"],
            "Способны ли вы выражать свои мысли и чувства легко и свободно?": ["Абсолютно нет", "Не очень",
                                                                               "Довольно легко", "Очень легко",
                                                                               "Абсолютно да"],
            "Как вы относитесь к переменам в жизни?": ["Абсолютно нет", "Не очень", "Довольно легко", "Очень легко",
                                                       "Абсолютно да"],
            "Часто ли вы ощущаете усталость и потребность в отдыхе?": ["Абсолютно нет", "Не очень", "Довольно часто",
                                                                       "Очень часто", "Абсолютно да"],
            "Легко ли вас что-то расстраивает?": ["Абсолютно нет", "Не очень", "Довольно легко", "Очень легко",
                                                  "Абсолютно да"],
            "Как вы реагируете на неожиданные ситуации?": ["Абсолютно нет", "Не очень", "Довольно спокойно",
                                                           "Очень спокойно", "Абсолютно да"],
            "Склонны ли вы к самокритике?": ["Абсолютно нет", "Не очень", "Довольно сильно", "Очень сильно",
                                             "Абсолютно да"],
            "Предпочитаете ли вы работать в команде или в одиночестве?": ["Абсолютно нет", "Не очень", "Довольно часто",
                                                                          "Очень часто", "Абсолютно да"],
            "Любите ли вы новые впечатления и приключения?": ["Абсолютно нет", "Не очень", "Довольно сильно",
                                                              "Очень сильно", "Абсолютно да"],
            "Склонны ли вы к обдуманным и взвешенным решениям?": ["Абсолютно нет", "Не очень", "Довольно легко",
                                                                  "Очень легко", "Абсолютно да"],
            "Как вы реагируете на критику со стороны окружающих?": ["Не очень положительно", "Спокойно",
                                                                    "Очень спокойно"],
        }

        self.temperament_rules = {
            "Флегматик": lambda scores: sum(scores) < 25,
            "Меланхолик": lambda scores: 25 <= sum(scores) < 50,
            "Сангвиник": lambda scores: 50 <= sum(scores) < 75,
            "Холерик": lambda scores: sum(scores) >= 75,
        }

        self.temperament_images = {
            "Флегматик": "./images/phlegmatic.jfif",
            "Меланхолик": "./images/melancholic.jfif",
            "Сангвиник": "./images/sanguine.jfif",
            "Холерик": "./images/choleric.jfif",
        }

        self.answers = []
        self.current_question_index = 0

        self.image_label = None

        self.create_widgets()

    def create_widgets(self):
        self.question_label = tk.Label(self.root, text=list(self.questions.keys())[self.current_question_index],
                                       wraplength=350)
        self.question_label.pack(pady=10)

        self.var = tk.StringVar()
        for i, option_text in enumerate(self.questions[list(self.questions.keys())[self.current_question_index]]):
            option = tk.Radiobutton(self.root, text=option_text, variable=self.var, value=str(i + 1))
            option.pack()

        self.next_button = tk.Button(self.root, text="Следующий вопрос", command=self.next_question)
        self.next_button.pack(pady=20)

    def next_question(self):
        answer = self.var.get()
        if answer:
            self.answers.append(int(answer))
            self.var.set("")
            self.current_question_index += 1

            if self.current_question_index < len(self.questions):
                self.question_label.config(text=list(self.questions.keys())[self.current_question_index])

                for widget in self.root.winfo_children():
                    if isinstance(widget, tk.Radiobutton):
                        widget.destroy()

                for i, option_text in enumerate(
                        self.questions[list(self.questions.keys())[self.current_question_index]]):
                    option = tk.Radiobutton(self.root, text=option_text, variable=self.var, value=str(i + 1))
                    option.pack()

                if self.current_question_index > 0:
                    self.next_button.pack(pady=20)
            else:
                self.show_results()
                self.next_button.pack_forget()

    def show_results(self):
        temperament = "Неопределенный темперамент"
        for temperament_name, rule in self.temperament_rules.items():
            if rule(self.answers):
                temperament = temperament_name
                break

        image_path = self.temperament_images.get(temperament, "./images/default.jpg")

        self.result_label = tk.Label(self.root, text=f"Ваш темперамент: {temperament}", font=("Helvetica", 12, "bold"))
        self.result_label.pack(pady=10)

        self.show_image(image_path)

        self.restart_button = tk.Button(self.root, text="Начать заново", command=self.restart_test)
        self.restart_button.pack(pady=20)

    def show_image(self, image_path):
        img = Image.open(image_path)
        img = img.resize((300, 300))
        img = ImageTk.PhotoImage(img)

        if self.image_label:
            self.image_label.destroy()

        self.image_label = tk.Label(self.root, image=img)
        self.image_label.image = img
        self.image_label.pack(pady=20)

    def restart_test(self):
        self.answers = []
        self.current_question_index = 0
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label) or isinstance(widget, tk.Radiobutton) or isinstance(widget, tk.Button):
                widget.destroy()
        self.create_widgets()


if __name__ == "__main__":
    root = tk.Tk()
    app = TemperamentTestApp(root)
    root.mainloop()
