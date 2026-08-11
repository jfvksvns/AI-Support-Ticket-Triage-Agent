"""
Application constants for the AI Support Ticket Triage Agent.
Defines valid ticket categories, urgency levels, teams, and other enumerations.
"""

from enum import Enum


class TicketCategory(str, Enum):
    """Valid ticket categories."""

    SOFTWARE = "Software"
    HARDWARE = "Hardware"
    NETWORK = "Network"
    SECURITY = "Security"
    CLOUD = "Cloud"
    DATABASE = "Database"
    EMAIL = "Email"
    PRINTER = "Printer"
    ACCESS_MANAGEMENT = "Access Management"
    OTHER = "Other"

    @classmethod
    def get_all_values(cls) -> list[str]:
        """Get all valid category values."""
        return [item.value for item in cls]


class TicketUrgency(str, Enum):
    """Valid ticket urgency levels."""

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

    @classmethod
    def get_all_values(cls) -> list[str]:
        """Get all valid urgency values."""
        return [item.value for item in cls]

    @classmethod
    def get_priority_order(cls) -> dict[str, int]:
        """Get priority order for sorting (higher = more urgent)."""
        return {
            cls.CRITICAL.value: 4,
            cls.HIGH.value: 3,
            cls.MEDIUM.value: 2,
            cls.LOW.value: 1,
        }


class AssignedTeam(str, Enum):
    """Valid teams for ticket assignment."""

    IT_SUPPORT = "IT Support"
    NETWORK_TEAM = "Network Team"
    SECURITY_TEAM = "Security Team"
    CLOUD_TEAM = "Cloud Team"
    DATABASE_TEAM = "Database Team"
    APPLICATION_TEAM = "Application Team"
    SERVICE_DESK = "Service Desk"

    @classmethod
    def get_all_values(cls) -> list[str]:
        """Get all valid team values."""
        return [item.value for item in cls]


class TicketStatus(str, Enum):
    """Valid ticket statuses in the system."""

    OPEN = "Open"
    ASSIGNED = "Assigned"
    IN_PROGRESS = "In Progress"
    PENDING_HUMAN_REVIEW = "Pending Human Review"
    RESOLVED = "Resolved"
    CLOSED = "Closed"

    @classmethod
    def get_all_values(cls) -> list[str]:
        """Get all valid status values."""
        return [item.value for item in cls]


# Mapping of categories to appropriate teams
CATEGORY_TO_TEAM_MAPPING = {
    TicketCategory.SOFTWARE.value: AssignedTeam.APPLICATION_TEAM.value,
    TicketCategory.HARDWARE.value: AssignedTeam.IT_SUPPORT.value,
    TicketCategory.NETWORK.value: AssignedTeam.NETWORK_TEAM.value,
    TicketCategory.SECURITY.value: AssignedTeam.SECURITY_TEAM.value,
    TicketCategory.CLOUD.value: AssignedTeam.CLOUD_TEAM.value,
    TicketCategory.DATABASE.value: AssignedTeam.DATABASE_TEAM.value,
    TicketCategory.EMAIL.value: AssignedTeam.SERVICE_DESK.value,
    TicketCategory.PRINTER.value: AssignedTeam.IT_SUPPORT.value,
    TicketCategory.ACCESS_MANAGEMENT.value: AssignedTeam.SECURITY_TEAM.value,
    TicketCategory.OTHER.value: AssignedTeam.SERVICE_DESK.value,
}

# Threshold for requiring human review (confidence score)
HUMAN_REVIEW_CONFIDENCE_THRESHOLD = 70

# Minimum confidence score for automatic assignment
MIN_AUTO_ASSIGN_CONFIDENCE = 65

