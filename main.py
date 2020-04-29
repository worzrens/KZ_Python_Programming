from tkinter import *
from populate import *


class TestTask:
    """
        Класс генерирующий одну пару вопросов-ответов по типу:
            Вопрос 1:
                1. Ответ 1
                2. Ответ 2
            【Подтвердить】
    """

    def __init__(self, root, question_key):
        self.root = root
        self.question = question_key
        self.question_component = self.generate_question()
        self.answer_result = IntVar()
        self.answer_buttons_arr = self.generate_buttons()
        self.confirm_answer_button = self.generate_confirm_answer_button()

    def generate_question(self):
        questions_list = Label(window, text=self.question.text, font=('Helvetica', 16, 'bold'))
        questions_list.pack()
        return questions_list

    def generate_buttons(self):
        return [self.create_answer_btn(answer) for answer in query_answers(self.question)]

    def handle_answer_selection(self):
        print(self.answer_result.get())

    def handle_answer_confirmation(self):
        global current_question
        """
            Такое ужасное условие потому-что Tkinter даже(!) не поддерживает Boolean переменные
        """
        answer_id = self.answer_result.get()
        print(find_answer_by_id(answer_id).is_correct)
        current_question += 1
        self.root.update()

    def create_answer_btn(self, answ):
        answ_btn = Radiobutton(
            self.root,
            text=answ.text,
            value=answ.id,
            variable=self.answer_result,
            command=self.handle_answer_selection
        )
        answ_btn.pack()
        return answ_btn

    def generate_confirm_answer_button(self):
        confirm_button = Button(self.root, text="Далi", command=self.handle_answer_confirmation)
        confirm_button.pack()
        return confirm_button

    def update_component(self, new_question):
        new_answers = query_answers(new_question)
        self.question_component.config(text=f"{new_question.text}", font=('Helvetica', 16, 'bold'))
        for answ_id, answer_btn in enumerate(self.answer_buttons_arr):
            answer_btn.config(text=new_answers[answ_id].text, value=new_answers[answ_id].id)


window = Tk()
window.title("Пiдготовчi курси")
window.geometry('1360x768')

subjects = query_subjects()

subjects_list = Listbox(window, height=len(subjects), width=15, selectmode=MULTIPLE)
subjects_list.pack()

for sub in subjects:
    subjects_list.insert(END, str(sub.name))
    # questions_count = Label(window, text=f'For {sub.name} are {len(query_questions([sub]))} questions\n',
    #                         font=('Helvetica', 14, 'bold'))
    # questions_count.pack()

questions = query_questions(subjects)
current_question = 0

test_task = TestTask(window, questions[current_question])


def update_current_question():
    test_task.update_component(questions[current_question])
    window.after(100, update_current_question)


update_current_question()
window.mainloop()
