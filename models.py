from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///schools.db', convert_unicode=True, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()




class Teacher(Base):
    __tablename__ = "teachers"
    id = Column('user_id', Integer, primary_key=True)
    username = Column('username', String(20), unique=True, index=True)
    password = Column('password', String(10))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Student(Base):
    __tablename__ = 'student'
    studentid = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(25))
    lastname = Column(String(25))

    def __init__(self, firstname=None, lastname=None):
        self.firstname = firstname
        self.lastname = lastname


class Quiz(Base):
    __tablename__ = 'quiz'
    quizid = Column(Integer, primary_key=True)
    subject = Column(String(25))
    questions = Column(Integer)
    date = Column(String(15))

    def __init__(self, subject, questions, date):
        self.subject = subject
        self.questions = questions
        self.date = date


class Grades(Base):
    __tablename__ = 'grades'
    studentid = Column(Integer, ForeignKey("student.studentid"),
                       primary_key=True)
    quizid = Column(Integer, ForeignKey("quiz.quizid"), primary_key=True)
    score = Column(Integer)
