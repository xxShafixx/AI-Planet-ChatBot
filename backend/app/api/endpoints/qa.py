# Imports
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from pathlib import Path
import fitz #PyMuPDF for PDF processing
import shutil
from datetime import datetime
from sqlalchemy.orm import Session
from app.crud.document import create_document, get_document_by_id
from app.dependencies import get_db
from pydantic import BaseModel
from app.utils.qa_processing import generate_answer
from typing import List
from app.schemas.answer import AnswerCreate, AnswerResponse
from app.crud.answer import create_answer, get_answers_for_document

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

# Endpoint for uploading PDFs
@router.post("/upload")
async def upload_def(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail = "Only PDF files are supported!")
    
    # Create uploads directory if it doesn't exist 
    upload_dir = Path("uploads")
    upload_dir.mkdir(parents = True, exist_ok = True)
    pdf_path = upload_dir / file.filename

    # Save the uploaded file
    with pdf_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text from the PDF
    try:
        text = extract_text(pdf_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail = f"Error extracting text: {str(e)}")
    
    # Store the document info in the db
    document = create_document(db, filename = file.filename, extracted_text = text)

    return JSONResponse(content={"message" : "PDF uploaded and processed successfully", "document_id" : document.id})


# Endpoint for asking questions
@router.post("/ask/{document_id}")
async def ask_question(document_id: int, request: QuestionRequest, db: Session = Depends(get_db)):
    
    document = get_document_by_id(db, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found.")

    
    answer = generate_answer(document.extracted_text, request.question)

    answer_object = create_answer(db, AnswerCreate(document_id=document_id, question=request.question, answer=answer))

    return {"answer": answer_object.answer}

# Helper function to extract text from PDFs using PyMuPDF
def extract_text(pdf_path: Path) -> str:
    text = ""
    with fitz.open(pdf_path) as pdf_document:
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

    return text

# Endpoint to get the history of questions for a document
@router.get("/ask/{document_id}/history", response_model=List[AnswerResponse])
async def get_question_history(document_id: int, db: Session = Depends(get_db)):
    answers = get_answers_for_document(db, document_id)
    if not answers:
        raise HTTPException(status_code=404, detail="No question history found for this document.")
    
    return answers


