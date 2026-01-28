"""
Sentinel Pause and Resume Logic

This module handles pausing graph execution for human input and resuming after approval.

Design principles:
- Human approval is a first-class state
- Graphs can pause indefinitely
- Resume is explicit
- State is preserved
"""

from uuid import UUID
from typing import Optional

from app.logger import get_logger

logger = get_logger(__name__)


async def pause_for_human_approval(
    graph_run_id: UUID,
    proposal_id: UUID,
) -> None:
    """
    Pause graph execution and wait for human decision.
    
    This function:
    - Transitions to AWAITING_HUMAN state
    - Sends notifications (Web UI + Telegram)
    - Saves graph state
    
    Args:
        graph_run_id: Which graph run to pause
        proposal_id: Which proposal needs approval
    """
    logger.info(
        f"Pausing graph run for human approval",
        extra={
            "graph_run_id": str(graph_run_id),
            "proposal_id": str(proposal_id),
        },
    )
    
    # TODO: Send notification to Web UI
    # TODO: Send notification to Telegram
    # TODO: Persist pause state


async def resume_after_approval(
    graph_run_id: UUID,
    decision: dict,
) -> None:
    """
    Resume graph execution after human decision.
    
    Args:
        graph_run_id: Which graph run to resume
        decision: Human decision (approve/reject/modify)
    """
    logger.info(
        f"Resuming graph run after decision",
        extra={
            "graph_run_id": str(graph_run_id),
            "decision_type": decision.get("type"),
        },
    )
    
    # TODO: Load graph state
    # TODO: Apply decision
    # TODO: Resume graph execution
