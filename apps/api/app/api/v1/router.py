"""
SolarRecover AI — API v1 Router
Aggregates all module routers under /api/v1 prefix.
"""
from fastapi import APIRouter

from app.modules.dashboard.router import router as dashboard_router

api_v1_router = APIRouter()

# Module routers will be added here as each phase is implemented:
#
# from app.modules.auth.router import router as auth_router
# from app.modules.organizations.router import router as organizations_router
# from app.modules.sites.router import router as sites_router
# from app.modules.plants.router import router as plants_router
# from app.modules.assets.router import router as assets_router
# from app.modules.digital_twin.router import router as twin_router
# from app.modules.ingestion.router import router as ingestion_router
# from app.modules.telemetry.router import router as telemetry_router
# from app.modules.weather.router import router as weather_router
# from app.modules.analytics.router import router as analytics_router
# from app.modules.performance.router import router as performance_router
# from app.modules.anomalies.router import router as anomalies_router
# from app.modules.diagnosis.router import router as diagnosis_router
# from app.modules.losses.router import router as losses_router
# from app.modules.financial.router import router as financial_router
# from app.modules.recovery.router import router as recovery_router
# from app.modules.maintenance.router import router as maintenance_router
# from app.modules.inspections.router import router as inspections_router
# from app.modules.copilot.router import router as copilot_router
# from app.modules.reports.router import router as reports_router
# from app.modules.notifications.router import router as notifications_router
# from app.modules.audit.router import router as audit_router
# from app.modules.system.router import router as system_router
#
api_v1_router.include_router(dashboard_router)
# api_v1_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
# api_v1_router.include_router(organizations_router, prefix="/organizations", tags=["Organizations"])
# ... etc.


@api_v1_router.get("/", tags=["API"])
async def api_root():
    """API v1 root — returns available endpoints."""
    return {
        "api": "SolarRecover AI",
        "version": "v1",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "ready": "/ready",
            "docs": "/docs",
            "dashboard_summary": "/api/v1/dashboard/summary",
            "openapi": "/openapi.json",
        },
    }
