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

    def __init__(self, root, subject_key, question_key):
        self.root = root
        self.subject = subject_key
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
        print("SELECTED NEW", self.answer_result.get())

    def handle_answer_confirmation(self):
        global current_question
        current_question += 1

        score_saldo = find_answer_by_id(self.answer_result.get()).is_correct
        print("HANDLE ANSWER CONFIRMATION", self.answer_result.get(), 'SALDO', score_saldo)
        save_answer_result(self.subject, score_saldo)
        self.answer_result.set(-1)

    def create_answer_btn(self, answ):
        answ_btn = Radiobutton(
            self.root,
            text=answ.text,
            value=answ.id,
            variable=self.answer_result,
            command=self.handle_answer_selection,
            tristatevalue=NONE
        )
        answ_btn.pack()
        return answ_btn

    def generate_confirm_answer_button(self):
        confirm_button = Button(self.root, text="Далi", command=self.handle_answer_confirmation, state=DISABLED)
        confirm_button.pack()
        return confirm_button

    def update_component(self, new_question):
        if not new_question:
            self.question_component.pack_forget()
            for answer_btn in self.answer_buttons_arr:
                answer_btn.pack_forget()
            self.confirm_answer_button.pack_forget()

        self.question = new_question
        if new_question:
            self.subject = new_question.subject
            new_answers = query_answers(new_question)
            self.question_component.config(text=f"{new_question.text}", font=('Helvetica', 16, 'bold'))
            for answ_id, answer_btn in enumerate(self.answer_buttons_arr):
                answer_btn.config(text=new_answers[answ_id].text, value=new_answers[answ_id].id)

            if self.answer_result.get() != -1:
                self.confirm_answer_button.config(state=NORMAL)
            else:
                self.confirm_answer_button.config(state=DISABLED)


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

test_task = TestTask(window, questions[current_question].subject, questions[current_question])

result_scores = Label(window, text='')
result_scores.pack()

scores = Label(window, text=f'SCORES: {get_pupil_scores()}', font=('Helvetica', 16, 'bold'))
scores.pack()


def update_current_question():

    if current_question >= len(questions):
        result_scores.config(text="You completed all questions!!!", font=('Helvetica', 16, 'bold'))
        new_question = False
    else:
        new_question = questions[current_question]
    test_task.update_component(new_question)

    scores.config(text=f'SCORES: {get_pupil_scores()}')
    window.after(250, update_current_question)


update_current_question()
window.mainloop()
