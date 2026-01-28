"""
API Schemas for Sentinel

Pydantic models for API request/response validation.

Design principles:
- Explicit, typed schemas
- Clear validation rules
- Consistent naming
- Documentation in models
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# ---------------------------------------------------------------------
# Common Schemas
# ---------------------------------------------------------------------

class MessageResponse(BaseModel):
    """Standard message response."""
    
    message: str
    details: Optional[dict] = None


class ErrorResponse(BaseModel):
    """Standard error response."""
    
    error: str
    details: Optional[dict] = None


# ---------------------------------------------------------------------
# Observation Schemas
# ---------------------------------------------------------------------

class ObservationCreate(BaseModel):
    """Request to create a new observation."""
    
    observation_type: str = Field(
        ...,
        description="Type of observation (email_received, etc.)",
    )
    
    subject: Optional[str] = Field(
        None,
        max_length=500,
        description="Short summary or subject",
    )
    
    content: Optional[str] = Field(
        None,
        description="Full content",
    )
    
    external_id: Optional[str] = Field(
        None,
        description="External system ID",
    )
    
    metadata: Optional[dict] = Field(
        default_factory=dict,
        description="Additional metadata",
    )


class ObservationResponse(BaseModel):
    """Response for observation data."""
    
    id: UUID
    observation_type: str
    status: str
    subject: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ---------------------------------------------------------------------
# Proposal Schemas
# ---------------------------------------------------------------------

class ProposalResponse(BaseModel):
    """Response for proposal data."""
    
    id: UUID
    proposal_type: str
    status: str
    agent_name: str
    confidence: float
    reasoning: Optional[str]
    proposed_action: dict
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProposalList(BaseModel):
    """List of proposals."""
    
    proposals: List[ProposalResponse]
    total: int


# ---------------------------------------------------------------------
# Human Decision Schemas
# ---------------------------------------------------------------------

class HumanDecisionCreate(BaseModel):
    """Request to submit a human decision."""
    
    proposal_id: UUID = Field(
        ...,
        description="Which proposal is being decided",
    )
    
    decision_type: str = Field(
        ...,
        description="approve, reject, modify, or defer",
    )
    
    decision_source: str = Field(
        default="web_ui",
        description="How decision was made (web_ui, telegram, api)",
    )
    
    reasoning: Optional[str] = Field(
        None,
        description="Optional explanation",
    )
    
    modified_action: Optional[dict] = Field(
        None,
        description="Modified action if decision_type is 'modify'",
    )


class HumanDecisionResponse(BaseModel):
    """Response for human decision data."""
    
    id: UUID
    proposal_id: UUID
    decision_type: str
    decision_source: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ---------------------------------------------------------------------
# Graph Run Schemas
# ---------------------------------------------------------------------

class GraphRunResponse(BaseModel):
    """Response for graph run data."""
    
    id: UUID
    status: str
    trigger_type: str
    langfuse_trace_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class GraphRunList(BaseModel):
    """List of graph runs."""
    
    graph_runs: List[GraphRunResponse]
    total: int
