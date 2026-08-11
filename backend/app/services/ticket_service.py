"""
Ticket service for CRUD operations and business logic.
Handles ticket creation, retrieval, updating, and deletion from database.
"""

import logging
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import desc, and_

from app.models.database import Ticket
from app.models.schemas import (
    TicketCreateRequest,
    TicketResponse,
    ClassificationResponse
)
from app.core.constants import TicketStatus

logger = logging.getLogger(__name__)


class TicketService:
    """
    Service for managing support tickets in the database.
    
    Provides operations for:
    - Creating new tickets
    - Retrieving tickets (single, list, filtered)
    - Updating ticket information
    - Deleting tickets
    - Querying statistics
    """

    @staticmethod
    def create_ticket(
        db: Session,
        ticket_data: TicketCreateRequest,
        classification: ClassificationResponse
    ) -> Ticket:
        """
        Create a new support ticket with AI classification.
        
        Args:
            db: Database session
            ticket_data: Ticket creation data from request
            classification: AI classification results
            
        Returns:
            Ticket: Created ticket object
            
        Raises:
            Exception: If database operation fails
        """
        try:
            # Determine if human review is needed
            requires_review = classification.requires_human_review
            
            # Determine initial status
            status = TicketStatus.PENDING_HUMAN_REVIEW.value if requires_review else TicketStatus.ASSIGNED.value

            # Create ticket instance
            ticket = Ticket(
                subject=ticket_data.subject,
                description=ticket_data.description,
                reporter_name=ticket_data.reporter_name,
                reporter_email=ticket_data.reporter_email,
                department=ticket_data.department,
                category=classification.category,
                urgency=classification.urgency,
                confidence=classification.confidence,
                assigned_team=classification.assigned_team,
                summary=classification.summary,
                reasoning=classification.reasoning,
                suggested_response=classification.suggested_response,
                status=status,
                requires_human_review=requires_review,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )

            # Add to session and commit
            db.add(ticket)
            db.commit()
            db.refresh(ticket)

            logger.info(f"Created ticket #{ticket.id}: {ticket.subject}")
            return ticket

        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create ticket: {str(e)}")
            raise Exception(f"Failed to create ticket: {str(e)}")

    @staticmethod
    def get_ticket_by_id(db: Session, ticket_id: int) -> Optional[Ticket]:
        """
        Retrieve a ticket by ID.
        
        Args:
            db: Database session
            ticket_id: Ticket ID to retrieve
            
        Returns:
            Optional[Ticket]: Ticket object or None if not found
        """
        try:
            ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
            if not ticket:
                logger.warning(f"Ticket #{ticket_id} not found")
            return ticket
        except Exception as e:
            logger.error(f"Error retrieving ticket #{ticket_id}: {str(e)}")
            raise Exception(f"Failed to retrieve ticket: {str(e)}")

    @staticmethod
    def list_tickets(
        db: Session,
        skip: int = 0,
        limit: int = 50,
        urgency: Optional[str] = None,
        category: Optional[str] = None,
        status: Optional[str] = None,
        requires_review: Optional[bool] = None
    ) -> tuple[List[Ticket], int]:
        """
        List tickets with optional filtering and pagination.
        
        Args:
            db: Database session
            skip: Number of items to skip (for pagination)
            limit: Maximum items to return
            urgency: Filter by urgency level (optional)
            category: Filter by category (optional)
            status: Filter by status (optional)
            requires_review: Filter by human review flag (optional)
            
        Returns:
            tuple: (list of tickets, total count)
        """
        try:
            query = db.query(Ticket)

            # Apply filters
            filters = []
            if urgency:
                filters.append(Ticket.urgency == urgency)
            if category:
                filters.append(Ticket.category == category)
            if status:
                filters.append(Ticket.status == status)
            if requires_review is not None:
                filters.append(Ticket.requires_human_review == requires_review)

            if filters:
                query = query.filter(and_(*filters))

            # Get total count before pagination
            total = query.count()

            # Apply pagination and ordering
            tickets = query.order_by(
                desc(Ticket.created_at)
            ).offset(skip).limit(limit).all()

            return tickets, total

        except Exception as e:
            logger.error(f"Error listing tickets: {str(e)}")
            raise Exception(f"Failed to list tickets: {str(e)}")

    @staticmethod
    def update_ticket_status(
        db: Session,
        ticket_id: int,
        new_status: str
    ) -> Optional[Ticket]:
        """
        Update a ticket's status.
        
        Args:
            db: Database session
            ticket_id: Ticket ID to update
            new_status: New status value
            
        Returns:
            Optional[Ticket]: Updated ticket or None if not found
            
        Raises:
            ValueError: If status is invalid
        """
        try:
            # Validate status
            valid_statuses = [status.value for status in TicketStatus]
            if new_status not in valid_statuses:
                raise ValueError(f"Invalid status: {new_status}")

            ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
            if not ticket:
                logger.warning(f"Ticket #{ticket_id} not found for status update")
                return None

            ticket.status = new_status
            ticket.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(ticket)

            logger.info(f"Updated ticket #{ticket_id} status to {new_status}")
            return ticket

        except Exception as e:
            db.rollback()
            logger.error(f"Failed to update ticket status: {str(e)}")
            raise Exception(f"Failed to update ticket status: {str(e)}")

    @staticmethod
    def delete_ticket(db: Session, ticket_id: int) -> bool:
        """
        Delete a ticket from the database.
        
        Args:
            db: Database session
            ticket_id: Ticket ID to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        try:
            ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
            if not ticket:
                logger.warning(f"Ticket #{ticket_id} not found for deletion")
                return False

            db.delete(ticket)
            db.commit()

            logger.info(f"Deleted ticket #{ticket_id}")
            return True

        except Exception as e:
            db.rollback()
            logger.error(f"Failed to delete ticket: {str(e)}")
            raise Exception(f"Failed to delete ticket: {str(e)}")

    @staticmethod
    def search_tickets(
        db: Session,
        search_query: str,
        skip: int = 0,
        limit: int = 50
    ) -> tuple[List[Ticket], int]:
        """
        Search tickets by subject or description.
        
        Args:
            db: Database session
            search_query: Search term to find in subject or description
            skip: Number of items to skip
            limit: Maximum items to return
            
        Returns:
            tuple: (list of matching tickets, total count)
        """
        try:
            from sqlalchemy import or_

            # Search in subject and description (case-insensitive)
            query = db.query(Ticket).filter(
                or_(
                    Ticket.subject.ilike(f"%{search_query}%"),
                    Ticket.description.ilike(f"%{search_query}%")
                )
            )

            total = query.count()
            tickets = query.order_by(
                desc(Ticket.created_at)
            ).offset(skip).limit(limit).all()

            return tickets, total

        except Exception as e:
            logger.error(f"Error searching tickets: {str(e)}")
            raise Exception(f"Failed to search tickets: {str(e)}")

    @staticmethod
    def get_tickets_by_team(
        db: Session,
        team: str,
        skip: int = 0,
        limit: int = 50
    ) -> tuple[List[Ticket], int]:
        """
        Get all tickets assigned to a specific team.
        
        Args:
            db: Database session
            team: Team name to filter by
            skip: Number of items to skip
            limit: Maximum items to return
            
        Returns:
            tuple: (list of tickets, total count)
        """
        try:
            query = db.query(Ticket).filter(Ticket.assigned_team == team)
            total = query.count()
            tickets = query.order_by(
                desc(Ticket.urgency),
                desc(Ticket.created_at)
            ).offset(skip).limit(limit).all()

            return tickets, total

        except Exception as e:
            logger.error(f"Error retrieving team tickets: {str(e)}")
            raise Exception(f"Failed to retrieve team tickets: {str(e)}")

    @staticmethod
    def get_high_priority_tickets(
        db: Session,
        limit: int = 20
    ) -> List[Ticket]:
        """
        Get recent high priority and critical tickets.
        
        Args:
            db: Database session
            limit: Maximum number of tickets to return
            
        Returns:
            List[Ticket]: List of high priority tickets
        """
        try:
            from sqlalchemy import or_

            tickets = db.query(Ticket).filter(
                or_(
                    Ticket.urgency == "Critical",
                    Ticket.urgency == "High"
                )
            ).order_by(
                desc(Ticket.created_at)
            ).limit(limit).all()

            return tickets

        except Exception as e:
            logger.error(f"Error retrieving high priority tickets: {str(e)}")
            return []
