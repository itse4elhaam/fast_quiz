from sqlalchemy import Boolean, Column, ForeignKey, Integer, SavepointClause, String
from db import Base

class Questions(Base): # type: ignore
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    questions_text = Column(String, index=True)

class Choices(Base): # type: ignore
    __tablename__ = 'choices'
    id = Column(Integer, primary_key=True, index=True)
    choices_text = Column(String, index=True)
    is_correct = Column(Boolean, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))

