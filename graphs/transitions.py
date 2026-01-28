"""
Sentinel State Transition Logic

This module handles explicit state transitions with full audit trails.

Design principles:
- All state changes go through this module
- Every transition is logged
- Invalid transitions are rejected
- Transitions are observable
"""

from uuid import UUID
from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from graphs.states import SentinelState, get_allowed_transitions
from db.models.graph_runs import StateTransition
from app.logger import get_logger

logger = get_logger(__name__)


async def transition_state(
    db: AsyncSession,
    graph_run_id: UUID,
    from_state: SentinelState,
    to_state: SentinelState,
    reason: str,
    metadata: Optional[dict] = None,
) -> StateTransition:
    """
    Execute a state transition with full validation and audit trail.
    
    This is the ONLY way state transitions should occur in Sentinel.
    
    Args:
        db: Database session
        graph_run_id: Which graph run is transitioning
        from_state: Current state
        to_state: Desired next state
        reason: Why this transition is occurring
        metadata: Additional context
        
    Returns:
        StateTransition record
        
    Raises:
        ValueError: If transition is not allowed
    """
    # Validate transition is allowed
    allowed_transitions = get_allowed_transitions(from_state)
    
    if to_state not in allowed_transitions:
        error_msg = (
            f"Invalid state transition: {from_state.value} → {to_state.value}. "
            f"Allowed transitions: {[s.value for s in allowed_transitions]}"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    # Create transition record
    transition = StateTransition(
        graph_run_id=graph_run_id,
        from_state=from_state.value,
        to_state=to_state.value,
        reason=reason,
        metadata=metadata or {},
    )
    
    db.add(transition)
    await db.flush()
    
    logger.info(
        f"State transition: {from_state.value} → {to_state.value}",
        extra={
            "graph_run_id": str(graph_run_id),
            "transition_id": str(transition.id),
            "reason": reason,
        },
    )
    
    return transition


async def get_current_state(
    db: AsyncSession,
    graph_run_id: UUID,
) -> Optional[SentinelState]:
    """
    Get the current state of a graph run.
    
    This queries the most recent state transition.
    """
    from sqlalchemy import select, desc
    
    stmt = (
        select(StateTransition)
        .where(StateTransition.graph_run_id == graph_run_id)
        .order_by(desc(StateTransition.created_at))
        .limit(1)
    )
    
    result = await db.execute(stmt)
    latest_transition = result.scalar_one_or_none()
    
    if latest_transition is None:
        return None
    
    return SentinelState(latest_transition.to_state)
