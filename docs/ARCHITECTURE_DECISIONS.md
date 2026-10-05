# SolarRecover AI — Architecture Decisions

> **Status**: LOCKED  
> **Last Updated**: 2026-10-04  
> **Authority**: User requirements override Product Brief where they differ.

---

## AD-001: Frontend Framework

| Attribute | Value |
|-----------|-------|
| **Decision** | Next.js + TypeScript |
| **Status** | LOCKED |
| **Rationale** | Explicitly locked by product owner. Next.js provides SSR/SSG for SEO on marketing pages, file-based routing, API routes, and optimized production builds. |
| **Product Brief Suggested** | React + Vite + TypeScript + Tailwind CSS |
| **Override Reason** | User explicitly locked Next.js. Tailwind not specified — using vanilla CSS per user system prompt preferences. |
| **Deployment Target** | Cloudflare Pages (static export / edge) |

## AD-002: Frontend Styling

| Attribute | Value |
|-----------|-------|
| **Decision** | Vanilla CSS (custom design system) |
| **Status** | LOCKED |
| **Rationale** | User preferences specify vanilla CSS unless Tailwind explicitly requested. Professional, premium industrial design without framework dependency. |
| **Notes** | CSS custom properties for theming. Design system tokens for consistency. |

## AD-003: Backend Framework

| Attribute | Value |
|-----------|-------|
| **Decision** | Python + FastAPI |
| **Status** | LOCKED |
| **Rationale** | Explicitly locked. FastAPI provides async support, automatic OpenAPI docs, Pydantic validation, and Python ML ecosystem access. |
| **Architecture** | Modular Monolith — internally modular, extractable to microservices later |

## AD-004: Backend Architecture Pattern

| Attribute | Value |
|-----------|-------|
| **Decision** | FastAPI Modular Monolith |
| **Status** | LOCKED |
| **Rationale** | Single deployable unit with clean internal module boundaries. Appropriate for 1–10 users, 10–100 plants. Extractable later. |
| **Modules** | `/auth`, `/organizations`, `/users`, `/sites`, `/plants`, `/assets`, `/digital-twin`, `/ingestion`, `/telemetry`, `/weather`, `/analytics`, `/performance`, `/anomalies`, `/diagnosis`, `/losses`, `/financial`, `/recovery`, `/maintenance`, `/inspections`, `/copilot`, `/reports`, `/notifications`, `/audit`, `/ml`, `/system` |

## AD-005: Primary Database

| Attribute | Value |
|-----------|-------|
| **Decision** | PostgreSQL |
| **Status** | LOCKED |
| **Rationale** | Robust relational DB with JSON support, full-text search, and extensions ecosystem. Free tier available on multiple providers. |
| **ORM** | SQLAlchemy 2.0 (async) + Alembic migrations |

## AD-006: Time-Series Strategy

| Attribute | Value |
|-----------|-------|
| **Decision** | TimescaleDB-compatible PostgreSQL schema |
| **Status** | LOCKED |
| **Rationale** | Free-tier providers may not support TimescaleDB extension. Architecture uses PostgreSQL-native time-series patterns (BRIN indexes, partitioning, efficient timestamp indexing) with an abstract data-access layer that can switch to TimescaleDB hypertables later. |
| **Migration Path** | Abstract repository pattern → swap to TimescaleDB when infrastructure allows |
| **Limitation** | Documented — no hypertable compression or continuous aggregates until TimescaleDB is available |

## AD-007: Caching & Background Jobs

| Attribute | Value |
|-----------|-------|
| **Decision** | Redis (optional) + Python background workers |
| **Status** | DECIDED |
| **Rationale** | Product Brief recommends Redis. For zero-budget MVP, use in-process background tasks (FastAPI BackgroundTasks + asyncio) with optional Redis/Celery upgrade path. |
| **MVP Implementation** | `asyncio` task queue with database-backed job status |
| **Production Path** | Redis + Celery/ARQ when infrastructure budget allows |

## AD-008: ML Stack

| Attribute | Value |
|-----------|-------|
| **Decision** | Pandas + NumPy + scikit-learn + XGBoost/LightGBM |
| **Status** | LOCKED |
| **Rationale** | Classical ML and statistical methods for reliability. PyTorch only if justified by data volume and task complexity. |
| **Initial Models** | Statistical baselines, Isolation Forest, tree-based regressors |
| **Deep Learning** | Not in MVP — insufficient labeled PV fault data for reliable DL |

## AD-009: AI / LLM Architecture

| Attribute | Value |
|-----------|-------|
| **Decision** | LLM API + tool/function calling + structured outputs |
| **Status** | LOCKED |
| **Rationale** | LLM is the interpretation/explanation layer, NOT the numerical prediction engine. Numerical truth comes from ML/physics/statistical services. LLM calls backend tools to retrieve data. |
| **Provider** | Abstracted `AIProvider` interface — supports Google Gemini (free tier), OpenAI, etc. |
| **Separation** | Numerical Intelligence (Python/ML) ↔ Diagnostic Intelligence (rules + ML) ↔ Generative Intelligence (LLM) |

