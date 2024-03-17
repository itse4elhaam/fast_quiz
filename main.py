from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from db import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# defining types here 
class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]

def get_db():
    db = SessionLocal();
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/questions/{question_id}")
async def read_question(question_id: int, db:db_dependency):
    try:
        found_question = db.query(models.Questions).filter(models.Questions.id == question_id).first()
        if(not found_question):
            raise HTTPException(status_code=404, detail="Question not found")
        return found_question
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/choices/{question_id}")
async def read_choice(question_id: int, db:db_dependency):
    try:
        found_choice = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
        if(not found_choice):
            raise HTTPException(status_code=404, detail="choice not found")
        return found_choice
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/questions/")
async def create_questions(question: QuestionBase, db: db_dependency):
    try:
        db_question = models.Questions(question_text=question.question_text)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        
        for choice in question.choices:
            db_choice = models.Choices(
                choice_text=choice.choice_text,
                is_correct=choice.is_correct,
                question_id=db_question.id  
            )
            db.add(db_choice)

        db.commit()  
        return {"message": "Question created successfully"}
    except Exception as e:
        print(e)
        db.rollback()  
        raise HTTPException(status_code=500, detail=str(e))