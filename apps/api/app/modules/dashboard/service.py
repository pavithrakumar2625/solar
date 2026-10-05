"""Database-backed dashboard summary queries."""

from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.assets import Plant, TelemetryReading
from app.modules.dashboard.schemas import (
    DashboardMetric,
    DashboardSummary,
    HealthDistribution,
    PlantPerformance,
)


def _float(value: Decimal | int | None) -> float:
    return float(value or 0)


def _format_mw(value: Decimal | int | None) -> str:
    return f"{_float(value):,.1f} MW"


def _format_count(value: int | None) -> str:
    return f"{value or 0:,}"


async def build_dashboard_summary(session: AsyncSession) -> DashboardSummary:
    """Build the overview dashboard from persisted database state."""
    plant_count = await session.scalar(select(func.count(Plant.id)))
    total_capacity = await session.scalar(select(func.coalesce(func.sum(Plant.capacity_mw), 0)))

    latest_readings = (
        select(
            TelemetryReading.plant_id,
            func.max(TelemetryReading.recorded_at).label("recorded_at"),
        )
        .group_by(TelemetryReading.plant_id)
        .subquery()
    )

    generation_totals = await session.execute(
        select(
            func.coalesce(func.sum(TelemetryReading.actual_generation_mw), 0),
            func.coalesce(func.sum(TelemetryReading.expected_generation_mw), 0),
            func.count(TelemetryReading.id),
        ).join(
            latest_readings,
            and_(
                TelemetryReading.plant_id == latest_readings.c.plant_id,
                TelemetryReading.recorded_at == latest_readings.c.recorded_at,
            ),
        )
    )
    actual_generation, expected_generation, latest_count = generation_totals.one()

    data_status = "ready" if plant_count else "empty"
    if not plant_count:
        message = "No plants are stored in PostgreSQL yet. Add sites, plants, and telemetry to populate the dashboard."
    elif latest_count == 0:
        message = "Plants exist, but no telemetry readings are available yet."
    else:
        message = "Dashboard summary is built from PostgreSQL asset and telemetry records."

    generation_gap = max(_float(expected_generation) - _float(actual_generation), 0)
    generation_gap_pct = (
        generation_gap / _float(expected_generation) * 100 if _float(expected_generation) else 0
    )

    metrics = [
        DashboardMetric(
            label="Total Plants",
            value=_format_count(plant_count),
            detail="Stored in PostgreSQL",
            tone="green" if plant_count else "muted",
        ),
        DashboardMetric(
            label="Total Capacity",
            value=_format_mw(total_capacity),
            detail="From plant records",
            tone="blue",
        ),
        DashboardMetric(
            label="Current Generation",
            value=_format_mw(actual_generation),
            detail="Latest reading per plant",
            tone="green" if latest_count else "muted",
        ),
        DashboardMetric(
            label="Expected Generation",
            value=_format_mw(expected_generation),
            detail="Latest reading per plant",
            tone="blue" if latest_count else "muted",
        ),
        DashboardMetric(
            label="Generation Gap",
            value=_format_mw(int(generation_gap)),
            detail=f"{generation_gap_pct:.1f}% below expected" if latest_count else "Telemetry required",
            tone="red" if generation_gap > 0 else "green",
        ),
        DashboardMetric(
            label="Active Anomalies",
            value="0",
            detail="Anomaly module not implemented",
            tone="muted",
        ),
        DashboardMetric(
            label="Open Maintenance",
            value="0",
            detail="Maintenance module not implemented",
            tone="muted",
        ),
    ]

    plant_rows = await session.execute(
        select(
            Plant.id,
            Plant.name,
            Plant.capacity_mw,
            TelemetryReading.actual_generation_mw,
            TelemetryReading.expected_generation_mw,
        )
        .outerjoin(
            latest_readings,
            Plant.id == latest_readings.c.plant_id,
        )
        .outerjoin(
            TelemetryReading,
            and_(
                TelemetryReading.plant_id == Plant.id,
                TelemetryReading.recorded_at == latest_readings.c.recorded_at,
            ),
        )
        .order_by(Plant.capacity_mw.desc(), Plant.name.asc())
        .limit(5)
    )

    plants: list[PlantPerformance] = []
    health = HealthDistribution(healthy=0, warning=0, critical=0)
    for row in plant_rows.all():
        expected = _float(row.expected_generation_mw)
        actual = _float(row.actual_generation_mw)
        performance_pct = actual / expected * 100 if expected else None

        if performance_pct is not None:
            if performance_pct >= 90:
                health.healthy += 1
            elif performance_pct >= 75:
                health.warning += 1
            else:
                health.critical += 1

        plants.append(
            PlantPerformance(
                id=row.id,
                name=row.name,
                capacity_mw=_float(row.capacity_mw),
                current_generation_mw=actual if row.actual_generation_mw is not None else None,
                expected_generation_mw=expected if row.expected_generation_mw is not None else None,
                performance_pct=round(performance_pct, 1) if performance_pct is not None else None,
            )
        )

    return DashboardSummary(
        generated_at=datetime.now(UTC),
        data_status=data_status,
        message=message,
        metrics=metrics,
        plants=plants,
        health=health,
        anomalies=[],
        loss_breakdown=[],
    )