## AD-010: Weather Integration

| Attribute | Value |
|-----------|-------|
| **Decision** | Abstracted `WeatherProvider` interface |
| **Status** | LOCKED |
| **Rationale** | Multiple free weather APIs exist (Open-Meteo, OpenWeatherMap free tier). Provider must be swappable. |
| **MVP Provider** | Open-Meteo (completely free, no API key required) |

## AD-011: File/Object Storage

| Attribute | Value |
|-----------|-------|
| **Decision** | Abstracted storage interface — local filesystem for MVP |
| **Status** | DECIDED |
| **Rationale** | Zero-budget constraint. Local storage with abstract interface that supports S3/R2/GCS later. |
| **MVP** | Local filesystem with configurable base path |
| **Production Path** | Cloudflare R2 (free tier: 10GB) or S3-compatible |

## AD-012: Authentication

| Attribute | Value |
|-----------|-------|
| **Decision** | JWT-based authentication with bcrypt password hashing |
| **Status** | DECIDED |
| **Rationale** | Self-hosted auth for zero-budget. No external auth provider dependency. Supports RBAC, org isolation, API tokens. |
| **Libraries** | `python-jose` (JWT), `passlib[bcrypt]` (hashing), `python-multipart` (forms) |

## AD-013: Deployment — Frontend

| Attribute | Value |
|-----------|-------|
| **Decision** | Cloudflare Pages |
| **Status** | LOCKED |
| **Rationale** | Explicitly locked. Next.js static export or edge deployment on Cloudflare. Free tier: unlimited sites, bandwidth. |

## AD-014: Deployment — Backend

| Attribute | Value |
|-----------|-------|
| **Decision** | Dockerized container on free-tier cloud |
| **Status** | DECIDED |
| **Rationale** | Dockerfile + docker-compose.yml. Deployable to Render (free), Railway (trial), Fly.io (free tier), or any Docker host. |
| **Local** | `docker-compose up` for full local stack |

## AD-015: Database Hosting

| Attribute | Value |
|-----------|-------|
| **Decision** | Free-tier PostgreSQL provider |
| **Status** | DECIDED |
| **Candidates** | Neon (free tier: 512MB), Supabase (free: 500MB), Railway (trial), or local Docker PostgreSQL |
| **Limitation** | Free-tier storage limits documented. TimescaleDB not available on most free tiers. |

## AD-016: API Versioning

| Attribute | Value |
|-----------|-------|
| **Decision** | URL-based versioning: `/api/v1/...` |
| **Status** | LOCKED |
| **Rationale** | Explicit, clear, REST-standard versioning. |

## AD-017: Real-Time / Near-Real-Time

| Attribute | Value |
|-----------|-------|
| **Decision** | Server-Sent Events (SSE) for MVP, WebSocket upgrade path |
| **Status** | DECIDED |
| **Rationale** | SSE is simpler, works through proxies, sufficient for notifications and job progress. WebSocket for Copilot streaming. |

## AD-018: CI/CD

| Attribute | Value |
|-----------|-------|
| **Decision** | GitHub Actions |
| **Status** | DECIDED |
| **Rationale** | Free for public repos, generous free tier for private repos. Lint, test, build, Docker build. |

## AD-019: Charting Library

| Attribute | Value |
|-----------|-------|
| **Decision** | Recharts (React-based) |
| **Status** | DECIDED |
| **Rationale** | Product Brief suggests Recharts/ECharts. Recharts integrates natively with React/Next.js. Composable, responsive. ECharts available as upgrade for complex visualizations. |

## AD-020: Project Structure

| Attribute | Value |
|-----------|-------|
| **Decision** | Monorepo with clear separation |
| **Status** | LOCKED |
| **Structure** | `apps/web/` (Next.js), `apps/api/` (FastAPI), `ml/` (ML pipeline), `database/` (migrations/seeds), `packages/` (shared contracts), `infrastructure/` (Docker/deploy), `docs/`, `tests/`, `scripts/` |

---

## Conflict Log

| Date | Issue | Resolution |
|------|-------|------------|
| 2026-10-04 | Product Brief recommends React+Vite+Tailwind; User locks Next.js+TypeScript+Vanilla CSS | User's locked decisions take precedence. No technical incompatibility. |
| 2026-10-04 | Product Brief recommends Redis; Zero-budget constraint | Use async in-process job queue for MVP with Redis upgrade path documented. |
| 2026-10-04 | TimescaleDB recommended but free-tier providers don't support it | PostgreSQL-native time-series schema with TimescaleDB migration path preserved. |

---

## Decision Change Protocol

1. If a genuine technical incompatibility is discovered, STOP and explain the conflict.
2. Do NOT silently substitute technologies.
3. Document any necessary deviation with rationale.
4. Get explicit approval before changing a LOCKED decision.
