from .db import SessionLocal

def get_db():
    """
    Database dependency function - creates and manages database sessions
    
    This function creates a new database session for each request and ensures 
    proper cleanup when the request is complete.
    
    Yields:
        SessionLocal: Database session that can be used in route handlers
    """

    # Create a new database session
    db = SessionLocal()

    try:
        # Yield the database session to the route handler
        yield db
    finally:
        # Ensure the database session is closed after the request is complete
        db.close()