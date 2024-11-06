# Database operations for managing documents

from sqlalchemy.orm import Session
from ..models.document import Document
from datetime import datetime

# Create a new document with current UTC timestamp
def create_document(db: Session, filename: str, extracted_text: str):
    db_document = Document(
        filename=filename,
        upload_date=datetime.utcnow(),
        extracted_text=extracted_text
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

# Query to get a single document by ID
def get_document_by_id(db: Session, document_id: int):
    return db.query(Document).filter(Document.id == document_id).first()

# Get all documents 
def get_all_documents(db: Session):
    return db.query(Document).all()