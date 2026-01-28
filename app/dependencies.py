"""
Sentinel FastAPI Dependencies

This module defines all FastAPI dependency providers used across the API layer.

Design principles:
- Centralized dependency definitions
- Request-scoped resources
- No business logic
- Safe to import anywhere
- Easy to extend incrementally

This file acts as the "spine" of request handling.
"""

from typing import Generator, Optional

from fastapi import Depends, Header, HTTPException, status

from app.config import get_settings
from app.logger import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------
# Configuration Dependency
# ---------------------------------------------------------------------

def settings_dependency():
    """
    Provide access to Sentinel settings.

    This is a thin wrapper around get_settings() so it can be used
    consistently as a FastAPI dependency.
    """
    return get_settings()


# ---------------------------------------------------------------------
# Database Session Dependency (Stub)
# ---------------------------------------------------------------------

def db_session_dependency() -> Generator[None, None, None]:
    """
    Provide a database session for the request lifecycle.

    NOTE:
    - This is a stub in the scaffold phase.
    - Actual SQLAlchemy session wiring will be added later.
    - Yield-based pattern is used to support cleanup.

    Future responsibilities:
    - Open DB session
    - Yield session
    - Commit / rollback
    - Close session
    """
    logger.debug("DB session dependency requested (stub)")
    try:
        yield None
    finally:
        pass


# ---------------------------------------------------------------------
# Authentication Dependency (Single-User Model)
# ---------------------------------------------------------------------

def auth_dependency(
    authorization: Optional[str] = Header(default=None),
):
    """
    Authenticate incoming requests using a static bearer token.

    Sentinel is a single-user system.
    This dependency enforces:
    - Presence of Authorization header
    - Correct bearer token

    NOTE:
    - Token validation is intentionally simple.
    - This is not OAuth and does not support multiple users.
    """
    settings = get_settings()

    if settings.api_auth_token is None:
        logger.warning(
            "API auth token is not configured; allowing request (development mode)"
        )
        return

    if not authorization:
        logger.warning("Missing Authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )

    scheme, _, token = authorization.partition(" ")

    if scheme.lower() != "bearer" or token != settings.api_auth_token:
        logger.warning("Invalid API authentication token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    logger.debug("Request authenticated successfully")


# ---------------------------------------------------------------------
# Common Dependency Bundles
# ---------------------------------------------------------------------

def common_dependencies():
    """
    Bundle commonly used dependencies.

    This helper exists to make router definitions cleaner.

    Example usage:
        dependencies=[Depends(common_dependencies)]
    """
    return Depends(auth_dependency)