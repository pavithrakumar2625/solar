"""
SolarRecover AI — FastAPI Application
Vendor-Neutral Solar Asset Intelligence & Digital Twin Platform
"""
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from app.api.health import health_router
from app.api.v1.router import api_v1_router
from app.core.config import settings
from app.core.database import engine
from app.core.logging import setup_logging


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan — startup and shutdown events."""
    setup_logging()

    yield

    await engine.dispose()


def create_app() -> FastAPI:
    """Application factory."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "SolarRecover AI — Vendor-Neutral Solar Asset Intelligence & Digital Twin Platform. "
            "Transforms PV operational data into explainable energy-loss diagnosis, financial impact "
            "analysis, recovery simulation, and actionable maintenance decisions."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(health_router)
    app.include_router(api_v1_router, prefix="/api/v1")

    return app


app = create_app()
