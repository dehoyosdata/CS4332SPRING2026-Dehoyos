# scripts/ — Startup and Seeding

This folder contains the container entrypoint and the library data seed script.

---

## Structure

| File | Purpose |
|------|---------|
| **`entrypoint.sh`** | Docker entrypoint. Runs the seed script when `SEED_LIBRARY_DATA=true`, then starts uvicorn. |
| **`seed_library_data.py`** | Seeds the database with users, students, books, and loans when enabled. |

---

## entrypoint.sh

**What it does:**

1. If `SEED_LIBRARY_DATA=true`, runs `python scripts/seed_library_data.py`.
2. Starts the API with `uvicorn app.main:app --host 0.0.0.0 --port 8000`.

**When it runs:** The Dockerfile sets this as the container's `ENTRYPOINT`. The seed runs before the API starts, so data is available on first request.

**Environment:** Reads `SEED_LIBRARY_DATA` from the container environment (passed from `.env` via docker-compose).

---

## seed_library_data.py

**When it runs:**

- **Automatically:** When `SEED_LIBRARY_DATA=true` and `entrypoint.sh` runs before uvicorn.
- **Manually:** `docker compose exec dal python scripts/seed_library_data.py` (after containers are up).

**What it seeds:**

| Table | Count | Notes |
|-------|-------|-------|
| `users` | 10 | alice@university.edu … jack@university.edu, password: `password123` |
| `students` | 1,000 | Random names, unique emails |
| `books` | 2,000 | Titles like "Introduction to Python", unique ISBNs |
| `loans` | ~30,000 | Mix of on-time, late, and unreturned |

**Logic:**

1. **Skips if already seeded** — Checks if `students` has rows; if so, exits.
2. **Waits for DB** — Retries connection up to 36 times with 5s delay.
3. **Creates tables** — `Base.metadata.create_all(bind=engine)` if needed.
4. **Seeds in order** — Users → Students → Books → Loans.
5. **Loan distribution** — ~12% not returned, ~73% on-time, ~15% late (configurable via constants).
6. **Book copies** — Adjusts `copies_available` after seeding to reflect active loans.

**Dependencies:** Uses `app.core.db` (engine, SessionLocal), `app.models`, and `app.utils.hashing`. Requires `faker` for random data.
