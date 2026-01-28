"""
Sentinel Actions & Execution Models

Actions are executed operations with outcomes.

Domain: Actions & Execution
"""

from sqlalchemy import Column, String, Enum as SQLEnum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from db.session import Base
from db.models.base import TimestampMixin, UUIDPrimaryKey

import enum


class ActionStatus(str, enum.Enum):
    """Execution status of an action."""
    
    PENDING = "pending"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class Action(Base, UUIDPrimaryKey, TimestampMixin):
    """
    Represents an executed or pending action.
    
    Actions are:
    - Only executed by the Executor Agent
    - Only after explicit approval
    - Fully logged with outcomes
    - Reversible where possible
    """
    
    __tablename__ = "actions"
    
    proposal_id = Column(
        UUID(as_uuid=True),
        ForeignKey("proposals.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Which proposal was executed",
    )
    
    decision_id = Column(
        UUID(as_uuid=True),
        ForeignKey("human_decisions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Which human decision approved this",
    )
    
    status = Column(
        SQLEnum(ActionStatus),
        nullable=False,
        default=ActionStatus.PENDING,
        index=True,
    )
    
    action_definition = Column(
        JSONB,
        nullable=False,
        comment="What was executed (may be modified from original proposal)",
    )
    
    outcome = Column(
        JSONB,
        nullable=True,
        comment="Results of execution (success data, error details, etc.)",
    )
    
    error_message = Column(
        Text,
        nullable=True,
        comment="Error details if action failed",
    )
    
    rollback_data = Column(
        JSONB,
        nullable=True,
        comment="Data needed to reverse this action",
    )
    
    additional_metadata = Column(
        JSONB,
        nullable=True,
        default=dict,
        comment="Additional action-specific metadata",
    )
    
    # Relationships
    proposal = relationship("Proposal", backref="actions")
    decision = relationship("HumanDecision", backref="actions")
    
    def __repr__(self) -> str:
        return f"<Action(id={self.id}, proposal_id={self.proposal_id}, status={self.status})>"
