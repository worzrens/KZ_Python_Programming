from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship

from init_db import engine

"""
    Модели для предмета, вопроса, ответов, ученика
"""
Base = declarative_base()


class Pupil(Base):
    __tablename__ = 'pupil'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    scores = Column(String)

    def __repr__(self):
        return f'Pupil: {self.name}| Scores: {self.scores}'


class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    question = relationship('Question', backref='subject')

    def __repr__(self):
        return f'Subject: {self.name}'


class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    subject_id = Column(Integer, ForeignKey('subject.id'))
    answer = relationship('Answer', backref='question')

    def __repr__(self):
        return f'S: {self.subject.name}| Q: {self.text}'


class Answer(Base):
    __tablename__ = 'answer'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey('question.id'))

    def __repr__(self):
        return f'S: {self.question.subject.name}| Q: {self.question.text} | A: {self.text} {self.is_correct}'


Base.metadata.create_all(engine)
