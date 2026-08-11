#!/usr/bin/env python3
"""
Entry point for the AI Support Ticket Triage Agent backend.
Starts the FastAPI application with Uvicorn.

Usage:
    python main.py              # Start with default settings
    python main.py --host 0.0.0.0 --port 8000  # Custom host/port
    python main.py --reload     # Auto-reload on file changes
"""

import uvicorn
import logging
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from app.main import app
from app.core.config import get_settings

logger = logging.getLogger(__name__)


def main():
    """
    Main entry point for the application.
    Starts the Uvicorn ASGI server.
    """
    settings = get_settings()
    
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Server: {settings.HOST}:{settings.PORT}")
    logger.info(f"Database: {settings.DATABASE_URL}")
    logger.info(f"Claude Model: {settings.CLAUDE_MODEL}")
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True,
        use_colors=True
    )


if __name__ == "__main__":
    main()
