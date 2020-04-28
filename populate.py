from models import *
from init_db import session


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def create_subjects(names):
    if type(names) is str:
        return get_or_create(session, Subject, name=names)
    elif type(names) is list:
        return [get_or_create(session, Subject, name=name) for name in names]


subjects = create_subjects(['Математика', 'Украинский', 'Физика'])

for subject in subjects:
    q1 = get_or_create(session, Question, text=f'Вопрос #1 по {subject.name}', subject=subject)
    q2 = get_or_create(session, Question, text=f'Вопрос #2 по {subject.name}', subject=subject)

    for question in [q1, q2]:
        a1 = get_or_create(session, Answer, text='A1', question=question)
        a2 = get_or_create(session, Answer, text='A2', is_correct=True, question=question)


def query_subjects():
    return session.query(Subject).all()


def query_questions(subj_name):
    return session.query(Question).filter_by(subject=subj_name).all()


def query_answers():
    return session.query(Answer).all()
