# Basic CRUD operations for working with answers in the DB

from sqlalchemy.orm import Session
from app.models.answer import Answer                    # SQLAlchemy model
from app.schemas.answer import AnswerCreate             # Pydantic schema for validation

def create_answer(db: Session, answer: AnswerCreate) -> Answer:

    # Creates a new Answer record in the DB
    # model_dump() converts our Pydantic model to a dict that SQLAlchemy can use

    db_answer = Answer(**answer.model_dump())
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

def get_answers_for_document(db: Session, document_id: int):
    return db.query(Answer).filter(Answer.document_id == document_id).all()
