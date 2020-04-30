from tkinter import IntVar, Label, Radiobutton, NONE, Button, NORMAL, DISABLED

from orm_utils import find_answer_by_id, save_answer_result, query_answers
from tkinter_utils import pack_component


class TestTask:
    _tracker = None
    """
        Класс генерирующий одну пару вопросов-ответов по типу:
            Вопрос 1:
                1. Ответ 1
                2. Ответ 2
            【Подтвердить】 
            【Закончить】 
    """

    def __init__(self, root, subject_key, question_key, tracker):
        global _tracker
        _tracker = tracker

        self._ROOT = root
        self._SUBJECT = subject_key
        self._QUESTION = question_key
        self.__generate_whole_component()

    @pack_component
    def _generate_question(self):
        return Label(self._ROOT, text=self._QUESTION.text, font=('Helvetica', 16, 'bold'))

    @pack_component
    def _generate_select_answer_button(self, answ):
        return Radiobutton(
            self._ROOT,
            text=answ.text,
            value=answ.id,
            variable=self.answer_result,
            tristatevalue=NONE
        )

    def _generate_all_select_buttons(self):
        return [self._generate_select_answer_button(answer) for answer in query_answers(self._QUESTION)]

    @pack_component
    def _generate_confirm_answer_button(self):
        return Button(self._ROOT, text="Далi", command=self.handle_answer_confirmation, state=DISABLED)

    @pack_component
    def _generate_finish_button(self):
        return Button(self._ROOT, text="Скiнчити", command=self._handle_finish_test)

    def __generate_whole_component(self):
        self.question_component = self._generate_question()
        self.answer_result = IntVar()
        self.answer_buttons_arr = self._generate_all_select_buttons()
        self.confirm_answer_button = self._generate_confirm_answer_button()
        self.finish_button = self._generate_finish_button()

    def handle_answer_confirmation(self):
        _tracker.increment()
        score_saldo = find_answer_by_id(self.answer_result.get()).is_correct
        print("HANDLE ANSWER CONFIRMATION", self.answer_result.get(), 'SALDO', score_saldo)
        save_answer_result(self._SUBJECT, score_saldo)
        self.answer_result.set(-1)

    @staticmethod
    def _handle_finish_test():
        _tracker.premature_finish()

    def _remove_component(self):
        self.question_component.pack_forget()
        for answer_btn in self.answer_buttons_arr:
            answer_btn.pack_forget()
        self.confirm_answer_button.pack_forget()
        self.finish_button.pack_forget()

    def update_component(self, new_question):
        if not new_question:
            self._remove_component()

        self._QUESTION = new_question
        if new_question:
            self._SUBJECT = new_question.subject
            new_answers = query_answers(new_question)
            self.question_component.config(text=f"{new_question.text}", font=('Helvetica', 16, 'bold'))
            for answ_id, answer_btn in enumerate(self.answer_buttons_arr):
                answer_btn.config(text=new_answers[answ_id].text, value=new_answers[answ_id].id)

            if self.answer_result.get() != -1:
                self.confirm_answer_button.config(state=NORMAL)
            else:
                self.confirm_answer_button.config(state=DISABLED)