"""
Sentinel Configuration Module

This module defines all runtime configuration for the Sentinel backend.

Design principles:
- Single source of truth for configuration
- Explicit, typed settings
- Environment-driven
- Safe to import from anywhere
- No side effects on import

Nothing in this file should depend on application logic.
"""

from functools import lru_cache
from typing import Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class SentinelSettings(BaseSettings):
    """
    Global configuration for Sentinel.

    All values are loaded from environment variables.
    Defaults are intentionally conservative.
    """

    # Application ----------
    
    app_name: str = Field(default="sentinel-backend")
    environment: str = Field(default="development")  # development | staging | production
    debug: bool = Field(default=False)

    # Security ---------------------

    api_auth_token: Optional[str] = Field(
        default=None,
        description="Static bearer token for frontend and Telegram authentication",
    )

    # Database ---------------------

    database_url: str = Field(
        default="postgresql://sentinel:sentinel@localhost:5432/sentinel",
        description="PostgreSQL connection string",
    )

    # LangGraph ---------------------
    
    enable_langgraph: bool = Field(default=True)

    # CrewAI / Agents ---------------------

    enable_agents: bool = Field(default=True)
    crewai_api_key: Optional[str] = Field(
        default=None,
        description="API key for CrewAI integration",
    )
    # Observability (Langfuse) ---------------------

    enable_observability: bool = Field(default=True)
    langfuse_public_key: Optional[str] = Field(default=None)
    langfuse_secret_key: Optional[str] = Field(default=None)
    langfuse_host: Optional[str] = Field(
        default="https://cloud.langfuse.com",
        description="Langfuse API endpoint",
    )

    # Scheduling ---------------------
    enable_scheduler: bool = Field(default=True)

    # Feature Flags (Safety First) ---------------------

    allow_auto_approval: bool = Field(
        default=False,
        description="If true, low-risk proposals may skip human approval",
    )

    allow_execution: bool = Field(
        default=True,
        description="Global kill switch for all execution",
    )
    class Config:
        env_prefix = "SENTINEL_"
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> SentinelSettings:
    """
    Cached access to Sentinel settings.

    Using lru_cache ensures:
    - Settings are loaded once
    - Imports are cheap
    - Configuration is consistent across the app
    """
    return SentinelSettings()