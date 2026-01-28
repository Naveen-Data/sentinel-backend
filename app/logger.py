"""
Sentinel Logging Configuration

This module defines the logging setup for the Sentinel backend.

Design goals:
- Structured, consistent logs
- Environment-aware verbosity
- Safe to import anywhere
- Compatible with observability tools (Langfuse)
- No side effects beyond logging configuration

Logging is not observability, but observability builds on logging.
"""

import logging
import sys
from typing import Optional

from app.config import get_settings


LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)


def _get_log_level(environment: str, debug: bool) -> int:
    """
    Determine log level based on environment and debug flag.

    - development + debug -> DEBUG
    - production -> INFO
    - otherwise -> INFO
    """
    if environment == "development" and debug:
        return logging.DEBUG
    return logging.INFO


def configure_logging() -> None:
    """
    Configure global logging for Sentinel.

    This function should be called exactly once,
    at application startup (e.g., in app/main.py).

    It configures:
    - Root logger
    - Stream handler
    - Formatting
    """
    settings = get_settings()

    log_level = _get_log_level(
        environment=settings.environment,
        debug=settings.debug,
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers to avoid duplicate logs
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)

    root_logger.addHandler(handler)

    # Silence overly noisy third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)

    root_logger.debug(
        "Logging configured",
        extra={
            "environment": settings.environment,
            "debug": settings.debug,
            "log_level": logging.getLevelName(log_level),
        },
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a namespaced logger for a Sentinel module.

    Usage:
        logger = get_logger(__name__)

    This ensures:
    - Consistent naming
    - Centralized configuration
    - Easy filtering
    """
    return logging.getLogger(name if name else "sentinel")