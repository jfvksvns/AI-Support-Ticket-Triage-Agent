"""
Core configuration for the AI Support Ticket Triage Agent.
Loads environment variables and provides app-wide configuration.
"""

import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application metadata
    APP_NAME: str = "AI Support Ticket Triage Agent"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Intelligent AI-powered support ticket classification and routing system"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Server configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    RELOAD: bool = os.getenv("RELOAD", "True").lower() == "true"

    # Database configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./tickets.db"
    )
    DATABASE_ECHO: bool = os.getenv("DATABASE_ECHO", "False").lower() == "true"

    # Claude AI configuration
    CLAUDE_API_KEY: str = os.getenv("CLAUDE_API_KEY", "")
    CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "claude-opus-4-1")
    CLAUDE_MAX_TOKENS: int = int(os.getenv("CLAUDE_MAX_TOKENS", "2048"))
    CLAUDE_TIMEOUT: int = int(os.getenv("CLAUDE_TIMEOUT", "30"))

    # API configuration
    API_KEY: Optional[str] = os.getenv("API_KEY", None)
    ENABLE_CORS: bool = os.getenv("ENABLE_CORS", "True").lower() == "true"
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    # Logging configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "app.log")

    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = True

    def validate_config(self) -> None:
        """Validate critical configuration settings."""
        if not self.CLAUDE_API_KEY:
            raise ValueError(
                "CLAUDE_API_KEY environment variable is not set. "
                "Please provide a valid Claude API key."
            )
        if self.PORT < 1 or self.PORT > 65535:
            raise ValueError(f"Invalid PORT: {self.PORT}. Must be between 1 and 65535.")


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings (cached).
    Validates configuration on first load.

    Returns:
        Settings: Application configuration instance.

    Raises:
        ValueError: If critical configuration is missing or invalid.
    """
    settings = Settings()
    settings.validate_config()
    return settings
