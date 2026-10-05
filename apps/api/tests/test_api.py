"""API tests for the SolarRecover AI foundation."""

from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from typing import Any

from fastapi.testclient import TestClient

from app.core.database import get_db
from app.main import app
from app.modules.dashboard.schemas import DashboardSummary


def test_health_check() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_api_root_lists_dashboard_summary() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/")

    assert response.status_code == 200
    assert response.json()["endpoints"]["dashboard_summary"] == "/api/v1/dashboard/summary"


def test_readiness_returns_503_when_database_is_unavailable(monkeypatch: Any) -> None:
    from app.api import health as health_module

    class BrokenSessionFactory:
        async def __aenter__(self) -> "BrokenSessionFactory":
            raise RuntimeError("database unavailable")

        async def __aexit__(self, *_: object) -> None:
            return None

    monkeypatch.setattr(health_module, "async_session_factory", lambda: BrokenSessionFactory())

    with TestClient(app) as client:
        response = client.get("/ready")

    assert response.status_code == 503
    assert response.json()["status"] == "not_ready"
    assert response.json()["database"] == "unavailable"


def test_dashboard_summary_contract(monkeypatch: Any) -> None:
    from app.modules.dashboard import router as dashboard_router

    async def override_db() -> AsyncGenerator[object, None]:
        yield object()

    async def fake_summary(_: object) -> DashboardSummary:
        return DashboardSummary(
            generated_at=datetime.now(UTC),
            data_status="empty",
            message="No plants are stored in PostgreSQL yet.",
            metrics=[],
            plants=[],
            health={"healthy": 0, "warning": 0, "critical": 0},
            anomalies=[],
            loss_breakdown=[],
        )

    app.dependency_overrides[get_db] = override_db
    monkeypatch.setattr(dashboard_router, "build_dashboard_summary", fake_summary)

    try:
        with TestClient(app) as client:
            response = client.get("/api/v1/dashboard/summary")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["data_status"] == "empty"
    assert body["plants"] == []
