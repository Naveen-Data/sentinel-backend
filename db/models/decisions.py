"""
Sentinel Human Decisions Models

Human decisions are explicit approval/rejection records.

Domain: Human Decisions
"""

from sqlalchemy import Column, String, Enum as SQLEnum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB

from db.session import Base
from db.models.base import TimestampMixin, UUIDPrimaryKey
from sqlalchemy.orm import relationship

import enum


class DecisionType(str, enum.Enum):
    """Types of human decisions."""
    
    APPROVE = "approve"
    REJECT = "reject"
    MODIFY = "modify"
    DEFER = "defer"


class DecisionSource(str, enum.Enum):
    """How the human decision was made."""
    
    WEB_UI = "web_ui"
    TELEGRAM = "telegram"
    API = "api"


class HumanDecision(Base, UUIDPrimaryKey, TimestampMixin):
    """
    Represents a human approval or rejection.
    
    Human decisions are:
    - First-class state transitions
    - Never bypassed
    - Fully audited
    - Correlated with agent confidence
    """
    
    __tablename__ = "human_decisions"
    
    proposal_id = Column(
        UUID(as_uuid=True),
        ForeignKey("proposals.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Which proposal was decided upon",
    )
    
    decision_type = Column(
        SQLEnum(DecisionType),
        nullable=False,
        index=True,
    )
    
    decision_source = Column(
        SQLEnum(DecisionSource),
        nullable=False,
        comment="How the decision was made (web, telegram, etc.)",
    )
    
    reasoning = Column(
        Text,
        nullable=True,
        comment="Optional human explanation for the decision",
    )
    
    modified_action = Column(
        JSONB,
        nullable=True,
        comment="If modified, the new action definition",
    )
    
    additional_metadata = Column(
        JSONB,
        nullable=True,
        default=dict,
        comment="Additional decision-specific metadata",
    )
    
    # Relationships
    proposal = relationship("Proposal", backref="decisions")
    
    def __repr__(self) -> str:
        return f"<HumanDecision(id={self.id}, proposal_id={self.proposal_id}, type={self.decision_type})>"
