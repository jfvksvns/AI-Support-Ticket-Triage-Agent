"""
Classification service that coordinates AI agent classification with ticket creation.
Handles the complete flow from ticket data to AI classification to database storage.
"""

import logging
from typing import Optional

from sqlalchemy.orm import Session

from app.models.schemas import (
    TicketCreateRequest,
    ClassificationResponse,
    TicketResponse
)
from app.models.database import Ticket
from app.services.ai_agent import AIAgentService
from app.services.ticket_service import TicketService
from app.core.constants import HUMAN_REVIEW_CONFIDENCE_THRESHOLD

logger = logging.getLogger(__name__)


class ClassificationService:
    """
    Orchestrates the complete ticket classification workflow.
    
    Coordinates:
    - AI classification via Claude
    - Ticket creation in database
    - Human review flagging
    - Response generation
    """

    def __init__(self):
        """Initialize the classification service with AI agent."""
        self.ai_agent = AIAgentService()
        self.ticket_service = TicketService

    def process_ticket(
        self,
        db: Session,
        ticket_data: TicketCreateRequest
    ) -> TicketResponse:
        """
        Complete ticket processing workflow:
        1. Classify ticket using AI
        2. Flag for human review if needed
        3. Create ticket in database
        4. Return ticket response
        
        Args:
            db: Database session
            ticket_data: Incoming ticket data
            
        Returns:
            TicketResponse: Created ticket with classification
            
        Raises:
            Exception: If classification or database operations fail
        """
        try:
            logger.info(f"Starting ticket processing for: {ticket_data.subject}")

            # Step 1: Get AI classification
            classification = self.ai_agent.classify_ticket(
                subject=ticket_data.subject,
                description=ticket_data.description,
                reporter_name=ticket_data.reporter_name,
                department=ticket_data.department
            )

            # Step 2: Check if human review is needed based on confidence
            if classification.confidence < HUMAN_REVIEW_CONFIDENCE_THRESHOLD:
                classification.requires_human_review = True
                logger.warning(
                    f"Low confidence ({classification.confidence}) - flagging for human review"
                )

            # Step 3: Create ticket in database
            ticket = self.ticket_service.create_ticket(
                db=db,
                ticket_data=ticket_data,
                classification=classification
            )

            # Step 4: Convert to response
            response = TicketResponse.model_validate(ticket)
            logger.info(f"Successfully processed ticket #{ticket.id}")

            return response

        except Exception as e:
            logger.error(f"Ticket processing failed: {str(e)}")
            raise Exception(f"Failed to process ticket: {str(e)}")

    def classify_only(
        self,
        subject: str,
        description: str,
        reporter_name: Optional[str] = None,
        department: Optional[str] = None
    ) -> ClassificationResponse:
        """
        Perform classification without creating a ticket.
        Useful for preview/testing of classification.
        
        Args:
            subject: Ticket subject
            description: Ticket description
            reporter_name: Optional reporter name
            department: Optional department
            
        Returns:
            ClassificationResponse: Classification results only
        """
        try:
            logger.debug("Performing classification without ticket creation")
            
            classification = self.ai_agent.classify_ticket(
                subject=subject,
                description=description,
                reporter_name=reporter_name,
                department=department
            )

            # Check confidence threshold
            if classification.confidence < HUMAN_REVIEW_CONFIDENCE_THRESHOLD:
                classification.requires_human_review = True

            return classification

        except Exception as e:
            logger.error(f"Classification failed: {str(e)}")
            raise Exception(f"Failed to classify: {str(e)}")

    def reprocess_ticket_classification(
        self,
        db: Session,
        ticket_id: int
    ) -> Optional[TicketResponse]:
        """
        Rerun AI classification on an existing ticket.
        Updates the ticket with new classification results.
        
        Args:
            db: Database session
            ticket_id: ID of ticket to reprocess
            
        Returns:
            Optional[TicketResponse]: Updated ticket or None if not found
        """
        try:
            # Retrieve existing ticket
            ticket = self.ticket_service.get_ticket_by_id(db, ticket_id)
            if not ticket:
                logger.warning(f"Cannot reprocess: ticket #{ticket_id} not found")
                return None

            logger.info(f"Reprocessing ticket #{ticket_id} classification")

            # Re-classify
            classification = self.ai_agent.classify_ticket(
                subject=ticket.subject,
                description=ticket.description,
                reporter_name=ticket.reporter_name,
                department=ticket.department
            )

            # Check confidence threshold
            if classification.confidence < HUMAN_REVIEW_CONFIDENCE_THRESHOLD:
                classification.requires_human_review = True

            # Update ticket fields
            ticket.category = classification.category
            ticket.urgency = classification.urgency
            ticket.confidence = classification.confidence
            ticket.assigned_team = classification.assigned_team
            ticket.summary = classification.summary
            ticket.reasoning = classification.reasoning
            ticket.suggested_response = classification.suggested_response
            ticket.requires_human_review = classification.requires_human_review

            db.commit()
            db.refresh(ticket)

            response = TicketResponse.model_validate(ticket)
            logger.info(f"Successfully reprocessed ticket #{ticket_id}")

            return response

        except Exception as e:
            db.rollback()
            logger.error(f"Failed to reprocess ticket classification: {str(e)}")
            raise Exception(f"Failed to reprocess classification: {str(e)}")

    def health_check(self) -> dict:
        """
        Check health of classification service and AI agent.
        
        Returns:
            dict: Health status of AI service
        """
        ai_healthy = self.ai_agent.health_check()
        return {
            "service": "classification",
            "status": "healthy" if ai_healthy else "unhealthy",
            "ai_agent": "healthy" if ai_healthy else "unhealthy"
        }
