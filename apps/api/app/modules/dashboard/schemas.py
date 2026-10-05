"""Response schemas for the dashboard API."""

from datetime import datetime

from pydantic import BaseModel, Field


class DashboardMetric(BaseModel):
    label: str
    value: str
    detail: str
    tone: str = Field(pattern="^(green|blue|orange|red|muted)$")


class PlantPerformance(BaseModel):
    id: int
    name: str
    capacity_mw: float
    current_generation_mw: float | None
    expected_generation_mw: float | None
    performance_pct: float | None


class HealthDistribution(BaseModel):
    healthy: int
    warning: int
    critical: int


class DashboardSummary(BaseModel):
    generated_at: datetime
    data_status: str = Field(pattern="^(empty|ready)$")
    message: str
    metrics: list[DashboardMetric]
    plants: list[PlantPerformance]
    health: HealthDistribution
    anomalies: list[str]
    loss_breakdown: list[str]
