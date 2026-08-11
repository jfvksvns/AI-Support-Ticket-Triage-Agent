"""
SQLAlchemy database engine configuration and initialization.
Handles database connection pooling and lifecycle management.
"""

import logging
from typing import Generator

from sqlalchemy import create_engine, event, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.core.config import get_settings
from app.models.database import Base

logger = logging.getLogger(__name__)


class DatabaseEngine:
    """
    Manages SQLAlchemy database engine and sessions.
    Provides connection pooling and lifecycle management.
    """

    _engine: Engine = None
    _session_factory: sessionmaker = None

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the database engine and session factory.
        Creates tables if they don't exist.

        Raises:
            RuntimeError: If already initialized or on database connection error.
        """
        if cls._engine is not None:
            logger.warning("Database engine already initialized")
            return

        try:
            settings = get_settings()
            
            # Configure database URL for SQLite
            database_url = settings.DATABASE_URL
            
            # SQLite-specific engine configuration
            if "sqlite" in database_url:
                cls._engine = create_engine(
                    database_url,
                    connect_args={"check_same_thread": False},
                    poolclass=StaticPool,
                    echo=settings.DATABASE_ECHO,
                )
                # Register SQLite pragmas for better concurrency
                @event.listens_for(Engine, "connect")
                def set_sqlite_pragma(dbapi_conn, connection_record):
                    """Enable foreign keys and optimize SQLite for better concurrency."""
                    cursor = dbapi_conn.cursor()
                    cursor.execute("PRAGMA foreign_keys=ON")
                    cursor.execute("PRAGMA journal_mode=WAL")
                    cursor.close()
            else:
                # Generic configuration for other databases
                cls._engine = create_engine(
                    database_url,
                    echo=settings.DATABASE_ECHO,
                )

            # Create session factory
            cls._session_factory = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=cls._engine
            )

            # Create all tables
            Base.metadata.create_all(bind=cls._engine)
            logger.info(f"Database initialized successfully: {database_url}")

        except Exception as e:
            logger.error(f"Failed to initialize database: {str(e)}")
            raise RuntimeError(f"Database initialization failed: {str(e)}")

    @classmethod
    def get_engine(cls) -> Engine:
        """
        Get the database engine instance.
        Initializes if not already done.

        Returns:
            Engine: SQLAlchemy engine instance.
        """
        if cls._engine is None:
            cls.initialize()
        return cls._engine

    @classmethod
    def get_session(cls) -> Session:
        """
        Create a new database session.
        Initializes engine if needed.

        Returns:
            Session: SQLAlchemy session instance.
        """
        if cls._session_factory is None:
            cls.initialize()
        return cls._session_factory()

    @classmethod
    def dispose(cls) -> None:
        """
        Dispose of the engine and close all connections.
        Call this on application shutdown.
        """
        if cls._engine is not None:
            cls._engine.dispose()
            cls._engine = None
            cls._session_factory = None
            logger.info("Database engine disposed")

    @classmethod
    def health_check(cls) -> bool:
        """
        Check database connectivity and health.

        Returns:
            bool: True if database is healthy, False otherwise.
        """
        try:
            session = cls.get_session()
            session.execute("SELECT 1")
            session.close()
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            return False


# Create engine instance on module import
def get_database_engine() -> Engine:
    """
    Get or create the database engine.

    Returns:
        Engine: SQLAlchemy engine instance.
    """
    return DatabaseEngine.get_engine()


def create_session() -> Session:
    """
    Create a new database session.

    Returns:
        Session: SQLAlchemy session instance.
    """
    return DatabaseEngine.get_session()


def init_db() -> None:
    """Initialize database tables and engine."""
    DatabaseEngine.initialize()


def close_db() -> None:
    """Close and dispose of database connections."""
    DatabaseEngine.dispose()
