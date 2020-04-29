import ast

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


def get_pupil_scores():
    return session.query(Pupil).first().scores


def save_answer_result(current_subject, score):
    current_pupil = session.query(Pupil).first()

    previous_score = ast.literal_eval(current_pupil.scores)
    previous_score[current_subject.name] = {
        "score": previous_score[current_subject.name].get("score", 0)+score,
        "answers": previous_score[current_subject.name].get("answers", 0)+1
    }

    current_pupil.scores = str(previous_score)
    session.commit()
    print('\n\nCURRENT SUBJECT', current_subject.name, 'ANSWER', score, 'CURRENT PUPIL AFTER CHANGES', current_pupil.scores, '\n\n')


"""
    Изначальное заполнение бд стандартным учеником, предметами, вопросами и ответами для них
"""

"""
    Открытого API у министерства образования нет, а скрапить ДПА
    или, не дай бог, копировать руками, я не буду -- у меня лапки
"""
subjects = create_subjects(['Математика', 'Украинский', 'Физика'])

for subject in subjects:
    q1 = get_or_create(session, Question, text=f'Вопрос #1 по {subject.name}', subject=subject)
    q2 = get_or_create(session, Question, text=f'Вопрос #2 по {subject.name}', subject=subject)

    for question in [q1, q2]:
        a1 = get_or_create(session, Answer, text=f'Неверный ответ для вопроса {question.id}', question=question)
        a2 = get_or_create(session, Answer, text=f'Верный ответ для вопроса {question.id}', is_correct=True, question=question)

pupil = get_or_create(session, Pupil, name='Шпорт Эдгар', scores=str({subj.name: {"score": 0, "answers": 0} for subj in subjects}))
