"""Core asset and telemetry tables for the SolarRecover AI foundation."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, Index, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Organization(Base):
    """Tenant or operating company that owns solar sites."""

    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    sites: Mapped[list[Site]] = relationship(back_populates="organization")


class Site(Base):
    """Physical solar site or campus."""

    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    country: Mapped[str | None] = mapped_column(String(80))
    timezone: Mapped[str] = mapped_column(String(80), default="UTC", nullable=False)
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6))
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    organization: Mapped[Organization] = relationship(back_populates="sites")
    plants: Mapped[list[Plant]] = relationship(back_populates="site")

    __table_args__ = (Index("ix_sites_organization_id", "organization_id"),)


class Plant(Base):
    """Generation plant under a site."""

    __tablename__ = "plants"

    id: Mapped[int] = mapped_column(primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    capacity_mw: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="active", nullable=False)
    commissioning_date: Mapped[date | None] = mapped_column(Date)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    site: Mapped[Site] = relationship(back_populates="plants")
    telemetry_readings: Mapped[list[TelemetryReading]] = relationship(back_populates="plant")

    __table_args__ = (
        Index("ix_plants_site_id", "site_id"),
        Index("ix_plants_status", "status"),
    )


class TelemetryReading(Base):
    """Plant-level time-series telemetry used by dashboard and analytics APIs."""

    __tablename__ = "telemetry_readings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    plant_id: Mapped[int] = mapped_column(ForeignKey("plants.id"), nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    actual_generation_mw: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    expected_generation_mw: Mapped[Decimal | None] = mapped_column(Numeric(12, 3))
    irradiance_wm2: Mapped[Decimal | None] = mapped_column(Numeric(12, 3))
    module_temperature_c: Mapped[Decimal | None] = mapped_column(Numeric(8, 3))
    availability_pct: Mapped[Decimal | None] = mapped_column(Numeric(6, 3))
    performance_ratio: Mapped[Decimal | None] = mapped_column(Numeric(6, 4))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    plant: Mapped[Plant] = relationship(back_populates="telemetry_readings")

    __table_args__ = (
        Index("ix_telemetry_readings_plant_time", "plant_id", "recorded_at"),
        Index("ix_telemetry_readings_recorded_at", "recorded_at"),
    )