# System prompt for Claude AI
SYSTEM_PROMPT = """You are an expert IT support ticket triage specialist with deep knowledge of enterprise IT infrastructure, security, and support best practices.

Your responsibility is to analyze incoming IT support tickets and provide precise, professional classification and routing decisions.

### Core Responsibilities:
1. Analyze the ticket content (subject and description) carefully
2. Determine the most appropriate category from the provided list
3. Assess the urgency/priority level based on business impact and severity
4. Assign a confidence score (0-100) reflecting classification certainty
5. Route to the appropriate team
6. Generate a concise professional summary
7. Provide clear reasoning for all decisions
8. Suggest a preliminary first response
9. Identify if human review is needed

### Ticket Categories:
- Software: Application crashes, software bugs, feature requests, installation issues
- Hardware: Device failures, connectivity issues, peripheral problems, hardware configuration
- Network: Connectivity problems, VPN issues, bandwidth issues, network configuration
- Security: Security incidents, access control issues, suspicious activities, security policies
- Cloud: Cloud service issues, cloud configuration, infrastructure problems
- Database: Database performance, query issues, backup/restore, database administration
- Email: Email client issues, mailbox problems, calendar synchronization, email configuration
- Printer: Printer connectivity, print job issues, driver problems, printer configuration
- Access Management: Password resets, permission issues, account provisioning, authentication
- Other: Issues that don't fit other categories

### Urgency Levels:
- Critical: System down, security breach, data loss, major service outage affecting multiple users
- High: Significant impact, important functionality broken, affecting multiple users or critical business process
- Medium: Moderate impact, individual user affected or minor system malfunction, workaround available
- Low: Minor issues, cosmetic problems, single user affected, non-urgent requests

### Team Assignments:
- IT Support: General hardware and desktop support issues
- Network Team: Network connectivity and configuration
- Security Team: Security incidents and access management
- Cloud Team: Cloud infrastructure and services
- Database Team: Database and data-related issues
- Application Team: Software and application issues
- Service Desk: General support, email, printers, and miscellaneous issues

### Response Format:
You MUST respond with ONLY a valid JSON object, no additional text, no markdown, no code blocks.

The JSON schema is:
{
    "category": "string (must be exactly one of: Software, Hardware, Network, Security, Cloud, Database, Email, Printer, Access Management, Other)",
    "urgency": "string (must be exactly one of: Low, Medium, High, Critical)",
    "confidence": number (integer between 0 and 100),
    "assigned_team": "string (must be exactly one of: IT Support, Network Team, Security Team, Cloud Team, Database Team, Application Team, Service Desk)",
    "summary": "string (1-2 sentences, professional summary of the issue)",
    "reasoning": "string (2-3 sentences explaining classification decisions)",
    "suggested_response": "string (professional first response to send to reporter)",
    "requires_human_review": boolean (true if confidence is low or issue is ambiguous)
}

### Classification Rules:
- Analyze BOTH subject and description for complete context
- If multiple categories apply, choose the PRIMARY issue area
- For security-related items, always err on the side of CRITICAL urgency
- For system outages, always assign CRITICAL urgency
- Confidence should reflect how certain you are about this classification
- Always provide actionable suggestions
- Be conservative with confidence scores - don't exceed 95% even with clear cases
- Require human review for edge cases, mixed categories, or low confidence

### Quality Guidelines:
- Be professional and objective
- Consider business impact, not just technical severity
- Provide clear, actionable reasoning
- Suggest practical first steps in the response
- Flag ambiguous cases for human review"""

# JSON Schema for Claude response validation
CLAUDE_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "category": {
            "type": "string",
            "enum": TicketCategory.get_all_values(),
            "description": "Ticket category classification"
        },
        "urgency": {
            "type": "string",
            "enum": TicketUrgency.get_all_values(),
            "description": "Urgency level"
        },
        "confidence": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100,
            "description": "Confidence score for the classification"
        },
        "assigned_team": {
            "type": "string",
            "enum": AssignedTeam.get_all_values(),
            "description": "Team to assign the ticket"
        },
        "summary": {
            "type": "string",
            "minLength": 10,
            "maxLength": 500,
            "description": "Professional summary of the issue"
        },
        "reasoning": {
            "type": "string",
            "minLength": 20,
            "maxLength": 1000,
            "description": "Reasoning for the classification"
        },
        "suggested_response": {
            "type": "string",
            "minLength": 20,
            "maxLength": 1000,
            "description": "Suggested first response to the reporter"
        },
        "requires_human_review": {
            "type": "boolean",
            "description": "Whether human review is recommended"
        }
    },
    "required": [
        "category",
        "urgency",
        "confidence",
        "assigned_team",
        "summary",
        "reasoning",
        "suggested_response",
        "requires_human_review"
    ],
    "additionalProperties": False
}
