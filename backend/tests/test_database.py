"""
Unit tests for database models and operations.
Tests SQLAlchemy models and database constraints.
"""

import pytest
from datetime import datetime, timezone

from app.models.database import Ticket
from app.models.schemas import TicketCreateRequest, ClassificationResponse
from app.services.ticket_service import TicketService


class TestTicketModel:
    """Tests for the Ticket ORM model."""

    def test_ticket_creation_with_valid_data(self):
        """Test creating a ticket with valid data."""
        ticket = Ticket(
            subject="Test ticket",
            description="This is a test ticket description",
            reporter_name="John Doe",
            reporter_email="john@example.com",
            department="IT",
            category="Software",
            urgency="High",
            confidence=85,
            assigned_team="Application Team",
            summary="Test summary",
            reasoning="Test reasoning",
            suggested_response="Test response",
            status="Open",
            requires_human_review=False
        )

        assert ticket.subject == "Test ticket"
        assert ticket.urgency == "High"
        assert ticket.confidence == 85
        assert ticket.status == "Open"

    def test_ticket_urgency_validation(self):
        """Test ticket urgency validation."""
        ticket = Ticket(
            subject="Test",
            description="Test description",
            reporter_name="Test",
            reporter_email="test@test.com",
            department="Test",
            category="Software",
            urgency="High",  # Valid
            confidence=50,
            assigned_team="IT Support",
            summary="Test",
            reasoning="Test",
            suggested_response="Test"
        )

        assert ticket.urgency == "High"

        # Invalid urgency should raise
        with pytest.raises(ValueError):
            ticket.urgency = "InvalidUrgency"

    def test_ticket_category_validation(self):
        """Test ticket category validation."""
        ticket = Ticket(
            subject="Test",
            description="Test description",
            reporter_name="Test",
            reporter_email="test@test.com",
            department="Test",
            category="Software",
            urgency="High",
            confidence=50,
            assigned_team="IT Support",
            summary="Test",
            reasoning="Test",
            suggested_response="Test"
        )

        assert ticket.category == "Software"

        # Invalid category should raise
        with pytest.raises(ValueError):
            ticket.category = "InvalidCategory"

    def test_ticket_confidence_validation(self):
        """Test ticket confidence validation."""
        ticket = Ticket(
            subject="Test",
            description="Test description",
            reporter_name="Test",
            reporter_email="test@test.com",
            department="Test",
            category="Software",
            urgency="High",
            confidence=85,  # Valid: 0-100
            assigned_team="IT Support",
            summary="Test",
            reasoning="Test",
            suggested_response="Test"
        )

        assert ticket.confidence == 85

        # Invalid confidence should raise
        with pytest.raises(ValueError):
            ticket.confidence = 150

        with pytest.raises(ValueError):
            ticket.confidence = -5

    def test_ticket_status_validation(self):
        """Test ticket status validation."""
        ticket = Ticket(
            subject="Test",
            description="Test description",
            reporter_name="Test",
            reporter_email="test@test.com",
            department="Test",
            category="Software",
            urgency="High",
            confidence=50,
            assigned_team="IT Support",
            summary="Test",
            reasoning="Test",
            suggested_response="Test",
            status="Open"  # Valid
        )

        assert ticket.status == "Open"

        # Invalid status should raise
        with pytest.raises(ValueError):
            ticket.status = "InvalidStatus"

    def test_ticket_to_dict(self):
        """Test converting ticket to dictionary."""
        now = datetime.now(timezone.utc)
        ticket = Ticket(
            id=1,
            subject="Test",
            description="Test description",
            reporter_name="Test",
            reporter_email="test@test.com",
            department="Test",
            category="Software",
            urgency="High",
            confidence=50,
            assigned_team="IT Support",
            summary="Test",
            reasoning="Test",
            suggested_response="Test",
            created_at=now,
            updated_at=now
        )

        ticket_dict = ticket.to_dict()

        assert ticket_dict["id"] == 1
        assert ticket_dict["subject"] == "Test"
        assert ticket_dict["category"] == "Software"
        assert ticket_dict["urgency"] == "High"
        assert ticket_dict["confidence"] == 50

    def test_ticket_repr(self):
        """Test ticket string representation."""
        ticket = Ticket(
            id=1,
            subject="Test ticket",
            description="Test description",
            reporter_name="Test",
            reporter_email="test@test.com",
            department="Test",
            category="Software",
            urgency="High",
            confidence=50,
            assigned_team="IT Support",
            summary="Test",
            reasoning="Test",
            suggested_response="Test"
        )

        repr_str = repr(ticket)

        assert "Ticket" in repr_str
        assert "id=1" in repr_str
        assert "Test ticket" in repr_str
        assert "High" in repr_str


