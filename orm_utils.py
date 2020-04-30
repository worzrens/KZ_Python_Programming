import ast

from models import *
from init_db import session


def get_or_create(sql_session, model, **kwargs):
    """
        Самописный get_or_create, потому что почему-то его нет в алхимии
    """
    instance = sql_session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        sql_session.add(instance)
        sql_session.commit()
        return instance


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
    """
        Берёт первого(и единственного) ученика в бд
        Переводит строку его оценок в питоновский дикт
        Добавляет к значениям оценки и ответов в целом для
        выбранного предмета 0/1 и 1 соответсвенно
    """
    current_pupil = session.query(Pupil).first()

    previous_score = ast.literal_eval(current_pupil.scores)
    previous_score[current_subject.name] = {
        "score": previous_score[current_subject.name].get("score", 0) + score,
        "answers": previous_score[current_subject.name].get("answers", 0) + 1
    }

    current_pupil.scores = str(previous_score)
    session.commit()


def show_worst_subject_score():
    scores_dict = ast.literal_eval(get_pupil_scores())
    coeffs = {
        sub_scores.get("score") / sub_scores.get("answers"): sub_name
        for sub_name, sub_scores in scores_dict.items()
        if sub_scores.get('answers') > 0
    }

    FINAL_SCORES = list(coeffs.keys())
    if FINAL_SCORES.count(1) == len(FINAL_SCORES) and len(FINAL_SCORES) > 0:
        return True
    elif 1 in FINAL_SCORES:
        FINAL_SCORES.remove(1)

    if FINAL_SCORES:
        return coeffs.get(min(FINAL_SCORES))
    return None
