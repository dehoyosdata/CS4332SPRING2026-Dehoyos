# CS4332 DAL Service

**Data Access Layer as a Service (DAL-as-a-Service)** — a standalone HTTP API that provides database access. Any backend (Node.js, Java, Go, Python, etc.) can call it over the network instead of connecting directly to the database.

---

## Table of Contents

1. [What is DAL-as-a-Service?](#what-is-dal-as-a-service)
2. [Architecture Diagram](#architecture-diagram)
3. [Component Overview](#component-overview)
4. [Python Files Explained](#python-files-explained)
5. [Docker Setup](#docker-setup)
6. [Getting Started](#getting-started)
7. [API Reference](#api-reference)
8. [Troubleshooting](#troubleshooting)
9. [Connecting with DBeaver](#connecting-with-dbeaver)
10. [Docker Cheatsheet](#docker-cheatsheet)

**Students:** See [`STUDENT_LEARNING.md`](STUDENT_LEARNING.md) for a guide on FastAPI, Pydantic, and SQLAlchemy — what to learn and how they’re used in this project. Ready to test yourself? See [`CHALLENGE.md`](CHALLENGE.md). Each package has its own README: `app/api/README.md`, `app/core/README.md`, `app/models/README.md`, `app/schemas/README.md`, `app/services/README.md`, `app/repositories/README.md`, `app/utils/README.md`, `scripts/README.md`.

---

## What is DAL-as-a-Service?

- **Centralized data access**: Only the DAL service connects to the database. Student backends call HTTP endpoints instead of the DB.
- **Framework-agnostic**: Works with any language (Node, Java, Go, Python, etc.) that can make HTTP requests.
- **Multi-database support**: Configure via environment variables for PostgreSQL or MySQL.
- **Library domain**: Includes a simple library scenario (students, books, loans, reports). See `app/schemas/README.md` for design details and domain overview.
- **Example clients**: Apps that consume the DAL API live in `example/`. Includes LibraryDashboard (Flask). See `example/README.md` for app ideas and design guidance.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           EXTERNAL CLIENTS                                    │
│              (Node.js, Java, Go, Python backends, curl, Postman)              │
└──────────────────────────────────────────┬──────────────────────────────────┘
                                           │ HTTP + x-api-key header
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER (main.py + app/api/)                    │
│  • FastAPI routes: health, users, students, books, loans, reports            │
│  • Request validation (Pydantic schemas)                                     │
│  • Dependency injection (API key, DB session)                                │
│  • HTTP status codes (200, 401, 404, 409, 422, 503)                          │
└──────────────────────────────────────────┬──────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SERVICE LAYER (app/services/)                              │
│  • Business logic: duplicate check, password hashing                          │
│  • Orchestrates repository calls                                             │
│  • No knowledge of HTTP or SQL                                                │
└──────────────────────────────────────────┬──────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                   REPOSITORY LAYER (app/repositories/)                         │
│  • Data access only: CRUD operations                                        │
│  • SQLAlchemy queries                                                        │
│  • Abstracts database details                                                │
└──────────────────────────────────────────┬──────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DATABASE (PostgreSQL or MySQL)                       │
│  • Tables: users, students, books, loans                                     │
└─────────────────────────────────────────────────────────────────────────────┘


SUPPORTING COMPONENTS:

  app/core/         app/models/         app/schemas/         app/api/
  config.py         base.py, user.py     users.py             deps.py
  db.py             library.py          library.py           health, users,
  security.py       (User, Student,      (UserCreate/Out,     students, books,
                    Book, Loan)          Student/Book/Loan)   loans, reports

  app/utils/hashing.py   →  hash_password() (SHA256 placeholder)
```

---

## Component Overview

| Layer | Responsibility |
|-------|----------------|
| **Presentation** | HTTP handling, validation, error responses |
| **Service** | Business rules (e.g., no duplicate emails, hash passwords) |
| **Repository** | Database queries, persistence |
| **Database** | Actual storage (Postgres or MySQL) |

---

## Python Files Explained

### Project Structure

```
dal-service/
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI app, router registration, startup
│   ├── core/                 # Config, DB, auth
│   │   ├── config.py         # Environment config (DB_*, API_KEY, INIT_SCHEMA)
│   │   ├── db.py             # SQLAlchemy engine, session, schema init
│   │   └── security.py       # API key (require_service_key)
│   ├── models/               # SQLAlchemy ORM models
│   │   ├── base.py           # Declarative base
│   │   ├── user.py           # User model
│   │   └── library.py        # Student, Book, Loan models
│   ├── schemas/              # Pydantic request/response schemas
│   │   ├── users.py          # UserCreate, UserOut
│   │   ├── library.py        # StudentCreate/Out, BookCreate/Out, LoanCreate/Out
│   │   └── README.md          # Schemas + library domain design
│   ├── api/                  # Route modules (presentation layer)
│   │   ├── deps.py           # Re-exports get_db, require_service_key
│   │   ├── health.py         # /health
│   │   ├── users.py          # /users
│   │   ├── students.py       # /students
│   │   ├── books.py          # /books
│   │   ├── loans.py          # /loans
│   │   └── reports.py        # /reports
│   ├── services/
│   │   ├── __init__.py
│   │   ├── users_service.py
│   │   ├── students_service.py
│   │   ├── books_service.py
│   │   ├── loans_service.py
│   │   └── reports_service.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── users_repo.py
│   │   ├── students_repo.py
│   │   ├── books_repo.py
│   │   └── loans_repo.py
│   └── utils/
│       ├── __init__.py
│       └── hashing.py        # Password hashing (placeholder)
├── scripts/
│   ├── entrypoint.sh
│   └── seed_library_data.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

### File-by-File Breakdown

| File | Purpose | Used By |
|------|---------|---------|
| **`app/main.py`** | FastAPI app, registers routers from `app.api`, startup event (schema init). | Entry point (uvicorn) |
| **`app/core/config.py`** | Loads `.env`, validates `DB_VENDOR`, `DB_HOST`, `API_KEY`, `INIT_SCHEMA`, etc. | `core/db.py`, `core/security.py` |
| **`app/core/db.py`** | SQLAlchemy engine, `get_db()` session dependency, `init_schema_with_retry()`. | `main.py`, `api/deps.py`, repositories |
| **`app/core/security.py`** | `require_service_key` dependency. Checks `x-api-key` header. | `api/deps.py` (re-exported to all routes) |
| **`app/models/`** | SQLAlchemy models: `Base`, `User`, `Student`, `Book`, `Loan`. | `core/db.py`, all repositories |
| **`app/schemas/`** | Pydantic schemas: `UserCreate/Out`, `StudentCreate/Out`, `BookCreate/Out`, `LoanCreate/Out`. | All `app/api/` route modules |
| **`app/api/deps.py`** | Re-exports `get_db`, `require_service_key` from core. | All route modules |
| **`app/api/health.py`** | `/health` endpoint. | `main.py` |
| **`app/api/users.py`** | `/users` POST, GET by-email. | `main.py` |
| **`app/api/students.py`** | `/students` POST, GET by ID, GET loans. | `main.py` |
| **`app/api/books.py`** | `/books` POST, GET by ID. | `main.py` |
| **`app/api/loans.py`** | `/loans` POST, PATCH return, GET active, GET overdue. | `main.py` |
| **`app/api/reports.py`** | `/reports/bad-history`, `/reports/good-history`. | `main.py` |
| **`app/services/*.py`** | Business logic: users, students, books, loans, reports. | API route modules |
| **`app/repositories/*.py`** | CRUD and data access. | Services |
| **`app/utils/hashing.py`** | `hash_password()` — SHA256 placeholder. | `users_service.py`, seed script |
| **`app/utils/README.md`** | Utils overview and hashing notes. | Documentation |
| **`app/schemas/README.md`** | Schemas overview, conventions, and library domain design. | Documentation |
| **`scripts/seed_library_data.py`** | Seeds users, students, books, loans when `SEED_LIBRARY_DATA=true`. Uses `app.core.db`, `app.models`. | Entrypoint / manual run |

### Dependency Flow

```
main.py
  ├── app.core.config (INIT_SCHEMA)
  ├── app.core.db (init_schema_with_retry)
  └── app.api (routers: health, users, students, books, loans, reports)
        ├── api/deps.py → get_db (core.db), require_service_key (core.security)
        ├── api/*.py → schemas (app.schemas), services
        └── services
              ├── repositories → models (app.models)
              └── utils/hashing.py
```

---

## Docker Setup

### What Each Docker File Does

| File | Purpose |
|------|---------|
| **`Dockerfile`** | Defines how to **build** the DAL service image. Base: Python 3.12. Installs dependencies, copies `app/`, runs uvicorn. |
| **`docker-compose.yml`** | Defines **which containers run**. Has 3 services: `dal` (your app), `db_postgres`, `db_mysql`. Uses **profiles** so you run only the DB you need. |

### docker-compose.yml Structure

```
services:
  dal          → Builds from Dockerfile, exposes port 8000, uses .env
  db_postgres  → Postgres 16 image, profile "postgres"
  db_mysql     → MySQL 8 image, profile "mysql"

volumes:
  postgres_data, mysql_data  → Persist DB data between restarts
```

### Important: .env File

**You must create a `.env` file** — Docker Compose and the app read configuration from it.

1. **Copy the example:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env`** for the database you use:
   - **PostgreSQL**: Keep default values (DB_HOST=db_postgres, etc.)
   - **MySQL**: Uncomment and set DB_VENDOR=mysql, DB_HOST=db_mysql, etc.

---

## Getting Started

### Step 1: Create .env

```bash
cd dal-service
cp .env.example .env
# Edit .env if using MySQL (see .env.example for MySQL block)
```

### Step 2: Start with PostgreSQL

```bash
docker compose --profile postgres up --build
```

- Builds the DAL service image
- Starts PostgreSQL
- DAL retries until DB is ready, then creates tables
- API available at **http://localhost:8000**

### Step 3: Start with MySQL

1. In `.env`, set:
   ```
   DB_VENDOR=mysql
   DB_HOST=db_mysql
   DB_PORT=3306
   DB_NAME=cs4332
   DB_USER=cs4332
   DB_PASSWORD=cs4332pass
   MYSQL_ROOT_PASSWORD=rootpass
   ```

2. Run:
   ```bash
   docker compose --profile mysql up --build
   ```

### Step 4: Verify

```bash
curl -H "x-api-key: dev-api-key-change-in-production" http://localhost:8000/health
# Expected: {"status":"ok","database":"connected"}
```

Open **http://localhost:8000/docs** for interactive API documentation.

### Step 5: Seed Library Data (Optional)

Set `SEED_LIBRARY_DATA=true` in `.env` to automatically seed on first run:
- 10 users (alice@university.edu … jack@university.edu, password: `password123`), 1000 students, 2000 books, ~30,000 loans
- Runs before the API starts; skips if data already exists
- Time period: Jan 2026 until seed run date
- Mix of on-time returns, late returns, and unreturned books

Or run manually after containers are up:
```bash
docker compose --profile postgres exec dal python scripts/seed_library_data.py
```

---

## API Reference

All endpoints require the **`x-api-key`** header. Missing or invalid key returns **401**.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check + DB connectivity |
| POST | `/users` | Create user (body: `{email, password}`) |
| GET | `/users/by-email?email=...` | Get user by email |
| POST | `/students` | Create student |
| GET | `/students/{id}` | Get student |
| GET | `/students/{id}/loans` | Student loan history |
| POST | `/books` | Create book |
| GET | `/books/{id}` | Get book |
| POST | `/loans` | Borrow book (body: `{student_id, book_id}`) |
| PATCH | `/loans/{id}/return` | Record return |
| GET | `/loans/active` | Loans not yet returned |
| GET | `/loans/overdue` | Active loans past due |
| GET | `/reports/bad-history` | Top students with late returns |
| GET | `/reports/good-history` | Top students with on-time returns |

### Example Requests

```bash
# Health
curl -H "x-api-key: dev-api-key-change-in-production" http://localhost:8000/health

# Create user
curl -X POST http://localhost:8000/users \
  -H "x-api-key: dev-api-key-change-in-production" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"secret123"}'

# Get by email
curl -H "x-api-key: dev-api-key-change-in-production" \
  "http://localhost:8000/users/by-email?email=alice@example.com"

# Library: create student, book, borrow, return
curl -X POST http://localhost:8000/students -H "x-api-key: dev-api-key-change-in-production" \
  -H "Content-Type: application/json" -d '{"name":"Alice","email":"alice@edu.com","max_books_allowed":3}'
curl -X POST http://localhost:8000/books -H "x-api-key: dev-api-key-change-in-production" \
  -H "Content-Type: application/json" -d '{"title":"Python 101","isbn":"978-0-123456-78-9","copies_available":2}'
curl -X POST http://localhost:8000/loans -H "x-api-key: dev-api-key-change-in-production" \
  -H "Content-Type: application/json" -d '{"student_id":1,"book_id":1}'
curl -X PATCH http://localhost:8000/loans/1/return -H "x-api-key: dev-api-key-change-in-production"
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **"could not translate host name db_postgres"** | Ensure `.env` has `DB_HOST=db_postgres` (for Postgres) or `DB_HOST=db_mysql` (for MySQL). Never use `localhost` when running in Docker. |
| **"password authentication failed"** | Stale DB volume with old credentials. Run `docker compose --profile postgres down -v` then `up --build` to reinitialize. |
| **"Database not ready"** | DB container may still be starting. Wait 10–30 seconds or check `docker compose logs db_postgres` (or `db_mysql`). |
| **401 on all requests** | Include `x-api-key` header. Value must match `API_KEY` in `.env`. |

---

## Security Note

- **API key**: Protect the `x-api-key` value. Rotate it in production.
- **Password hashing**: This project uses SHA256 as a **classroom placeholder only**. Real systems must use bcrypt, argon2, or scrypt.

---

## Connecting with DBeaver

Use these settings when the database is running via Docker (port mappings are exposed to your host).

### PostgreSQL

| Setting | Value |
|---------|-------|
| **Host** | `localhost` |
| **Port** | `5432` |
| **Database** | `cs4332` |
| **Username** | `cs4332` |
| **Password** | `cs4332pass` |

**Steps:** New Connection → PostgreSQL → Enter the values above → Test Connection.

### MySQL

| Setting | Value |
|---------|-------|
| **Host** | `localhost` |
| **Port** | `3306` |
| **Database** | `cs4332` |
| **Username** | `cs4332` |
| **Password** | `cs4332pass` |

**Steps:** New Connection → MySQL → Enter the values above → Test Connection.

**Note:** Use `localhost` because Docker publishes ports to your host. The `DB_HOST` values (`db_postgres`, `db_mysql`) are for containers talking to each other.

---

## Docker Cheatsheet

### Run in background

```bash
docker compose --profile postgres up -d --build
# or
docker compose --profile mysql up -d --build
```

`-d` runs containers in detached (background) mode. `--build` rebuilds the image if needed.

### Common commands

| Task | Command |
|------|---------|
| **View logs** | `docker compose logs dal` — DAL service logs |
| | `docker compose logs db_postgres` — Postgres logs |
| | `docker compose logs db_mysql` — MySQL logs |
| | `docker compose logs -f dal` — Follow logs (live) |
| **Stop containers** | `docker compose --profile postgres down` (or `--profile mysql`) |
| **Stop + remove volumes (delete DB data)** | `docker compose --profile postgres down -v` or `docker compose --profile mysql down -v` |
| **List running containers** | `docker compose ps` |

**Shutdown and delete volumes:** Use `down -v` to remove containers *and* named volumes. This wipes all database data. Useful when you want a fresh start or to fix "password authentication failed" from stale credentials.

### Shell access

| Goal | Command |
|------|---------|
| **Bash in DAL container** | `docker compose exec dal bash` |
| **PostgreSQL CLI** | `docker compose exec db_postgres psql -U cs4332 -d cs4332` |
| **MySQL CLI** | `docker compose exec db_mysql mysql -u cs4332 -pcs4332pass cs4332` |

With Postgres, `\dt` lists tables; `\q` quits. With MySQL, `SHOW TABLES;` lists tables; `exit` quits.

### Change database data mount location

Edit `docker-compose.yml` and change the volume from a named volume to a host path:

**Before (named volume — Docker manages location):**
```yaml
volumes:
  postgres_data:
  mysql_data:
# ...
    volumes:
      - postgres_data:/var/lib/postgresql/data
    # or
      - mysql_data:/var/lib/mysql
```

**After (host path — you choose where data lives):**
```yaml
# Remove from top-level volumes: section if using host path
    volumes:
      - ./data/postgres:/var/lib/postgresql/data   # PostgreSQL
    # or
      - ./data/mysql:/var/lib/mysql                # MySQL
```

Then create the directory and restart:
```bash
mkdir -p data/postgres   # or data/mysql
docker compose --profile postgres down
docker compose --profile postgres up -d
```

**Note:** Host paths are useful for backups or when you want the DB files in a specific folder. Named volumes are simpler and managed by Docker.

---

## License

For CS4332 course use.
