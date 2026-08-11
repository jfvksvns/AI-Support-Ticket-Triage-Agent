"""
Database session dependency injection for FastAPI.
Provides session instances to route handlers.
"""

from typing import Generator

from sqlalchemy.orm import Session

from app.database.engine import DatabaseEngine


def get_db() -> Generator[Session, None, None]:
    """
    Dependency injection function for database sessions.
    
    Yields:
        Session: SQLAlchemy session for database operations.
        
    Example:
        @app.get("/tickets")
        def list_tickets(db: Session = Depends(get_db)):
            tickets = db.query(Ticket).all()
            return tickets
    """
    session = DatabaseEngine.get_session()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
