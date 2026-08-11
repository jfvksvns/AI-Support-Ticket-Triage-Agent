"""
SQLAlchemy ORM models for the ticket triage database.
Defines the Ticket table and relationships.
"""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates

Base = declarative_base()


class Ticket(Base):
    """
    SQLAlchemy model for support tickets.
    
    Attributes:
        id: Unique ticket identifier
        subject: Brief ticket subject/title
        description: Detailed ticket description
        reporter_name: Name of the person reporting the issue
        reporter_email: Email address of the reporter
        department: Reporter's department
        category: Ticket category (classified by AI)
        urgency: Ticket urgency level (classified by AI)
        confidence: AI confidence score in the classification
        assigned_team: Team assigned to handle the ticket
        summary: AI-generated summary of the issue
        reasoning: AI reasoning for the classification
        suggested_response: Suggested first response from AI
        status: Current ticket status in the system
        requires_human_review: Whether human review was flagged
        created_at: Timestamp when ticket was created
        updated_at: Timestamp when ticket was last updated
    """

    __tablename__ = "tickets"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Ticket information
    subject = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    reporter_name = Column(String(255), nullable=False)
    reporter_email = Column(String(255), nullable=False, index=True)
    department = Column(String(255), nullable=False)

    # AI Classification
    category = Column(String(50), nullable=False, index=True)
    urgency = Column(String(20), nullable=False, index=True)
    confidence = Column(Integer, nullable=False)
    assigned_team = Column(String(100), nullable=False, index=True)

    # AI Generated Content
    summary = Column(Text, nullable=False)
    reasoning = Column(Text, nullable=False)
    suggested_response = Column(Text, nullable=False)

    # Ticket State
    status = Column(String(50), nullable=False, default="Open", index=True)
    requires_human_review = Column(Boolean, nullable=False, default=False)

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    @validates('urgency')
    def validate_urgency(self, key, value):
        """Validate urgency is a valid value."""
        valid_urgencies = ["Low", "Medium", "High", "Critical"]
        if value not in valid_urgencies:
            raise ValueError(f"Invalid urgency: {value}")
        return value

    @validates('category')
    def validate_category(self, key, value):
        """Validate category is a valid value."""
        valid_categories = [
            "Software", "Hardware", "Network", "Security", "Cloud",
            "Database", "Email", "Printer", "Access Management", "Other"
        ]
        if value not in valid_categories:
            raise ValueError(f"Invalid category: {value}")
        return value

    @validates('status')
    def validate_status(self, key, value):
        """Validate status is a valid value."""
        valid_statuses = [
            "Open", "Assigned", "In Progress", 
            "Pending Human Review", "Resolved", "Closed"
        ]
        if value not in valid_statuses:
            raise ValueError(f"Invalid status: {value}")
        return value

    @validates('confidence')
    def validate_confidence(self, key, value):
        """Validate confidence is between 0 and 100."""
        if not isinstance(value, int) or value < 0 or value > 100:
            raise ValueError("Confidence must be an integer between 0 and 100")
        return value

    def __repr__(self) -> str:
        """String representation of the ticket."""
        return f"<Ticket(id={self.id}, subject='{self.subject}', urgency={self.urgency})>"

    def to_dict(self) -> dict:
        """Convert ticket to dictionary."""
        return {
            "id": self.id,
            "subject": self.subject,
            "description": self.description,
            "reporter_name": self.reporter_name,
            "reporter_email": self.reporter_email,
            "department": self.department,
            "category": self.category,
            "urgency": self.urgency,
            "confidence": self.confidence,
            "assigned_team": self.assigned_team,
            "summary": self.summary,
            "reasoning": self.reasoning,
            "suggested_response": self.suggested_response,
            "status": self.status,
            "requires_human_review": self.requires_human_review,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
