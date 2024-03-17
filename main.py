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

@app.post("/questions/")
async def create_questions(question: QuestionBase, db: db_dependency):
    try:
        # Create the question
        db_question = models.Questions(question_text=question.question_text)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        
        # Create choices for the question
        for choice in question.choices:
            db_choice = models.Choices(
                choice_text=choice.choice_text,
                is_correct=choice.is_correct,
                question_id=db_question.id  # Use db_question.id after committing
            )
            db.add(db_choice)

        db.commit()  # Commit once after all changes
        return {"message": "Question created successfully"}
    except Exception as e:
        print(e)
        db.rollback()  # Rollback changes if an error occurs
        raise HTTPException(status_code=500, detail=str(e))