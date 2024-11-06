# Pydantic models for request/response validation when dealing with answers
# Defines the shape of our JSON data when talking to the API

from pydantic import BaseModel
from datetime import datetime

# Fields needed to create a new answer
class AnswerCreate(BaseModel):
    document_id: int
    question: str
    answer: str

class AnswerResponse(AnswerCreate):
    # Extended version of AnswerCreate that includes the fields
    # that get added when it's stored in the database
    id: int
    timestamp: datetime

    # This lets Pydantic automatically convert from SQLAlchemy models
    class Config:
        orm_mode = True
