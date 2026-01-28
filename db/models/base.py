"""
Sentinel Database Model Base Classes

This module defines shared base classes and mixins for all database models.

Design principles:
- DRY (Don't Repeat Yourself)
- Consistent timestamps
- Consistent ID generation
- Audit trail support
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID


class TimestampMixin:
    """
    Mixin for created_at and updated_at timestamps.
    
    Every model that tracks creation/modification time should inherit this.
    """
    
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class UUIDPrimaryKey:
    """
    Mixin for UUID primary keys.
    
    Most Sentinel entities use UUIDs for:
    - Global uniqueness
    - No sequential enumeration
    - Compatibility with distributed systems
    """
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False,
    )
