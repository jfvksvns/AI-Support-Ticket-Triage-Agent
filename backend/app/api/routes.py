"""
FastAPI route handlers for the Support Ticket Triage Agent API.
Defines all endpoints for ticket management, classification, and analytics.
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import (
    verify_api_key,
    get_classification_service,
    get_analytics_service,
    get_db
)
from app.models.schemas import (
    TicketCreateRequest,
    TicketResponse,
    TicketListResponse,
    ClassifyRequest,
    ClassifyResponse,
    StatisticsResponse,
    HealthResponse,
    UpdateTicketStatusRequest,
    ErrorResponse
)
from app.services.classification_service import ClassificationService
from app.services.analytics_service import AnalyticsService
from app.services.ticket_service import TicketService
from app.core.config import get_settings
from app.database.engine import DatabaseEngine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["tickets"])


# ==================== Ticket Classification Endpoints ====================

@router.post(
    "/classify",
    response_model=ClassifyResponse,
    status_code=status.HTTP_200_OK,
    summary="Classify a ticket",
    description="Classify a ticket without creating it in the database. Returns classification results only."
)
async def classify_ticket(
    request: ClassifyRequest,
    api_key: Optional[str] = Depends(verify_api_key),
    classification_service: ClassificationService = Depends(get_classification_service)
) -> ClassifyResponse:
    """
    Classify a support ticket using AI without saving it.
    
    This endpoint is useful for previewing classification results before
    creating a ticket. The ticket is NOT saved to the database.
    
    Args:
        request: Ticket data to classify (subject and description)
        api_key: API key for authentication (if required)
        classification_service: Classification service dependency
        
    Returns:
        ClassifyResponse: Classification results
        
    Raises:
        HTTPException: If classification fails
    """
    try:
        logger.info(f"Classifying ticket: {request.subject[:50]}")
        
        classification = classification_service.classify_only(
            subject=request.subject,
            description=request.description
        )
        
        return ClassifyResponse(classification=classification)
        
    except Exception as e:
        logger.error(f"Classification failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Classification failed: {str(e)}"
        )


# ==================== Ticket CRUD Endpoints ====================

@router.post(
    "/tickets",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new ticket",
    description="Submit a new support ticket. Automatically classifies using AI and saves to database."
)
async def create_ticket(
    request: TicketCreateRequest,
    api_key: Optional[str] = Depends(verify_api_key),
    classification_service: ClassificationService = Depends(get_classification_service),
    db: Session = Depends(get_db)
) -> TicketResponse:
    """
    Create a new support ticket with AI classification.
    
    The ticket is automatically classified using the AI agent, stored in the database,
    and returned with all classification results.
    
    Args:
        request: Ticket creation data
        api_key: API key for authentication (if required)
        classification_service: Classification service dependency
        db: Database session dependency
        
    Returns:
        TicketResponse: Created ticket with classification
        
    Raises:
        HTTPException: If ticket creation or classification fails
    """
    try:
        logger.info(f"Creating ticket: {request.subject}")
        
        ticket = classification_service.process_ticket(
            db=db,
            ticket_data=request
        )
        
        logger.info(f"Successfully created ticket #{ticket.id}")
        return ticket
        
    except Exception as e:
        logger.error(f"Failed to create ticket: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create ticket: {str(e)}"
        )


@router.get(
    "/tickets",
    response_model=TicketListResponse,
    status_code=status.HTTP_200_OK,
    summary="List all tickets",
    description="Retrieve a paginated list of tickets with optional filtering."
)
async def list_tickets(
    skip: int = Query(0, ge=0, description="Number of tickets to skip"),
    limit: int = Query(50, ge=1, le=100, description="Maximum tickets to return"),
    urgency: Optional[str] = Query(None, description="Filter by urgency level"),
    category: Optional[str] = Query(None, description="Filter by category"),
    status: Optional[str] = Query(None, description="Filter by status"),
    requires_review: Optional[bool] = Query(None, description="Filter by human review flag"),
    api_key: Optional[str] = Depends(verify_api_key),
    db: Session = Depends(get_db)
) -> TicketListResponse:
    """
    Retrieve a paginated list of tickets with optional filters.
    
    Supports filtering by:
    - Urgency level (Low, Medium, High, Critical)
    - Category (Software, Hardware, Network, etc.)
    - Status (Open, Assigned, In Progress, etc.)
    - Human review flag
    
    Args:
        skip: Number of tickets to skip (for pagination)
        limit: Maximum number of tickets to return (max 100)
        urgency: Optional urgency filter
        category: Optional category filter
        status: Optional status filter
        requires_review: Optional human review flag filter
        api_key: API key for authentication (if required)
        db: Database session dependency
        
    Returns:
        TicketListResponse: List of tickets with pagination info
        
    Raises:
        HTTPException: If query fails
    """
    try:
        logger.debug(f"Listing tickets: skip={skip}, limit={limit}")
        
        tickets, total = TicketService.list_tickets(
            db=db,
            skip=skip,
            limit=limit,
            urgency=urgency,
            category=category,
            status=status,
            requires_review=requires_review
        )
        
        return TicketListResponse(
            items=[TicketResponse.model_validate(t) for t in tickets],
            total=total,
            skip=skip,
            limit=limit
        )
        
    except Exception as e:
        logger.error(f"Failed to list tickets: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve tickets: {str(e)}"
        )


@router.get(
    "/tickets/{ticket_id}",
    response_model=TicketResponse,
    status_code=status.HTTP_200_OK,
    summary="Get ticket details",
    description="Retrieve detailed information about a specific ticket."
)
async def get_ticket(
    ticket_id: int,
    api_key: Optional[str] = Depends(verify_api_key),
    db: Session = Depends(get_db)
) -> TicketResponse:
    """
    Retrieve detailed information about a specific ticket.
    
    Args:
        ticket_id: ID of the ticket to retrieve
        api_key: API key for authentication (if required)
        db: Database session dependency
        
    Returns:
        TicketResponse: Ticket details
        
    Raises:
        HTTPException: If ticket not found
    """
    try:
        logger.debug(f"Retrieving ticket #{ticket_id}")
        
        ticket = TicketService.get_ticket_by_id(db=db, ticket_id=ticket_id)
        
        if not ticket:
            logger.warning(f"Ticket #{ticket_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket #{ticket_id} not found"
            )
        
        return TicketResponse.model_validate(ticket)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve ticket: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve ticket: {str(e)}"
        )


@router.patch(
    "/tickets/{ticket_id}/status",
    response_model=TicketResponse,
    status_code=status.HTTP_200_OK,
    summary="Update ticket status",
    description="Update the status of a ticket."
)
async def update_ticket_status(
    ticket_id: int,
    request: UpdateTicketStatusRequest,
    api_key: Optional[str] = Depends(verify_api_key),
    db: Session = Depends(get_db)
) -> TicketResponse:
    """
    Update the status of a specific ticket.
    
    Valid statuses: Open, Assigned, In Progress, Pending Human Review, Resolved, Closed
    
    Args:
        ticket_id: ID of the ticket to update
        request: New status value
        api_key: API key for authentication (if required)
        db: Database session dependency
        
    Returns:
        TicketResponse: Updated ticket
        
    Raises:
        HTTPException: If ticket not found or status is invalid
    """
    try:
        logger.info(f"Updating ticket #{ticket_id} status to {request.status}")
        
        ticket = TicketService.update_ticket_status(
            db=db,
            ticket_id=ticket_id,
            new_status=request.status
        )
        
        if not ticket:
            logger.warning(f"Ticket #{ticket_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket #{ticket_id} not found"
            )
        
        return TicketResponse.model_validate(ticket)
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Invalid status value: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to update ticket status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update ticket: {str(e)}"
        )


@router.delete(
    "/tickets/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a ticket",
    description="Delete a ticket from the system."
)
async def delete_ticket(
    ticket_id: int,
    api_key: Optional[str] = Depends(verify_api_key),
    db: Session = Depends(get_db)
) -> None:
    """
    Delete a ticket from the database.
    
    Args:
        ticket_id: ID of the ticket to delete
        api_key: API key for authentication (if required)
        db: Database session dependency
        
    Raises:
        HTTPException: If ticket not found
    """
    try:
        logger.info(f"Deleting ticket #{ticket_id}")
        
        deleted = TicketService.delete_ticket(db=db, ticket_id=ticket_id)
        
        if not deleted:
            logger.warning(f"Ticket #{ticket_id} not found for deletion")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket #{ticket_id} not found"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete ticket: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete ticket: {str(e)}"
        )


# ==================== Analytics Endpoints ====================

@router.get(
    "/statistics",
    response_model=StatisticsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get ticket statistics",
    description="Retrieve comprehensive statistics and metrics for all tickets."
)
async def get_statistics(
    api_key: Optional[str] = Depends(verify_api_key),
    analytics_service: AnalyticsService = Depends(get_analytics_service),
    db: Session = Depends(get_db)
) -> StatisticsResponse:
    """
    Retrieve comprehensive statistics for the dashboard.
    
    Includes:
    - Total ticket counts by urgency
    - Average confidence score
    - Human review counts
    - Distributions by category, team, and status
    
    Args:
        api_key: API key for authentication (if required)
        analytics_service: Analytics service dependency
        db: Database session dependency
        
    Returns:
        StatisticsResponse: Complete statistics object
    """
    try:
        logger.debug("Retrieving ticket statistics")
        
        stats = analytics_service.get_statistics(db=db)
        return stats
        
    except Exception as e:
        logger.error(f"Failed to retrieve statistics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve statistics: {str(e)}"
        )


# ==================== Health & Status Endpoints ====================

@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check the health and status of the API and dependencies."
)
async def health_check(
    classification_service: ClassificationService = Depends(get_classification_service)
) -> HealthResponse:
    """
    Check the health of the API and all dependencies.
    
    Tests:
    - Database connectivity
    - Claude AI API connectivity
    
    Returns:
        HealthResponse: Health status of all components
    """
    try:
        settings = get_settings()
        
        # Check database
        db_healthy = DatabaseEngine.health_check()
        db_status = "healthy" if db_healthy else "unhealthy"
        
        # Check AI service
        ai_health = classification_service.health_check()
        ai_status = ai_health.get("status", "unhealthy")
        
        # Overall status
        overall_status = "healthy" if (db_healthy and ai_status == "healthy") else "degraded"
        
        return HealthResponse(
            status=overall_status,
            version=settings.APP_VERSION,
            database=db_status,
            ai_service=ai_status
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            version=get_settings().APP_VERSION,
            database="unhealthy",
            ai_service="unhealthy"
        )
