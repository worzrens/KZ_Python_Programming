import ast
from tkinter import END, Listbox, Label, MULTIPLE

from orm_utils import get_pupil_scores, show_worst_subject_score


def pack_component(comp):
    """
        Декоратор деплоящий компоненты в TKinter-e
        K P A C U B O
    """

    def wrapper(*args):
        component = comp(*args)
        component.pack()
        return component

    return wrapper


class CurrentQuestionTracker:
    """
        Класс, следящий за тем, на какой сейчас вопрос следует отвечать
    """

    def __init__(self):
        self._counter = 0

    def get(self):
        return self._counter

    def increment(self):
        self._counter += 1
        return self._counter

    def premature_finish(self):
        self._counter = -1
        return self._counter


def update_scores_list(subjects_list):
    scores_dict = ast.literal_eval(get_pupil_scores())
    for subject in scores_dict.keys():
        subjects_list.insert(END,
                             f'{subject}:  {scores_dict.get(subject).get("score")}/{scores_dict.get(subject).get("answers")}')


@pack_component
def generate_subjects_list(root, subjects):
    return Listbox(root, height=len(subjects), width=18, selectmode=MULTIPLE)


@pack_component
def generate_result_scores(root):
    return Label(root, text='')



