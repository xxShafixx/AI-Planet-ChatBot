# Import required SQLAlchemy components

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from.config import DATABASE_URL
import os

# Create database engine 
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} 
                       if "sqlite" in DATABASE_URL else{})

# Used to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()