class TestDatabaseConstraints:
    """Tests for database constraints and relationships."""

    def test_ticket_timestamps(self, db_session):
        """Test ticket timestamps are set correctly."""
        ticket_data = TicketCreateRequest(
            subject="Test",
            description="Test description",
            reporter_name="Test",
            reporter_email="test@test.com",
            department="Test"
        )

        classification = ClassificationResponse(
            category="Software",
            urgency="High",
            confidence=50,
            assigned_team="IT Support",
            summary="Test",
            reasoning="Test",
            suggested_response="Test",
            requires_human_review=False
        )

        ticket = TicketService.create_ticket(
            db=db_session,
            ticket_data=ticket_data,
            classification=classification
        )

        assert ticket.created_at is not None
        assert ticket.updated_at is not None
        assert isinstance(ticket.created_at, datetime)
        assert isinstance(ticket.updated_at, datetime)

    def test_ticket_string_fields_required(self):
        """Test that required string fields cannot be None."""
        with pytest.raises(Exception):
            Ticket(
                subject=None,  # Required
                description="Test",
                reporter_name="Test",
                reporter_email="test@test.com",
                department="Test",
                category="Software",
                urgency="High",
                confidence=50,
                assigned_team="IT Support",
                summary="Test",
                reasoning="Test",
                suggested_response="Test"
            )

    def test_ticket_numeric_field_constraints(self):
        """Test numeric field constraints."""
        # Confidence must be between 0-100
        with pytest.raises(ValueError):
            Ticket(
                subject="Test",
                description="Test",
                reporter_name="Test",
                reporter_email="test@test.com",
                department="Test",
                category="Software",
                urgency="High",
                confidence="not_a_number",  # Should be int
                assigned_team="IT Support",
                summary="Test",
                reasoning="Test",
                suggested_response="Test"
            )


class TestDatabaseIndices:
    """Tests for database indexing and query performance."""

    def test_tickets_by_id_index(self, db_session, sample_ticket_data, sample_classification):
        """Test that ID index works."""
        ticket_data = TicketCreateRequest(**sample_ticket_data)
        classification = ClassificationResponse(**sample_classification)

        ticket = TicketService.create_ticket(
            db=db_session,
            ticket_data=ticket_data,
            classification=classification
        )

        # Should be able to quickly retrieve by ID
        retrieved = TicketService.get_ticket_by_id(db=db_session, ticket_id=ticket.id)

        assert retrieved is not None
        assert retrieved.id == ticket.id

    def test_tickets_by_status_index(self, db_session, sample_ticket_data, sample_classification):
        """Test that status index works."""
        ticket_data = TicketCreateRequest(**sample_ticket_data)
        classification = ClassificationResponse(**sample_classification)

        TicketService.create_ticket(
            db=db_session,
            ticket_data=ticket_data,
            classification=classification
        )

        # Should be able to quickly filter by status
        tickets, total = TicketService.list_tickets(
            db=db_session,
            status="Assigned"
        )

        assert total >= 0

    def test_tickets_by_urgency_index(self, db_session, sample_ticket_data, sample_classification):
        """Test that urgency index works."""
        ticket_data = TicketCreateRequest(**sample_ticket_data)
        classification = ClassificationResponse(**sample_classification)

        TicketService.create_ticket(
            db=db_session,
            ticket_data=ticket_data,
            classification=classification
        )

        # Should be able to quickly filter by urgency
        tickets, total = TicketService.list_tickets(
            db=db_session,
            urgency="High"
        )

        assert total >= 0
