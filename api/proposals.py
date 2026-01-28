"""
Proposals API Router

Endpoints for viewing and managing agent proposals.

Design principles:
- Read-mostly operations
- Authentication required
- Pagination support
- Filtering support
"""

from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from db import get_db
from db.models import Proposal, ProposalStatus
from api.schemas import ProposalResponse, ProposalList
from app.auth import get_authenticated_identity
from app.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get(
    "/",
    response_model=ProposalList,
    summary="List all proposals",
)
async def list_proposals(
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(50, ge=1, le=100, description="Max results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: AsyncSession = Depends(get_db),
    identity: dict = Depends(get_authenticated_identity),
) -> ProposalList:
    """
    List all proposals with optional filtering.
    
    Supports:
    - Status filtering
    - Pagination
    - Sorting by created_at (newest first)
    """
    logger.info("Listing proposals", extra={"status": status, "limit": limit})
    
    # Build query
    query = select(Proposal)
    
    if status:
        try:
            status_enum = ProposalStatus(status)
            query = query.where(Proposal.status == status_enum)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status: {status}",
            )
    
    # Get total count
    count_query = select(func.count()).select_from(query.alias())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Get paginated results
    query = query.order_by(Proposal.created_at.desc()).limit(limit).offset(offset)
    result = await db.execute(query)
    proposals = result.scalars().all()
    
    return ProposalList(
        proposals=[ProposalResponse.from_orm(p) for p in proposals],
        total=total,
    )


@router.get(
    "/{proposal_id}",
    response_model=ProposalResponse,
    summary="Get a specific proposal",
)
async def get_proposal(
    proposal_id: UUID,
    db: AsyncSession = Depends(get_db),
    identity: dict = Depends(get_authenticated_identity),
) -> ProposalResponse:
    """
    Get detailed information about a specific proposal.
    """
    logger.info(f"Getting proposal {proposal_id}")
    
    result = await db.execute(
        select(Proposal).where(Proposal.id == proposal_id)
    )
    proposal = result.scalar_one_or_none()
    
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    return ProposalResponse.from_orm(proposal)
