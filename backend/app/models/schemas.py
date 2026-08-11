"""
Pydantic models for request and response validation.
Defines API contract schemas with strict type checking.
"""

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, EmailStr, field_validator


class TicketCreateRequest(BaseModel):
    """
    Schema for creating a new support ticket.
    
    Attributes:
        subject: Brief description of the issue (required)
        description: Detailed description of the problem (required)
        reporter_name: Name of the person reporting (required)
        reporter_email: Email address of the reporter (required)
        department: Department of the reporter (required)
    """

    subject: str = Field(
        ...,
        min_length=5,
        max_length=255,
        description="Ticket subject line"
    )
    description: str = Field(
        ...,
        min_length=20,
        max_length=5000,
        description="Detailed ticket description"
    )
    reporter_name: str = Field(
        ...,
        min_length=2,
        max_length=255,
        description="Reporter's full name"
    )
    reporter_email: EmailStr = Field(
        ...,
        description="Reporter's email address"
    )
    department: str = Field(
        ...,
        min_length=2,
        max_length=255,
        description="Reporter's department"
    )

    @field_validator("subject", "description", "reporter_name", "department")
    @classmethod
    def strip_whitespace(cls, v):
        """Strip leading/trailing whitespace."""
        if isinstance(v, str):
            return v.strip()
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "subject": "Cannot connect to VPN",
                "description": "I've been unable to connect to the company VPN for the past 2 hours. I've restarted my machine and the VPN client. Error code: 1234",
                "reporter_name": "John Doe",
                "reporter_email": "john.doe@company.com",
                "department": "Sales"
            }
        }
    }


class ClassificationResponse(BaseModel):
    """
    Schema for AI classification response from Claude.
    
    Attributes:
        category: Ticket category classification
        urgency: Urgency level classification
        confidence: Confidence score (0-100)
        assigned_team: Team assignment
        summary: AI-generated summary
        reasoning: Classification reasoning
        suggested_response: Suggested first response
        requires_human_review: Whether human review is needed
    """

    category: str = Field(
        ...,
        description="Ticket category"
    )
    urgency: str = Field(
        ...,
        description="Urgency level"
    )
    confidence: int = Field(
        ...,
        ge=0,
        le=100,
        description="Confidence score"
    )
    assigned_team: str = Field(
        ...,
        description="Assigned team"
    )
    summary: str = Field(
        ...,
        description="Issue summary"
    )
    reasoning: str = Field(
        ...,
        description="Classification reasoning"
    )
    suggested_response: str = Field(
        ...,
        description="Suggested first response"
    )
    requires_human_review: bool = Field(
        ...,
        description="Whether human review is needed"
    )


class TicketResponse(BaseModel):
    """
    Schema for ticket response from database.
    
    Attributes:
        id: Unique ticket identifier
        subject: Ticket subject
        description: Ticket description
        reporter_name: Reporter's name
        reporter_email: Reporter's email
        department: Reporter's department
        category: Classified category
        urgency: Assigned urgency
        confidence: Confidence score
        assigned_team: Assigned team
        summary: AI summary
        reasoning: Classification reasoning
        suggested_response: Suggested response
        status: Current ticket status
        requires_human_review: Human review flag
        created_at: Creation timestamp
        updated_at: Update timestamp
    """

    id: int
    subject: str
    description: str
    reporter_name: str
    reporter_email: str
    department: str
    category: str
    urgency: str
    confidence: int
    assigned_team: str
    summary: str
    reasoning: str
    suggested_response: str
    status: str
    requires_human_review: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TicketDetailResponse(TicketResponse):
    """Extended ticket response with additional metadata."""

    pass


class TicketListResponse(BaseModel):
    """
    Schema for list of tickets.
    
    Attributes:
        items: List of ticket objects
        total: Total number of tickets
        skip: Number of items skipped
        limit: Maximum items returned
    """

    items: List[TicketResponse]
    total: int
    skip: int
    limit: int


class ClassifyRequest(BaseModel):
    """
    Request schema for classification endpoint.
    
    Attributes:
        subject: Ticket subject
        description: Ticket description
    """

    subject: str = Field(
        ...,
        min_length=5,
        max_length=255,
        description="Ticket subject"
    )
    description: str = Field(
        ...,
        min_length=20,
        max_length=5000,
        description="Ticket description"
    )


class ClassifyResponse(BaseModel):
    """
    Response schema for classification endpoint.
    
    Attributes:
        classification: AI classification results
        ticket_id: Created ticket ID (if saved)
    """

    classification: ClassificationResponse
    ticket_id: Optional[int] = None


class StatisticsResponse(BaseModel):
    """
    Schema for statistics dashboard data.
    
    Attributes:
        total_tickets: Total number of tickets
        critical_tickets: Number of critical urgency tickets
        high_tickets: Number of high urgency tickets
        medium_tickets: Number of medium urgency tickets
        low_tickets: Number of low urgency tickets
        average_confidence: Average confidence score
        human_review_count: Number of tickets flagged for review
        category_distribution: Count by category
        urgency_distribution: Count by urgency
        team_distribution: Count by assigned team
        status_distribution: Count by status
    """

    total_tickets: int
    critical_tickets: int
    high_tickets: int
    medium_tickets: int
    low_tickets: int
    average_confidence: float
    human_review_count: int
    category_distribution: dict
    urgency_distribution: dict
    team_distribution: dict
    status_distribution: dict


class HealthResponse(BaseModel):
    """
    Schema for health check endpoint.
    
    Attributes:
        status: Health status
        version: Application version
        database: Database connection status
        ai_service: AI service status
    """

    status: str = Field(
        ...,
        description="Overall health status"
    )
    version: str = Field(
        ...,
        description="Application version"
    )
    database: str = Field(
        ...,
        description="Database status"
    )
    ai_service: str = Field(
        ...,
        description="AI service status"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Health check timestamp"
    )


class ErrorResponse(BaseModel):
    """
    Schema for error responses.
    
    Attributes:
        detail: Error message
        error_code: Error code for categorization
        timestamp: When the error occurred
    """

    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Error timestamp"
    )


class UpdateTicketStatusRequest(BaseModel):
    """
    Schema for updating ticket status.
    
    Attributes:
        status: New ticket status
    """

    status: str = Field(
        ...,
        description="New ticket status"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "In Progress"
            }
        }
    }
