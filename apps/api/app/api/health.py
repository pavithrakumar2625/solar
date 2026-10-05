"""
SolarRecover AI — Health & Readiness Endpoints
"""
from datetime import UTC, datetime

from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from sqlalchemy import text

from app.core.config import settings
from app.core.database import async_session_factory

health_router = APIRouter(tags=["System"])


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    environment: str
    timestamp: str


class ReadinessResponse(BaseModel):
    status: str
    database: str
    timestamp: str


@health_router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Application health check — confirms the service is running."""
    return HealthResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.APP_ENV,
        timestamp=datetime.now(UTC).isoformat(),
    )


@health_router.get("/ready", response_model=ReadinessResponse)
async def readiness_check(response: Response) -> ReadinessResponse:
    """Readiness check — confirms dependencies are available."""
    db_status = "unknown"

    try:
        async with async_session_factory() as session:
            await session.execute(text("SELECT 1"))
            db_status = "connected"
    except Exception:
        db_status = "unavailable"

    overall = "ready" if db_status == "connected" else "not_ready"
    if overall != "ready":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return ReadinessResponse(
        status=overall,
        database=db_status,
        timestamp=datetime.now(UTC).isoformat(),
    )
