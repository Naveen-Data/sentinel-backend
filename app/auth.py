"""
Sentinel Authentication Module

This module contains authentication and authorization logic for Sentinel.

Design principles:
- Single-user system
- Explicit, simple authentication
- No external identity providers
- Easy to audit and reason about
- No side effects

This module should never contain business logic.
"""

from typing import Optional

from fastapi import Header, HTTPException, status

from app.config import get_settings
from app.logger import get_logger

logger = get_logger(__name__)


def verify_bearer_token(authorization: Optional[str]) -> None:
    """
    Verify the Authorization header against Sentinel's static bearer token.

    Rules:
    - Sentinel is a single-user system
    - Uses a static bearer token configured via environment variable
    - If no token is configured, authentication is bypassed (development only)

    Raises:
        HTTPException: If authentication fails
    """
    settings = get_settings()

    # Development / local mode: allow requests if no token is set
    if settings.api_auth_token is None:
        logger.warning(
            "API auth token not configured; authentication bypassed"
        )
        return

    if not authorization:
        logger.warning("Authorization header missing")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )

    scheme, _, token = authorization.partition(" ")

    if scheme.lower() != "bearer":
        logger.warning("Invalid authorization scheme")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization scheme",
        )

    if token != settings.api_auth_token:
        logger.warning("Invalid bearer token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    logger.debug("Bearer token authentication successful")


def get_authenticated_identity(
    authorization: Optional[str] = Header(default=None),
) -> dict:
    """
    Authenticate the request and return the authenticated identity.

    Sentinel is single-user, so the identity is static.

    Returns:
        dict: Authenticated identity metadata
    """
    verify_bearer_token(authorization)

    # Sentinel does not support multiple users.
    # This identity object exists for auditability and future extensibility.
    identity = {
        "type": "single_user",
        "source": "static_token",
    }

    logger.debug("Authenticated identity resolved", extra=identity)
    return identity