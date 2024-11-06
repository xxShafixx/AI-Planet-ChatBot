# Database configuration
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://shafi:1411@localhost:5432/db"
)
