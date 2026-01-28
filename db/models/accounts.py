"""
Sentinel Accounts & Sources Models

Represents external data sources (not users).
Sentinel is single-user, but multi-source.

Domain: Accounts & Sources
"""

from sqlalchemy import Column, String, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB

from db.session import Base
from db.models.base import TimestampMixin, UUIDPrimaryKey

import enum


class AccountType(str, enum.Enum):
    """Types of external accounts Sentinel can connect to."""
    
    GMAIL = "gmail"
    GOOGLE_CALENDAR = "google_calendar"
    APPLE_HEALTH = "apple_health"


class AccountStatus(str, enum.Enum):
    """Status of an external account connection."""
    
    ACTIVE = "active"
    REVOKED = "revoked"
    ERROR = "error"


class Account(Base, UUIDPrimaryKey, TimestampMixin):
    """
    Represents an external system connection.
    
    Examples:
    - Personal Gmail account
    - Work Google Calendar
    - Apple Health data export
    
    NOTE: Sentinel is single-user, so there is no user_id foreign key.
    """
    
    __tablename__ = "accounts"
    
    account_type = Column(
        SQLEnum(AccountType),
        nullable=False,
        index=True,
    )
    
    label = Column(
        String(255),
        nullable=False,
        comment="Human-readable label (e.g., 'Personal Email', 'Work Calendar')",
    )
    
    external_identifier = Column(
        String(500),
        nullable=True,
        comment="External system's identifier (e.g., email address)",
    )
    
    status = Column(
        SQLEnum(AccountStatus),
        nullable=False,
        default=AccountStatus.ACTIVE,
        index=True,
    )
    
    credentials = Column(
        JSONB,
        nullable=True,
        comment="Encrypted credentials and tokens (implementation-dependent)",
    )
    
    additional_metadata = Column(
        JSONB,
        nullable=True,
        default=dict,
        comment="Additional account-specific metadata",
    )
    
    def __repr__(self) -> str:
        return f"<Account(id={self.id}, type={self.account_type}, label={self.label})>"
