"""
Actions API Router

Endpoints for viewing action execution history.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db import get_db
from db.models import Action
from app.auth import get_authenticated_identity
from app.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get(
    "/proposal/{proposal_id}",
    summary="Get actions for a proposal",
)
async def get_proposal_actions(
    proposal_id: UUID,
    db: AsyncSession = Depends(get_db),
    identity: dict = Depends(get_authenticated_identity),
):
    """
    Get all actions executed for a specific proposal.
    """
    logger.info(f"Getting actions for proposal {proposal_id}")
    
    result = await db.execute(
        select(Action).where(Action.proposal_id == proposal_id)
    )
    actions = result.scalars().all()
    
    return {
        "proposal_id": str(proposal_id),
        "actions": [
            {
                "id": str(action.id),
                "status": action.status.value,
                "outcome": action.outcome,
                "created_at": action.created_at.isoformat(),
            }
            for action in actions
        ],
    }
