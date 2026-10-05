# SolarRecover AI — Implementation Plan

> **Last Updated**: 2026-10-04  
> **Total Phases**: 22 (0–21)  
> **Current Phase**: 1  

---

## Phase 0: Product Understanding & Architecture Validation ✅

**Status**: COMPLETE  
**Deliverables**:
- [x] Read Product Brief (11 pages, 19 sections)
- [x] Read reference UI mockup
- [x] Identify architecture decisions from user requirements
- [x] Create `/docs/ARCHITECTURE_DECISIONS.md`
- [x] Validate no conflicts between Product Brief and locked decisions
- [x] Document 3 conflicts and their resolutions

---

## Phase 1: Repository & Development Foundation

**Status**: IN PROGRESS  
**Goal**: Create the complete project skeleton with all config files, dev tooling, and both app scaffolds.

### Tasks:
- [ ] Create monorepo directory structure
- [ ] Initialize Next.js app (`apps/web/`)
- [ ] Initialize FastAPI app (`apps/api/`)
- [ ] Create ML directory structure (`ml/`)
- [ ] Create database directory structure (`database/`)
- [ ] Create shared packages structure (`packages/`)
- [ ] Create infrastructure configs (`infrastructure/`)
- [ ] Create Docker configs (Dockerfile, docker-compose.yml)
- [ ] Create `.env.example`
- [ ] Create `.gitignore`
- [ ] Create `README.md`
- [ ] Create GitHub Actions CI/CD config
- [ ] Set up Python dependencies (requirements.txt / pyproject.toml)
- [ ] Set up ESLint + TypeScript config for frontend
- [ ] Verify local dev environment works
- [ ] Create initial docs files

### Definition of Done:
- `docker-compose up` starts all services
- `npm run dev` starts frontend
- `uvicorn` starts backend
- `/health` and `/ready` endpoints respond
- TypeScript compiles without errors
- Python linting passes

---

## Phase 2: Database Schema & Migrations

**Status**: NOT STARTED  
**Goal**: Design and implement the complete normalized PostgreSQL schema.

### Tasks:
- [ ] Design core entity schema (organizations, users, roles)
- [ ] Design asset hierarchy schema (sites → plants → blocks → inverters → strings → modules)
- [ ] Design telemetry/time-series schema with efficient indexing
- [ ] Design analytics schema (anomalies, diagnoses, losses)
- [ ] Design maintenance schema (work orders, inspections)
- [ ] Design ML schema (models, predictions, metrics)
- [ ] Design AI/Copilot schema (sessions, messages, tool calls)
- [ ] Design support schema (notifications, reports, audit logs)
- [ ] Create Alembic migration environment
- [ ] Write initial migration
- [ ] Add seed data for development/demo
- [ ] Document schema in `/docs/DATABASE.md`

### Definition of Done:
- All migrations run successfully
- Schema supports full asset hierarchy
- Time-series tables have proper indexing
- Foreign keys and constraints enforced
- Seed data loads successfully

---

## Phase 3: Authentication & Authorization

**Status**: NOT STARTED  
**Goal**: JWT auth, RBAC, organization isolation.

### Tasks:
- [ ] Implement user registration/login API
- [ ] Implement JWT token management (access + refresh)
- [ ] Implement password hashing (bcrypt)
- [ ] Implement RBAC middleware
- [ ] Implement organization isolation
- [ ] Create auth UI (login, register, forgot password)
- [ ] Create protected route middleware (frontend)
- [ ] Add auth tests
- [ ] Add security tests (unauthorized access, tenant isolation)

---

## Phase 4: Organization / Site / Plant / Asset Hierarchy

**Status**: NOT STARTED  
**Goal**: CRUD for the complete PV asset hierarchy.

### Tasks:
- [ ] Organization CRUD API + UI
- [ ] Site CRUD API + UI
- [ ] Plant CRUD API + UI
- [ ] Block/Inverter/String/Module CRUD API + UI
- [ ] Asset hierarchy navigation UI
- [ ] Asset detail views
- [ ] Search and filtering
- [ ] Tests

---

## Phase 5: Data Ingestion Pipeline

**Status**: NOT STARTED  
**Goal**: CSV upload → schema detection → validation → mapping → normalization → storage.

### Tasks:
- [ ] CSV upload endpoint with file validation
- [ ] Schema detection engine
- [ ] Column mapping interface (frontend)
- [ ] Data validation pipeline
- [ ] Unit normalization
- [ ] Timestamp normalization
- [ ] Missing value analysis
- [ ] Duplicate detection
- [ ] Data quality scoring
- [ ] Background job processing
- [ ] Job status tracking + progress UI
- [ ] Ingestion history/audit
- [ ] Tests

---

## Phase 6: Digital Twin

**Status**: NOT STARTED  
**Goal**: Core Digital Twin system representing asset state.

### Tasks:
- [ ] Digital Twin data model (physical, digital, historical, relationship, context state)
- [ ] Twin state calculation engine
- [ ] Twin update on new telemetry
- [ ] Twin API endpoints
- [ ] Twin UI — hierarchy navigation
- [ ] Twin UI — asset state display
- [ ] Twin UI — historical state timeline
- [ ] Tests

---

## Phase 7: Expected Performance Engine

**Status**: NOT STARTED  
**Goal**: Calculate expected power output based on environmental and system factors.

### Tasks:
- [ ] Feature engineering (irradiance, temperature, capacity, seasonality, etc.)
- [ ] Statistical baseline model
- [ ] ML regression model (XGBoost/LightGBM)
- [ ] Model training pipeline
- [ ] Model evaluation (MAE, RMSE, MAPE, R²)
- [ ] Prediction API
- [ ] Expected vs actual comparison service
- [ ] Performance visualization UI
- [ ] Model versioning
- [ ] Tests (including temporal validation, leakage checks)

