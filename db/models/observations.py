"""
Sentinel Observations Models

Observations are facts captured from reality.

Domain: Observations
"""

from sqlalchemy import Column, String, Enum as SQLEnum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from db.session import Base
from db.models.base import TimestampMixin, UUIDPrimaryKey

import enum


class ObservationType(str, enum.Enum):
    """Types of observations Sentinel can capture."""
    
    EMAIL_RECEIVED = "email_received"
    CALENDAR_EVENT_CREATED = "calendar_event_created"
    CALENDAR_EVENT_UPDATED = "calendar_event_updated"
    HEALTH_DATA_SYNCED = "health_data_synced"
    MANUAL_INPUT = "manual_input"


class ObservationStatus(str, enum.Enum):
    """Processing status of an observation."""
    
    PENDING = "pending"
    ANALYZED = "analyzed"
    IGNORED = "ignored"
    ARCHIVED = "archived"


class Observation(Base, UUIDPrimaryKey, TimestampMixin):
    """
    Represents a fact from reality.
    
    Observations are:
    - Immutable (append-only)
    - Source-attributed
    - Never deleted (only archived)
    - The starting point of all decision chains
    """
    
    __tablename__ = "observations"
    
    observation_type = Column(
        SQLEnum(ObservationType),
        nullable=False,
        index=True,
    )
    
    account_id = Column(
        UUID(as_uuid=True),
        ForeignKey("accounts.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Which account this observation came from",
    )
    
    status = Column(
        SQLEnum(ObservationStatus),
        nullable=False,
        default=ObservationStatus.PENDING,
        index=True,
    )
    
    external_id = Column(
        String(500),
        nullable=True,
        comment="External system's ID for this observation (e.g., email message ID)",
    )
    
    subject = Column(
        String(500),
        nullable=True,
        comment="Short summary or subject line",
    )
    
    content = Column(
        Text,
        nullable=True,
        comment="Full content or body (may be truncated for large items)",
    )
    
    raw_data = Column(
        Text,
        nullable=True,
        comment="Raw data or payload (e.g., JSON, XML, etc.)",
    )
    
    # Renaming 'metadata' to avoid conflict with SQLAlchemy reserved names
    additional_metadata = Column(
        JSONB,
        nullable=True,
        default=dict,
        comment="Additional observation-specific metadata",
    )
    
    # Relationships
    account = relationship("Account", backref="observations")
    
    def __repr__(self) -> str:
        return f"<Observation(id={self.id}, type={self.observation_type}, status={self.status})>"
