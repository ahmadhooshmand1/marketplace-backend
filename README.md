# Marketplace Backend API

Backend service for a multi-vendor online marketplace (inspired by Basalam), built with **FastAPI**, **PostgreSQL**, and **Raw SQL (`psycopg`)** using a layered architecture.

## Tech Stack
- **Framework:** FastAPI + Uvicorn
- **Database:** PostgreSQL 16 (Docker)
- **Database Driver:** `psycopg` (Raw SQL, no ORM)
- **Validation & Settings:** Pydantic v2 & `pydantic-settings`
- **Authentication:** JWT (`PyJWT`)
- **Package Manager:** `uv`

## Project Structure
```text
├── docs/
│   ├── api-design.md       # Full API specification (v1)
│   ├── erd-diagram.pdf     # Database ERD diagram
│   └── wireframes/         # UI wireframes
├── src/
│   ├── api/                # FastAPI routers & endpoints
│   ├── services/           # Business logic
│   ├── repositories/       # Raw SQL queries
│   ├── schemas/            # Pydantic request/response models
│   ├── connections/        # Database connection management
│   ├── utils/              # JWT & security helpers
│   ├── config.py           # Environment configuration
│   └── main.py             # Application entry point
├── docker-compose.yml
├── schema.sql
├── .env.example
└── pyproject.toml
```

## Current Progress (Phase 1 — API Development)
- [x] Project setup, Dockerized PostgreSQL 16, and database schema
- [x] Layered architecture & health check (`GET /health`)
- [x] JWT authentication helper (`HTTPBearer`)
- [x] **Section 1: Auth & Users**
  - `POST /v1/auth/login`
  - `GET /v1/users/me`
  - `PATCH /v1/users/me`
- [ ] **Section 2:** User Addresses
- [ ] **Section 3:** Wallets & Transactions
- [ ] **Section 4:** Booths
- [ ] **Section 5:** Products & Reviews
- [ ] **Section 6:** Carts & Cart Items
- [ ] **Section 7:** Coupons & Orders

## Getting Started

1. **Clone the repository and install dependencies:**
   ```bash
   uv sync
   ```

2. **Configure environment variables:**
   Copy `.env.example` to `.env` and fill in your PostgreSQL credentials.

3. **Start PostgreSQL with Docker:**
   ```bash
   docker compose up -d
   ```

4. **Run the API server:**
   ```bash
   uv run uvicorn src.main:app --reload
   ```

5. **Open API Documentation (Swagger UI):**
   - Health check: `http://127.0.0.1:8000/health`
   - Interactive docs: `http://127.0.0.1:8000/docs`

## Documentation
- [API Design Specification (v1)](docs/api-design.md)
- [Database ERD Diagram](docs/erd-diagram.pdf)
- [Wireframes](docs/wireframes/)