---

## Phase 8: Anomaly Detection

**Status**: NOT STARTED  
**Goal**: Real ML anomaly detection pipeline.

### Tasks:
- [ ] Statistical baseline detection (z-score, rolling stats)
- [ ] Residual analysis detection
- [ ] Isolation Forest implementation
- [ ] Anomaly scoring and severity
- [ ] Anomaly API with full evidence
- [ ] Anomaly timeline UI
- [ ] Anomaly detail UI
- [ ] Model evaluation (Precision, Recall, F1, false alarm rate)
- [ ] Tests

---

## Phase 9: Root Cause Engine

**Status**: NOT STARTED  
**Goal**: Evidence-backed probable cause hypotheses.

### Tasks:
- [ ] Rule-based diagnostic engine
- [ ] Evidence collection service
- [ ] Confidence scoring
- [ ] Multi-hypothesis generation
- [ ] Diagnosis API
- [ ] Diagnosis UI with evidence display
- [ ] Tests

---

## Phase 10: Energy Loss Attribution

**Status**: NOT STARTED  
**Goal**: Estimate and attribute lost generation.

### Tasks:
- [ ] Gap calculation (expected - actual)
- [ ] Loss attribution engine (soiling, shading, inverter, degradation, etc.)
- [ ] Uncertainty estimation
- [ ] Loss API
- [ ] Loss visualization UI
- [ ] Tests

---

## Phase 11: Financial Impact

**Status**: NOT STARTED  
**Goal**: Convert energy loss to financial impact.

### Tasks:
- [ ] Tariff/PPA configuration
- [ ] Financial calculation engine
- [ ] Currency support
- [ ] Financial API
- [ ] Financial dashboard UI
- [ ] Tests

---

## Phase 12: Recovery Simulator

**Status**: NOT STARTED  
**Goal**: Scenario-based recovery simulation.

### Tasks:
- [ ] Scenario definition (clean, inspect, replace, etc.)
- [ ] Recovery estimation engine
- [ ] Cost estimation
- [ ] Payback calculation
- [ ] Scenario comparison API
- [ ] Scenario comparison UI
- [ ] Tests

---

## Phase 13: Maintenance Intelligence

**Status**: NOT STARTED  
**Goal**: Explainable priority engine + work orders.

### Tasks:
- [ ] Priority scoring engine (energy loss, financial, risk, severity, etc.)
- [ ] Priority explanation generation
- [ ] Work order management
- [ ] Maintenance API
- [ ] Maintenance dashboard UI
- [ ] Tests

---

## Phase 14: Technician Mode

**Status**: NOT STARTED  
**Goal**: Simplified technician interface.

### Tasks:
- [ ] Technician-specific views
- [ ] Inspection checklists
- [ ] Work status recording
- [ ] Before/after capture
- [ ] Technician notes
- [ ] Resolution recording
- [ ] Tests

---

## Phase 15: AI Solar Copilot

**Status**: NOT STARTED  
**Goal**: Domain-aware AI assistant.

### Tasks:
- [ ] AIProvider interface
- [ ] Tool/function definitions for backend data retrieval
- [ ] Copilot session management
- [ ] Structured output handling
- [ ] Chat UI with streaming
- [ ] Evidence citation in responses
- [ ] AI trust contract enforcement
- [ ] Tests (groundedness, hallucination, tool calling)

---

## Phase 16: Reports & Notifications

**Status**: NOT STARTED  
**Goal**: Generate data-driven reports and push notifications.

### Tasks:
- [ ] Report generation engine (performance, anomaly, loss, financial, recovery, maintenance, health)
- [ ] Report API
- [ ] Report UI
- [ ] Notification system
- [ ] Notification preferences
- [ ] Email notifications (optional)
- [ ] SSE for real-time updates
- [ ] Tests

---

## Phase 17: Asset Memory & Feedback

**Status**: NOT STARTED  
**Goal**: Close the loop — maintenance outcomes improve asset intelligence.

### Tasks:
- [ ] Asset history tracking
- [ ] Before/action/after/outcome recording
- [ ] Feedback event recording
- [ ] Asset memory API
- [ ] Asset timeline UI
- [ ] Model adaptation hooks
- [ ] Tests

---

## Phase 18: Integration & Real-Time Architecture

**Status**: NOT STARTED  
**Goal**: Wire everything together, SSE/WebSocket for real-time updates.

---

## Phase 19: Testing & Security Hardening

**Status**: NOT STARTED  
**Goal**: Comprehensive test suite + security hardening.

---

## Phase 20: Observability & Deployment

**Status**: NOT STARTED  
**Goal**: Logging, monitoring, health checks, production deployment configs.

---

## Phase 21: Production/Demo Validation

**Status**: NOT STARTED  
**Goal**: Full end-to-end validation of the complete workflow.

---

## Dependency Notes

- Phase 7 depends on Phase 5 (needs telemetry data)
- Phase 8 depends on Phase 7 (needs expected performance for residual analysis)
- Phase 9 depends on Phase 8 (needs anomalies to diagnose)
- Phase 10 depends on Phase 7+8 (needs expected vs actual + anomaly context)
- Phase 11 depends on Phase 10 (needs loss estimates)
- Phase 12 depends on Phase 10+11 (needs loss + financial context)
- Phase 13 depends on Phase 8+10+11 (needs anomaly + loss + financial data)
- Phase 15 depends on Phase 7–13 (needs backend tools to call)
- All phases depend on Phase 2 (database) and Phase 3 (auth)
