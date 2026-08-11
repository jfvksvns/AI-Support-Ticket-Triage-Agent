"""
FastAPI application initialization and configuration.
Sets up the app, middleware, routes, and Swagger documentation.
"""

import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi

from app.core.config import get_settings
from app.database.engine import DatabaseEngine, init_db, close_db
from app.api.routes import router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting AI Support Ticket Triage Agent...")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    close_db()
    logger.info("Application shutdown complete")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    settings = get_settings()

    # Create FastAPI app
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan
    )

    # ==================== Middleware ====================

    # CORS Middleware
    if settings.ENABLE_CORS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.ALLOWED_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        logger.info(f"CORS enabled for origins: {settings.ALLOWED_ORIGINS}")

    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Handle uncaught exceptions globally."""
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

    # ==================== Request/Response Logging ====================

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """Log all HTTP requests."""
        logger.debug(f"{request.method} {request.url.path}")
        response = await call_next(request)
        logger.debug(f"{request.method} {request.url.path} - {response.status_code}")
        return response

    # ==================== Routes ====================

    app.include_router(router)

    # Root endpoint
    @app.get("/", tags=["health"])
    async def root():
        """Root endpoint providing API information."""
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "description": settings.APP_DESCRIPTION,
            "docs": "/api/docs",
            "health": "/api/health"
        }

    # ==================== Custom OpenAPI Schema ====================

    def custom_openapi():
        """Customize OpenAPI schema with additional metadata."""
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title=settings.APP_NAME,
            version=settings.APP_VERSION,
            description=settings.APP_DESCRIPTION,
            routes=app.routes,
        )

        openapi_schema["info"]["x-logo"] = {
            "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
        }

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

    logger.info(f"FastAPI application created: {settings.APP_NAME} v{settings.APP_VERSION}")
    return app


# Create the FastAPI application instance
app = create_app()
