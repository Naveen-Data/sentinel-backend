"""
Sentinel Backend Application Entry Point

This module initializes the FastAPI application and wires together:
- Configuration
- Logging
- Basic health endpoint
- API routers (scaffold only)

Business logic, agents, and orchestration must NOT live here.
"""

from fastapi import FastAPI

from app.config import get_settings
from app.logger import configure_logging, get_logger

# ---------------------------------------------------------------------
# Application Setup
# ---------------------------------------------------------------------

settings = get_settings()

configure_logging()
logger = get_logger(__name__)

logger.info(
    "Starting Sentinel backend",
    extra={
        "app_name": settings.app_name,
        "environment": settings.environment,
        "debug": settings.debug,
    },
)

app = FastAPI(
    title="Sentinel Backend",
    description="Agentic AI backend with human-in-the-loop control",
    version="0.1.0",
    debug=settings.debug,
)

# ---------------------------------------------------------------------
# Health & Meta Endpoints
# ---------------------------------------------------------------------

@app.get("/", tags=["system"])
def root() -> dict:
    """
    Root endpoint providing API information.
    """
    return {
        "service": "Sentinel Backend",
        "version": "0.1.0",
        "description": "Agentic AI backend with human-in-the-loop control",
        "health": "/health",
        "api": {
            "proposals": "/api/proposals",
            "graph_runs": "/api/graph-runs", 
            "actions": "/api/actions",
            "decisions": "/api/decisions"
        },
        "docs": "/docs",
        "openapi": "/openapi.json"
    }

@app.get("/health", tags=["system"])
def health_check() -> dict:
    """
    Basic health check endpoint.

    This endpoint intentionally avoids:
    - Database checks
    - External API checks
    - Agent execution

    Its only purpose is to confirm the service is running.
    """
    logger.debug("Health check requested")
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.environment,
    }


# ---------------------------------------------------------------------
# Router Registration
# ---------------------------------------------------------------------

from api import proposals, graph_runs, actions, decisions

app.include_router(
    proposals.router,
    prefix="/api/proposals",
    tags=["proposals"],
)

app.include_router(
    graph_runs.router,
    prefix="/api/graph-runs",
    tags=["graph-runs"],
)

app.include_router(
    actions.router,
    prefix="/api/actions",
    tags=["actions"],
)

app.include_router(
    decisions.router,
    prefix="/api/decisions",
    tags=["decisions"],
)


# ---------------------------------------------------------------------
# Startup & Shutdown Hooks
# ---------------------------------------------------------------------

@app.on_event("startup")
async def on_startup() -> None:
    """
    Application startup hook.
    
    Responsibilities:
    - Initialize database connections
    - Initialize Langfuse
    - Log startup
    """
    from db import init_db
    from observability import get_langfuse_client
    
    logger.info("Sentinel backend starting up...")
    
    # Initialize database
    if settings.database_url:
        try:
            await init_db()
            logger.info("Database initialized")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
    
    # Initialize observability
    if settings.enable_observability:
        langfuse = get_langfuse_client()
        if langfuse:
            logger.info("Langfuse observability enabled")
        else:
            logger.warning("Langfuse initialization failed or not configured")
    
    logger.info("Sentinel backend startup complete")



@app.on_event("shutdown")
async def on_shutdown() -> None:
    """
    Application shutdown hook.
    
    Responsibilities:
    - Flush Langfuse
    - Close database connections
    """
    from observability.langfuse_client import shutdown_langfuse
    
    logger.info("Sentinel backend shutting down...")
    
    # Shutdown observability
    shutdown_langfuse()
    
    logger.info("Sentinel backend shutdown complete")