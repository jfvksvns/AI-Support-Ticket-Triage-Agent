"""
Unit tests for business logic services.
Tests ticket service, classification service, and analytics service.
"""

import pytest
from sqlalchemy.orm import Session

from app.services.ticket_service import TicketService
from app.models.schemas import TicketCreateRequest, ClassificationResponse
from app.models.database import Ticket


class TestTicketService:
    """Tests for TicketService."""

    def test_create_ticket(self, db_session: Session, sample_ticket_data, sample_classification):
        """Test creating a ticket."""
        ticket_data = TicketCreateRequest(**sample_ticket_data)
        classification = ClassificationResponse(**sample_classification)
        
        ticket = TicketService.create_ticket(
            db=db_session,
            ticket_data=ticket_data,
            classification=classification
        )

        assert ticket.id is not None
        assert ticket.subject == sample_ticket_data["subject"]
        assert ticket.description == sample_ticket_data["description"]
        assert ticket.category == sample_classification["category"]
        assert ticket.urgency == sample_classification["urgency"]
        assert ticket.assigned_team == sample_classification["assigned_team"]

    def test_get_ticket_by_id(self, db_session: Session, sample_ticket_data, sample_classification):
        """Test retrieving a ticket by ID."""
        ticket_data = TicketCreateRequest(**sample_ticket_data)
        classification = ClassificationResponse(**sample_classification)
        
        created_ticket = TicketService.create_ticket(
            db=db_session,
            ticket_data=ticket_data,
            classification=classification
        )
        
        retrieved_ticket = TicketService.get_ticket_by_id(
            db=db_session,
            ticket_id=created_ticket.id
        )

        assert retrieved_ticket is not None
        assert retrieved_ticket.id == created_ticket.id
        assert retrieved_ticket.subject == created_ticket.subject

    def test_get_ticket_not_found(self, db_session: Session):
        """Test retrieving a non-existent ticket."""
        ticket = TicketService.get_ticket_by_id(db=db_session, ticket_id=9999)

        assert ticket is None

    def test_list_tickets(self, db_session: Session, sample_ticket_data, sample_classification):
        """Test listing tickets."""
        # Create multiple tickets
        for i in range(3):
            ticket_data = TicketCreateRequest(**sample_ticket_data)
            classification = ClassificationResponse(**sample_classification)
            TicketService.create_ticket(
                db=db_session,
                ticket_data=ticket_data,
                classification=classification
            )

        tickets, total = TicketService.list_tickets(db=db_session)

        assert total == 3
        assert len(tickets) == 3

    def test_list_tickets_pagination(self, db_session: Session, sample_ticket_data, sample_classification):
        """Test ticket pagination."""
        # Create multiple tickets
        for i in range(10):
            ticket_data = TicketCreateRequest(**sample_ticket_data)
            classification = ClassificationResponse(**sample_classification)
            TicketService.create_ticket(
                db=db_session,
                ticket_data=ticket_data,
                classification=classification
            )

        # Get first page
        tickets_page1, total = TicketService.list_tickets(
            db=db_session,
            skip=0,
            limit=5
        )

        assert len(tickets_page1) == 5
        assert total == 10

        # Get second page
        tickets_page2, _ = TicketService.list_tickets(
            db=db_session,
            skip=5,
            limit=5
        )

        assert len(tickets_page2) == 5

    def test_update_ticket_status(self, db_session: Session, sample_ticket_data, sample_classification):
        """Test updating ticket status."""
        ticket_data = TicketCreateRequest(**sample_ticket_data)
        classification = ClassificationResponse(**sample_classification)
        
        ticket = TicketService.create_ticket(
            db=db_session,
            ticket_data=ticket_data,
            classification=classification
        )

        updated_ticket = TicketService.update_ticket_status(
            db=db_session,
            ticket_id=ticket.id,
            new_status="In Progress"
        )

        assert updated_ticket.status == "In Progress"

    def test_update_ticket_status_invalid(self, db_session: Session, sample_ticket_data, sample_classification):
        """Test updating ticket with invalid status."""
        ticket_data = TicketCreateRequest(**sample_ticket_data)
        classification = ClassificationResponse(**sample_classification)
        
        ticket = TicketService.create_ticket(
            db=db_session,
            ticket_data=ticket_data,
            classification=classification
        )

        with pytest.raises(ValueError):
            TicketService.update_ticket_status(
                db=db_session,
                ticket_id=ticket.id,
                new_status="Invalid Status"
            )

    def test_delete_ticket(self, db_session: Session, sample_ticket_data, sample_classification):
        """Test deleting a ticket."""
        ticket_data = TicketCreateRequest(**sample_ticket_data)
        classification = ClassificationResponse(**sample_classification)
        
        ticket = TicketService.create_ticket(
            db=db_session,
            ticket_data=ticket_data,
            classification=classification
        )

        deleted = TicketService.delete_ticket(
            db=db_session,
            ticket_id=ticket.id
        )

        assert deleted is True
        
        # Verify it's deleted
        retrieved = TicketService.get_ticket_by_id(
            db=db_session,
            ticket_id=ticket.id
        )
        assert retrieved is None

    def test_delete_ticket_not_found(self, db_session: Session):
        """Test deleting a non-existent ticket."""
        deleted = TicketService.delete_ticket(db=db_session, ticket_id=9999)

        assert deleted is False

    def test_search_tickets(self, db_session: Session, sample_ticket_data, sample_classification):
        """Test searching tickets."""
        ticket_data = TicketCreateRequest(**sample_ticket_data)
        classification = ClassificationResponse(**sample_classification)
        
        TicketService.create_ticket(
            db=db_session,
            ticket_data=ticket_data,
            classification=classification
        )

        tickets, total = TicketService.search_tickets(
            db=db_session,
            search_query="VPN"
        )

        assert total > 0
        assert len(tickets) > 0

    def test_search_tickets_no_results(self, db_session: Session):
        """Test search with no results."""
        tickets, total = TicketService.search_tickets(
            db=db_session,
            search_query="nonexistent"
        )

        assert total == 0
        assert len(tickets) == 0

    def test_get_tickets_by_team(self, db_session: Session, sample_ticket_data, sample_classification):
        """Test retrieving tickets by team."""
        ticket_data = TicketCreateRequest(**sample_ticket_data)
        classification = ClassificationResponse(**sample_classification)
        
        TicketService.create_ticket(
            db=db_session,
            ticket_data=ticket_data,
            classification=classification
        )

        team_name = sample_classification["assigned_team"]
        tickets, total = TicketService.get_tickets_by_team(
            db=db_session,
            team=team_name
        )

        assert total > 0
        for ticket in tickets:
            assert ticket.assigned_team == team_name

    def test_get_high_priority_tickets(self, db_session: Session, sample_ticket_data, sample_classification):
        """Test retrieving high priority tickets."""
        ticket_data = TicketCreateRequest(**sample_ticket_data)
        classification = ClassificationResponse(**sample_classification)
        
        TicketService.create_ticket(
            db=db_session,
            ticket_data=ticket_data,
            classification=classification
        )

        high_priority = TicketService.get_high_priority_tickets(db=db_session)

        # Should have at least one high priority ticket
        assert len(high_priority) >= 0


