# SQLAlchemy model for the answers table
# Defines the structure of how we store Q&A pairs in the database

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base                                                     # Base class for all our models

class Answer(Base):
    __tablename__ = "answers"

    # Basic columns every qna entry needs
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Sets up the relationship with the Document model
    document = relationship("Document", back_populates="answers")
