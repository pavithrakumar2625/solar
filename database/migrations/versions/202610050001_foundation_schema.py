"""foundation schema

Revision ID: 202610050001
Revises:
Create Date: 2026-10-05 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202610050001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "sites",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("country", sa.String(length=80), nullable=True),
        sa.Column("timezone", sa.String(length=80), nullable=False),
        sa.Column("latitude", sa.Numeric(precision=9, scale=6), nullable=True),
        sa.Column("longitude", sa.Numeric(precision=9, scale=6), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sites_organization_id", "sites", ["organization_id"])
    op.create_table(
        "plants",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("site_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("capacity_mw", sa.Numeric(precision=12, scale=3), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("commissioning_date", sa.Date(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["site_id"], ["sites.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_plants_site_id", "plants", ["site_id"])
    op.create_index("ix_plants_status", "plants", ["status"])
    op.create_table(
        "telemetry_readings",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("plant_id", sa.Integer(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("actual_generation_mw", sa.Numeric(precision=12, scale=3), nullable=False),
        sa.Column("expected_generation_mw", sa.Numeric(precision=12, scale=3), nullable=True),
        sa.Column("irradiance_wm2", sa.Numeric(precision=12, scale=3), nullable=True),
        sa.Column("module_temperature_c", sa.Numeric(precision=8, scale=3), nullable=True),
        sa.Column("availability_pct", sa.Numeric(precision=6, scale=3), nullable=True),
        sa.Column("performance_ratio", sa.Numeric(precision=6, scale=4), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["plant_id"], ["plants.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_telemetry_readings_plant_time",
        "telemetry_readings",
        ["plant_id", "recorded_at"],
    )
    op.create_index("ix_telemetry_readings_recorded_at", "telemetry_readings", ["recorded_at"])


def downgrade() -> None:
    op.drop_index("ix_telemetry_readings_recorded_at", table_name="telemetry_readings")
    op.drop_index("ix_telemetry_readings_plant_time", table_name="telemetry_readings")
    op.drop_table("telemetry_readings")
    op.drop_index("ix_plants_status", table_name="plants")
    op.drop_index("ix_plants_site_id", table_name="plants")
    op.drop_table("plants")
    op.drop_index("ix_sites_organization_id", table_name="sites")
    op.drop_table("sites")
    op.drop_table("organizations")
