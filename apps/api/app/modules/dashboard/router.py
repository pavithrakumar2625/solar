"""Dashboard API routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.dashboard.schemas import DashboardSummary
from app.modules.dashboard.service import build_dashboard_summary

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummary)
async def dashboard_summary(db: Annotated[AsyncSession, Depends(get_db)]) -> DashboardSummary:
    """Return a database-backed overview summary for the frontend dashboard."""
    try:
        return await build_dashboard_summary(db)
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is unavailable or migrations have not been applied.",
        ) from exc
