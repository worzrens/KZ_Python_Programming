from models import *
from init_db import session
from orm_utils import get_or_create


def create_subjects(names):
    return [get_or_create(session, Subject, name=name) for name in names]


def populate_db():
    """
        Изначальное заполнение бд стандартным учеником, предметами, вопросами и ответами для них
        Открытого API у министерства образования нет, а скрапить ДПА
        или, не дай бог, копировать руками, я не буду -- у меня лапки
    """
    subjects = create_subjects(['Математика', 'Украинский', 'Физика', 'История', 'География'])

    for subject in subjects:
        questions = [get_or_create(session, Question, text=f'Вопрос #{q} по {subject.name}', subject=subject)
                     for q in range(1, 6)]

        for question in questions:
            a1 = get_or_create(session, Answer, text=f'Неверный ответ для вопроса {question.id}', question=question)
            a2 = get_or_create(session, Answer, text=f'Верный ответ для вопроса {question.id}', is_correct=True, question=question)

    pupil = get_or_create(session, Pupil, name='Шпорт Эдгар', scores=str({subj.name: {"score": 0, "answers": 0} for subj in subjects}))
