"""
AI Agent service that integrates with the Anthropic Claude API.
Handles ticket classification and AI-powered ticket processing.
"""

import json
import logging
from typing import Optional, Dict, Any

import anthropic

from app.core.config import get_settings
from app.core.constants import SYSTEM_PROMPT, CLAUDE_RESPONSE_SCHEMA
from app.models.schemas import ClassificationResponse

logger = logging.getLogger(__name__)


class AIAgentService:
    """
    Service for AI-powered ticket classification using Claude API.
    
    Handles:
    - Connecting to Claude API
    - Sending ticket information for classification
    - Parsing and validating AI responses
    - Error handling and retry logic
    """

    def __init__(self):
        """Initialize the AI Agent service with Claude API credentials."""
        settings = get_settings()
        self.api_key = settings.CLAUDE_API_KEY
        self.model = settings.CLAUDE_MODEL
        self.max_tokens = settings.CLAUDE_MAX_TOKENS
        self.timeout = settings.CLAUDE_TIMEOUT
        
        # Initialize Anthropic client
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def classify_ticket(
        self,
        subject: str,
        description: str,
        reporter_name: Optional[str] = None,
        department: Optional[str] = None
    ) -> ClassificationResponse:
        """
        Classify a support ticket using Claude AI.
        
        Analyzes the ticket subject and description to:
        - Determine the category
        - Assign urgency level
        - Generate confidence score
        - Route to appropriate team
        - Provide reasoning and suggestions
        
        Args:
            subject: Ticket subject line
            description: Detailed ticket description
            reporter_name: Optional reporter name for context
            department: Optional reporter department for context
            
        Returns:
            ClassificationResponse: AI classification results
            
        Raises:
            ValueError: If API response is invalid or malformed
            Exception: If API call fails or times out
        """
        try:
            # Build the user prompt with ticket information
            user_prompt = self._build_user_prompt(
                subject=subject,
                description=description,
                reporter_name=reporter_name,
                department=department
            )

            logger.debug(f"Sending classification request to Claude API (model: {self.model})")

            # Call Claude API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=SYSTEM_PROMPT,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                timeout=self.timeout
            )

            # Extract response text
            response_text = message.content[0].text if message.content else ""
            
            # Parse and validate JSON response
            classification = self._parse_response(response_text)
            
            logger.info(
                f"Successfully classified ticket: "
                f"category={classification.category}, "
                f"urgency={classification.urgency}, "
                f"confidence={classification.confidence}"
            )

            return classification

        except anthropic.APIError as e:
            logger.error(f"Claude API error: {str(e)}")
            raise Exception(f"Failed to classify ticket: {str(e)}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response from Claude: {str(e)}")
            raise ValueError(f"Invalid AI response format: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during classification: {str(e)}")
            raise Exception(f"Classification failed: {str(e)}")

    def _build_user_prompt(
        self,
        subject: str,
        description: str,
        reporter_name: Optional[str] = None,
        department: Optional[str] = None
    ) -> str:
        """
        Build the user prompt for Claude classification.
        
        Args:
            subject: Ticket subject
            description: Ticket description
            reporter_name: Optional reporter name
            department: Optional department
            
        Returns:
            str: Formatted prompt for Claude
        """
        prompt_parts = [
            "=== SUPPORT TICKET TO CLASSIFY ===\n"
        ]

        if reporter_name:
            prompt_parts.append(f"Reporter: {reporter_name}\n")
        
        if department:
            prompt_parts.append(f"Department: {department}\n")

        prompt_parts.extend([
            f"\nSubject: {subject}\n",
            f"\nDescription:\n{description}\n",
            "\n=== PROVIDE CLASSIFICATION IN JSON FORMAT ===\n",
            "Respond with ONLY a valid JSON object, no additional text or markdown."
        ])

        return "".join(prompt_parts)

    def _parse_response(self, response_text: str) -> ClassificationResponse:
        """
        Parse and validate Claude's JSON response.
        
        Extracts JSON from the response, validates against schema,
        and returns a ClassificationResponse object.
        
        Args:
            response_text: Raw text response from Claude
            
        Returns:
            ClassificationResponse: Parsed and validated response
            
        Raises:
            ValueError: If response is invalid or doesn't match schema
        """
        # Clean response text (remove markdown code blocks if present)
        response_text = response_text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()

        # Parse JSON
        try:
            response_dict = json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {response_text[:200]}")
            raise ValueError(f"Invalid JSON in AI response: {str(e)}")

        # Validate required fields
        required_fields = [
            "category", "urgency", "confidence", "assigned_team",
            "summary", "reasoning", "suggested_response", "requires_human_review"
        ]
        
        missing_fields = [f for f in required_fields if f not in response_dict]
        if missing_fields:
            raise ValueError(f"Missing required fields in response: {missing_fields}")

        # Validate field values
        self._validate_response_values(response_dict)

        # Create and return response object
        try:
            return ClassificationResponse(**response_dict)
        except Exception as e:
            logger.error(f"Failed to create ClassificationResponse: {str(e)}")
            raise ValueError(f"Invalid response values: {str(e)}")

    def _validate_response_values(self, response_dict: Dict[str, Any]) -> None:
        """
        Validate individual response field values.
        
        Args:
            response_dict: Response dictionary to validate
            
        Raises:
            ValueError: If any field has invalid values
        """
        # Valid categories
        valid_categories = [
            "Software", "Hardware", "Network", "Security", "Cloud",
            "Database", "Email", "Printer", "Access Management", "Other"
        ]
        if response_dict.get("category") not in valid_categories:
            raise ValueError(
                f"Invalid category: {response_dict.get('category')}. "
                f"Must be one of: {', '.join(valid_categories)}"
            )

        # Valid urgencies
        valid_urgencies = ["Low", "Medium", "High", "Critical"]
        if response_dict.get("urgency") not in valid_urgencies:
            raise ValueError(
                f"Invalid urgency: {response_dict.get('urgency')}. "
                f"Must be one of: {', '.join(valid_urgencies)}"
            )

        # Valid teams
        valid_teams = [
            "IT Support", "Network Team", "Security Team", "Cloud Team",
            "Database Team", "Application Team", "Service Desk"
        ]
        if response_dict.get("assigned_team") not in valid_teams:
            raise ValueError(
                f"Invalid assigned_team: {response_dict.get('assigned_team')}. "
                f"Must be one of: {', '.join(valid_teams)}"
            )

        # Confidence must be 0-100
        confidence = response_dict.get("confidence")
        if not isinstance(confidence, int) or confidence < 0 or confidence > 100:
            raise ValueError(
                f"Invalid confidence: {confidence}. Must be integer between 0 and 100"
            )

        # Boolean validation
        if not isinstance(response_dict.get("requires_human_review"), bool):
            raise ValueError(
                f"Invalid requires_human_review: must be boolean"
            )

        # String length validation
        if len(response_dict.get("summary", "")) < 10:
            raise ValueError("Summary must be at least 10 characters")
        if len(response_dict.get("reasoning", "")) < 20:
            raise ValueError("Reasoning must be at least 20 characters")
        if len(response_dict.get("suggested_response", "")) < 20:
            raise ValueError("Suggested response must be at least 20 characters")

    def health_check(self) -> bool:
        """
        Check if Claude API is accessible and responsive.
        
        Returns:
            bool: True if API is healthy, False otherwise
        """
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=100,
                messages=[
                    {
                        "role": "user",
                        "content": "Respond with 'OK' if you receive this message."
                    }
                ],
                timeout=self.timeout
            )
            return bool(message.content)
        except Exception as e:
            logger.error(f"Claude API health check failed: {str(e)}")
            return False
