"""
Decisions API Router

Endpoints for submitting and viewing human decisions.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db import get_db
from db.models import HumanDecision, Proposal, DecisionType, DecisionSource
from api.schemas import HumanDecisionCreate, HumanDecisionResponse, MessageResponse
from app.auth import get_authenticated_identity
from app.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post(
    "/",
    response_model=HumanDecisionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a human decision",
)
async def create_decision(
    decision: HumanDecisionCreate,
    db: AsyncSession = Depends(get_db),
    identity: dict = Depends(get_authenticated_identity),
) -> HumanDecisionResponse:
    """
    Submit a human decision (approve/reject/modify/defer) for a proposal.
    
    This endpoint:
    - Validates the proposal exists
    - Creates a decision record
    - Triggers graph resume (if applicable)
    """
    logger.info(
        f"Creating decision for proposal {decision.proposal_id}",
        extra={"decision_type": decision.decision_type},
    )
    
    # Verify proposal exists
    result = await db.execute(
        select(Proposal).where(Proposal.id == decision.proposal_id)
    )
    proposal = result.scalar_one_or_none()
    
    if not proposal:
        raise HTTPException(
            status_code=404,
            detail=f"Proposal {decision.proposal_id} not found",
        )
    
    # Validate decision type
    try:
        decision_type_enum = DecisionType(decision.decision_type)
        decision_source_enum = DecisionSource(decision.decision_source)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Create decision record
    human_decision = HumanDecision(
        proposal_id=decision.proposal_id,
        decision_type=decision_type_enum,
        decision_source=decision_source_enum,
        reasoning=decision.reasoning,
        modified_action=decision.modified_action,
    )
    
    db.add(human_decision)
    await db.commit()
    await db.refresh(human_decision)
    
    logger.info(f"Decision created: {human_decision.id}")
    
    # TODO: Trigger graph resume
    
    return HumanDecisionResponse.from_orm(human_decision)


@router.get(
    "/proposal/{proposal_id}",
    summary="Get decisions for a proposal",
)
async def get_proposal_decisions(
    proposal_id: UUID,
    db: AsyncSession = Depends(get_db),
    identity: dict = Depends(get_authenticated_identity),
):
    """
    Get all decisions made for a specific proposal.
    """
    logger.info(f"Getting decisions for proposal {proposal_id}")
    
    result = await db.execute(
        select(HumanDecision).where(HumanDecision.proposal_id == proposal_id)
    )
    decisions = result.scalars().all()
    
    return {
        "proposal_id": str(proposal_id),
        "decisions": [
            HumanDecisionResponse.from_orm(d) for d in decisions
        ],
    }
