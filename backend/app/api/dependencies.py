"""
Dependency injection and security functions for API routes.
Handles authentication, validation, and service initialization.
"""

import logging
from typing import Optional

from fastapi import Depends, HTTPException, Header, status

from app.core.config import get_settings
from app.database.session import get_db
from app.services.classification_service import ClassificationService
from app.services.analytics_service import AnalyticsService

logger = logging.getLogger(__name__)


def verify_api_key(
    x_api_key: Optional[str] = Header(None)
) -> Optional[str]:
    """
    Verify API key from request headers.
    
    If API key is configured in settings, validates the request.
    If no API key is configured, authentication is disabled.
    
    Args:
        x_api_key: API key from X-API-Key header
        
    Returns:
        Optional[str]: The API key if valid
        
    Raises:
        HTTPException: If API key is required but missing or invalid
    """
    settings = get_settings()
    
    # If no API key is configured, skip authentication
    if not settings.API_KEY:
        return None
    
    # If API key is configured, validate it
    if not x_api_key:
        logger.warning("API request received without API key header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if x_api_key != settings.API_KEY:
        logger.warning(f"Invalid API key attempted: {x_api_key[:10]}...")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
    
    return x_api_key


def get_classification_service() -> ClassificationService:
    """
    Get the classification service instance.
    Dependency for ticket classification operations.
    
    Returns:
        ClassificationService: Classification service instance
    """
    return ClassificationService()


def get_analytics_service() -> AnalyticsService:
    """
    Get the analytics service instance.
    Dependency for statistics and analytics operations.
    
    Returns:
        AnalyticsService: Analytics service instance
    """
    return AnalyticsService()


# Optional: For routes that don't require authentication
def optional_api_key(
    x_api_key: Optional[str] = Header(None)
) -> Optional[str]:
    """
    Optional API key verification.
    Allows requests with or without API key.
    
    Args:
        x_api_key: API key from X-API-Key header (optional)
        
    Returns:
        Optional[str]: The API key if provided and valid, None otherwise
    """
    settings = get_settings()
    
    # If no API key is configured, skip authentication
    if not settings.API_KEY:
        return None
    
    # If API key is provided, validate it
    if x_api_key and x_api_key != settings.API_KEY:
        logger.warning(f"Invalid API key attempted: {x_api_key[:10]}...")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
    
    return x_api_key
