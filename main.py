from tkinter import *
from populate import *


class TestTask:
    """
        Класс генерирующий одну пару вопросов-ответов по типу:
            Вопрос 1:
                1. Ответ 1
                2. Ответ 2
    """
    def __init__(self, root, question_key):
        self.root = root
        self.question = question_key
        self.answer_result = IntVar()
        self.answer_buttons_arr = self.generate_buttons()

    def generate_buttons(self):
        return [self.create_answer_btn(answer) for answer in query_answers(self.question)]

    def select_answer(self):
        print(self.answer_result.get())

    def create_answer_btn(self, answ):
        answ_btn = Radiobutton(
            self.root,
            text=f"{answ.id}|{answ.text}",
            value=answ.id,
            variable=self.answer_result,
            command=self.select_answer
        )
        answ_btn.pack()
        return answ_btn


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


for question in query_questions(subjects):
    questions_list = Label(window, text=f"{question.text}", font=('Helvetica', 16, 'bold'))
    questions_list.pack()
    answered = IntVar()

    test_task = TestTask(window, question)

linebreak = Label(window, text="\n")
linebreak.pack()


window.mainloop()
