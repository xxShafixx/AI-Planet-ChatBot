# SQLAlchemy model for documents
# Stores the uploaded PDFs' metadata and their extracted text

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Document(Base):
    __tablename__ = "documents"

    # Main columns for document info
    id = Column(Integer, primary_key = True, index = True)
    filename = Column(String, index = True)
    upload_date = Column(DateTime, default = datetime.utcnow)
    extracted_text = Column(Text)

    # Link to Answer model - if we delete a document, also delete its answers
    answers = relationship("Answer", back_populates = "document", cascade = "all, delete")