import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

"""
    Создает локальную бд и сессию для неё
"""

basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine('sqlite:///' + os.path.join(basedir, 'app.db'), echo=True)

Session = sessionmaker(bind=engine)
session = Session()
