"""
Graph Runs API Router

Endpoints for viewing graph run history and status.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from db import get_db
from db.models import GraphRun
from api.schemas import GraphRunResponse, GraphRunList
from app.auth import get_authenticated_identity
from app.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get(
    "/",
    response_model=GraphRunList,
    summary="List all graph runs",
)
async def list_graph_runs(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    identity: dict = Depends(get_authenticated_identity),
) -> GraphRunList:
    """
    List all graph runs with pagination.
    """
    logger.info("Listing graph runs")
    
    # Get total count
    count_result = await db.execute(select(func.count()).select_from(GraphRun))
    total = count_result.scalar() or 0
    
    # Get paginated results
    result = await db.execute(
        select(GraphRun)
        .order_by(GraphRun.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    graph_runs = result.scalars().all()
    
    return GraphRunList(
        graph_runs=[GraphRunResponse.from_orm(gr) for gr in graph_runs],
        total=total,
    )


@router.get(
    "/{graph_run_id}",
    response_model=GraphRunResponse,
    summary="Get a specific graph run",
)
async def get_graph_run(
    graph_run_id: UUID,
    db: AsyncSession = Depends(get_db),
    identity: dict = Depends(get_authenticated_identity),
) -> GraphRunResponse:
    """
    Get detailed information about a specific graph run.
    """
    logger.info(f"Getting graph run {graph_run_id}")
    
    result = await db.execute(
        select(GraphRun).where(GraphRun.id == graph_run_id)
    )
    graph_run = result.scalar_one_or_none()
    
    if not graph_run:
        raise HTTPException(status_code=404, detail="Graph run not found")
    
    return GraphRunResponse.from_orm(graph_run)
