# SolarRecover AI

> **Vendor-Neutral Solar Asset Intelligence & Digital Twin Platform**  
> Recover More. Power Tomorrow.

---

## Overview

SolarRecover AI transforms fragmented PV operational data into explainable energy-loss diagnosis, financial impact analysis, recovery simulation, and actionable maintenance decisions.

### Core Product Loop

```
OBSERVE → MODEL → DETECT → EXPLAIN → QUANTIFY → SIMULATE → ACT → MEASURE → LEARN
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js + TypeScript + Vanilla CSS |
| Backend | Python + FastAPI |
| Database | PostgreSQL (TimescaleDB-compatible) |
| ML | Pandas, NumPy, scikit-learn, XGBoost, LightGBM |
| AI | LLM API + Tool/Function Calling + Structured Outputs |
| Deployment | Docker + Cloudflare Pages (frontend) |

---

## Quick Start

### Prerequisites

- Node.js 20+
- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose (optional)

### Local Development

**1. Clone and configure:**
```bash
git clone https://github.com/your-org/solar-recover-ai.git
cd solar-recover-ai
cp .env.example .env
# Edit .env with your database credentials
```

**2. Start with Docker (recommended):**
```bash
docker-compose up -d
```

**3. Or start services individually:**

Backend:
```bash
cd apps/api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

Frontend:
```bash
cd apps/web
npm install
npm run dev
```

**4. Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

---

## Project Structure

```
solar-recover-ai/
├── apps/
│   ├── web/                    # Next.js frontend
│   └── api/                    # FastAPI backend
├── ml/                         # ML pipeline
│   ├── data/
│   ├── preprocessing/
│   ├── features/
│   ├── models/
│   ├── training/
│   ├── inference/
│   ├── evaluation/
│   └── monitoring/
├── database/
│   ├── migrations/
│   ├── seeds/
│   └── schema/
├── packages/
│   ├── contracts/
│   ├── shared/
│   └── config/
├── infrastructure/
│   ├── docker/
│   └── deployment/
├── docs/
├── tests/
├── scripts/
├── .github/
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [Architecture Decisions](docs/ARCHITECTURE_DECISIONS.md) | Locked technical decisions |
| [Implementation Plan](docs/IMPLEMENTATION_PLAN.md) | Phased build plan |
| [Progress](docs/PROGRESS.md) | Current implementation status |
| [Database](docs/DATABASE.md) | Schema documentation |
| [API](docs/API.md) | API reference |
| [AI/ML](docs/AI_ML.md) | ML architecture and evaluation |
| [Deployment](docs/DEPLOYMENT.md) | Deployment guide |

---

## License

Proprietary — All rights reserved.
