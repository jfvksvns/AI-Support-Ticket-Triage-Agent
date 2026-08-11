"""
Pytest configuration and shared test fixtures.
Provides common test setup and utilities for all test modules.
"""

import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app
from app.models.database import Base
from app.database.session import get_db


@pytest.fixture(scope="session")
def db_engine():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create a new database session for each test."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """Create a test client with test database session."""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_ticket_data():
    """Sample ticket creation data for testing."""
    return {
        "subject": "Cannot connect to VPN",
        "description": "I've been unable to connect to the company VPN for the past 2 hours. I've restarted my machine and the VPN client. Error code: 1234",
        "reporter_name": "John Doe",
        "reporter_email": "john.doe@company.com",
        "department": "Sales"
    }


@pytest.fixture
def sample_classification():
    """Sample classification response from AI."""
    return {
        "category": "Network",
        "urgency": "High",
        "confidence": 85,
        "assigned_team": "Network Team",
        "summary": "VPN connectivity issue affecting remote access",
        "reasoning": "User cannot connect to VPN after restart. This is a network connectivity issue requiring Network Team intervention.",
        "suggested_response": "We've escalated your VPN issue to our Network Team. They will contact you within the next hour.",
        "requires_human_review": False
    }
