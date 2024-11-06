#                                                                   				AI-Planet ChatBot

## Objective
Develop a full-stack application that allows users to upload PDF documents and ask questions regarding the content of these documents. The backend will process these documents and utilize natural language processing to provide answers to the questions posed by the users.

## Tools and Technologies
    Backend: FastAPI
    NLP Processing: LangChain/LLamaIndex
    Frontend: Next.js
    Database: SQLite or PostgreSQL
    File Storage: Local filesystem

## Installation and Setup

1. Clone the repository: git clone https://github.com/xxShafixx/AI-Planet-Chatbot.git   
2. Create and activate a virtual environment:
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
3. Install the required dependencies:
    pip install -r requirements.txt
4. Start the backend server:
    uvicorn app.main:app --reload
5. Start the frontend development server:
    npm run dev
6. Open the application in your browser at `http://localhost:3000`.

## API Documentation
    No API's were used since OLLAMA was used.

## Application Architecture
    The application contains backend and frontend in different folders.
    Backend further has app folder which consists of api, crud, models, schemas and utilities along with the configurations, dependencies and a main file.
    Frontend has a public folder which contains images and icons. It also has src folder which has globals.css, layout.js and page.js

