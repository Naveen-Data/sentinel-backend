"""
Sentinel LangGraph Orchestration Models

Represents graph runs, state transitions, and orchestration metadata.

Domain: Orchestration (LangGraph)
"""

from sqlalchemy import Column, String, Enum as SQLEnum, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from db.session import Base
from db.models.base import TimestampMixin, UUIDPrimaryKey

import enum


class GraphRunStatus(str, enum.Enum):
    """Overall status of a graph run."""
    
    STARTED = "started"
    IN_PROGRESS = "in_progress"
    PAUSED_FOR_HUMAN = "paused_for_human"
    RESUMED = "resumed"
    COMPLETED = "completed"
    FAILED = "failed"


class GraphRun(Base, UUIDPrimaryKey, TimestampMixin):
    """
    Represents one execution of the Sentinel LangGraph.
    
    A graph run is:
    - The top-level unit of work
    - Traceable in Langfuse
    - May pause and resume
    - May contain multiple state transitions
    """
    
    __tablename__ = "graph_runs"
    
    status = Column(
        SQLEnum(GraphRunStatus),
        nullable=False,
        default=GraphRunStatus.STARTED,
        index=True,
    )
    
    trigger_type = Column(
        String(100),
        nullable=False,
        index=True,
        comment="What triggered this run (scheduled, manual, api, observation)",
    )
    
    observation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("observations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Which observation triggered this run (if applicable)",
    )
    
    langfuse_trace_id = Column(
        String(500),
        nullable=True,
        index=True,
        comment="Langfuse trace ID for observability correlation",
    )
    
    initial_state = Column(
        JSONB,
        nullable=True,
        comment="Starting state of the graph",
    )
    
    final_state = Column(
        JSONB,
        nullable=True,
        comment="Terminal state of the graph",
    )
    
    additional_metadata = Column(
        JSONB,
        nullable=True,
        default=dict,
        comment="Additional graph run metadata",
    )
    
    # Relationships
    observation = relationship("Observation", backref="graph_runs")
    
    def __repr__(self) -> str:
        return f"<GraphRun(id={self.id}, status={self.status}, trigger={self.trigger_type})>"


class StateTransition(Base, UUIDPrimaryKey, TimestampMixin):
    """
    Represents a single state transition within a graph run.
    
    State transitions are:
    - Explicit, never implicit
    - Logged with reasons
    - The atomic unit of orchestration observability
    """
    
    __tablename__ = "state_transitions"
    
    graph_run_id = Column(
        UUID(as_uuid=True),
        ForeignKey("graph_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    from_state = Column(
        String(100),
        nullable=False,
        comment="Previous state",
    )
    
    to_state = Column(
        String(100),
        nullable=False,
        index=True,
        comment="New state",
    )
    
    reason = Column(
        Text,
        nullable=True,
        comment="Why this transition occurred",
    )
    
    additional_metadata = Column(
        JSONB,
        nullable=True,
        default=dict,
        comment="Additional transition metadata",
    )
    
    # Relationships
    graph_run = relationship("GraphRun", backref="transitions")
    
    def __repr__(self) -> str:
        return f"<StateTransition(id={self.id}, {self.from_state} → {self.to_state})>"
