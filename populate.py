from models import *
from init_db import session
from orm_utils import get_or_create


def create_subjects(names):
    return [get_or_create(session, Subject, name=name) for name in names]


def query_subjects():
    return session.query(Subject).all()


def query_questions(subject_list):
    """
            Такое сложное условие фильтра, потому что SQLAlchemy
            не поддерживает фильтрацию по релейшнам и нельзя сделать:
            session.query(Question).filter(subject.in_(subject_list)).all()
    """
    return [*session.query(Question).filter(Question.subject_id.in_(subj.id for subj in subject_list)).all()]


def query_answers(question_key):
    return session.query(Answer).filter_by(question=question_key).all()


def find_answer_by_id(answer_id):
    return session.query(Answer).get(answer_id)


"""
    Изначальное заполнение бд предметами, вопросами и ответами для них
"""

subjects = create_subjects(['Математика', 'Украинский', 'Физика'])

for subject in subjects:
    q1 = get_or_create(session, Question, text=f'Вопрос #1 по {subject.name}', subject=subject)
    q2 = get_or_create(session, Question, text=f'Вопрос #2 по {subject.name}', subject=subject)

    for question in [q1, q2]:
        a1 = get_or_create(session, Answer, text=f'Неверный ответ для вопроса {question.id}', question=question)
        a2 = get_or_create(session, Answer, text=f'Верный ответ для вопроса {question.id}', is_correct=True, question=question)