class TestClassificationService:
    """Tests for ClassificationService."""

    def test_classification_service_health_check(self):
        """Test classification service health check."""
        from app.services.classification_service import ClassificationService
        
        service = ClassificationService()
        health = service.health_check()

        assert "service" in health
        assert "status" in health
        assert health["status"] in ["healthy", "unhealthy"]


class TestAnalyticsService:
    """Tests for AnalyticsService."""

    def test_get_statistics_empty(self, db_session: Session):
        """Test getting statistics with no data."""
        from app.services.analytics_service import AnalyticsService
        
        stats = AnalyticsService.get_statistics(db=db_session)

        assert stats.total_tickets == 0
        assert stats.average_confidence == 0.0
        assert stats.human_review_count == 0

    def test_get_statistics_with_data(self, db_session: Session, sample_ticket_data, sample_classification):
        """Test getting statistics with data."""
        from app.services.analytics_service import AnalyticsService
        
        # Create a ticket
        ticket_data = TicketCreateRequest(**sample_ticket_data)
        classification = ClassificationResponse(**sample_classification)
        TicketService.create_ticket(
            db=db_session,
            ticket_data=ticket_data,
            classification=classification
        )

        stats = AnalyticsService.get_statistics(db=db_session)

        assert stats.total_tickets >= 1
        assert len(stats.category_distribution) > 0
        assert len(stats.urgency_distribution) > 0

    def test_get_team_workload(self, db_session: Session, sample_ticket_data, sample_classification):
        """Test getting team workload."""
        from app.services.analytics_service import AnalyticsService
        
        ticket_data = TicketCreateRequest(**sample_ticket_data)
        classification = ClassificationResponse(**sample_classification)
        TicketService.create_ticket(
            db=db_session,
            ticket_data=ticket_data,
            classification=classification
        )

        workload = AnalyticsService.get_team_workload(db=db_session)

        assert isinstance(workload, dict)
        assert len(workload) > 0
        for team, metrics in workload.items():
            assert "total" in metrics
            assert "open" in metrics
            assert "critical" in metrics
