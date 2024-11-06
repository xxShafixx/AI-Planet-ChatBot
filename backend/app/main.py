# Import required packages and modules
from fastapi import FastAPI
from app.api.endpoints import qa
from .db import engine
from .models.document import Base
from fastapi.middleware.cors import CORSMiddleware


# Initialize FastAPI application
app = FastAPI()

# Include the QA router with URL prefix /api/v1
app.include_router(qa.router, prefix = "/api/v1")

# Configure CORS (Cross-Origin Resource Sharing) middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create all database tables based on SQLAlchemy models
Base.metadata.create_all(bind = engine)

# Root endpoint
@app.get("/")
def read_root():
    return{"message":"Welcome to the PDF QnA App!"}