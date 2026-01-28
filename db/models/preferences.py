"""
Sentinel Preferences & System Metadata Models

Stores user preferences and system configuration.

Domain: Preferences & System Metadata
"""

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import JSONB

from db.session import Base
from db.models.base import TimestampMixin, UUIDPrimaryKey


class Preference(Base, UUIDPrimaryKey, TimestampMixin):
    """
    Represents a user preference or system setting.
    
    Preferences are:
    - Key-value pairs
    - Schema-flexible (JSONB)
    - Used for personalization
    - Learned over time
    """
    
    __tablename__ = "preferences"
    
    key = Column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
        comment="Preference key (e.g., 'default_work_start_time')",
    )
    
    value = Column(
        JSONB,
        nullable=False,
        comment="Preference value (flexible schema)",
    )
    
    description = Column(
        Text,
        nullable=True,
        comment="Human-readable description of this preference",
    )
    
    additional_metadata = Column(
        JSONB,
        nullable=True,
        default=dict,
        comment="Additional metadata",
    )
    
    def __repr__(self) -> str:
        return f"<Preference(key={self.key})>"
