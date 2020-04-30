import ast
from tkinter import *

from orm_utils import query_questions, query_subjects, show_worst_subject_score
from test_task import TestTask
from tkinter_utils import CurrentQuestionTracker, update_scores_list, generate_subjects_list, generate_result_scores


def update_current_question():
    if cur_q.get() >= len(questions) or cur_q.get() == -1:
        SCORES = show_worst_subject_score()
        if SCORES is not None and SCORES is not True:
            text_message = f"\nВы закончили тест!!!, \nХудшие оценки по {SCORES}"
        elif SCORES is True:
            text_message = f'\nВсе тесты выполнены идеально!'
        else:
            text_message = f"\nВы не ответили ни на один вопрос :с"

        result_scores.config(text=text_message, font=('Helvetica', 16, 'bold'))
        new_question = False
    else:
        new_question = questions[cur_q.get()]
    test_task.update_component(new_question)

    subjects_list.delete(0, END)
    update_scores_list(subjects_list)
    WINDOW.after(250, update_current_question)


WINDOW = Tk()
WINDOW.title("Пiдготовчi курси")
WINDOW.geometry('640x480')

subjects = query_subjects()
questions = query_questions(subjects)
cur_q = CurrentQuestionTracker()

subjects_list = generate_subjects_list(WINDOW, subjects)
result_scores = generate_result_scores(WINDOW)
update_scores_list(subjects_list)

test_task = TestTask(WINDOW, questions[cur_q.get()].subject, questions[cur_q.get()], cur_q)

update_current_question()
WINDOW.mainloop()
