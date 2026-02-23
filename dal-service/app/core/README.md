# app/core — Configuration, Database, Security

This package holds shared infrastructure: environment config, database connection, and API-key authentication. Other packages import from here — it has no knowledge of routes, schemas, or business logic.

---

## Structure


| File              | Purpose                                                                                                           |
| ----------------- | ----------------------------------------------------------------------------------------------------------------- |
| `**config.py**`   | Loads `.env` via `dotenv`, validates required vars, exports constants. Fails fast at import if config is invalid. |
| `**db.py**`       | SQLAlchemy engine, `SessionLocal`, `get_db()` dependency, `init_schema_with_retry()`.                             |
| `**security.py**` | `require_service_key` — FastAPI dependency that validates the `x-api-key` header.                                 |


---

## config.py

**Environment variables read:**


| Variable      | Purpose                              | Example                               |
| ------------- | ------------------------------------ | ------------------------------------- |
| `DB_VENDOR`   | Database type                        | `postgres` or `mysql`                 |
| `DB_HOST`     | Hostname                             | `db_postgres` (Docker) or `localhost` |
| `DB_PORT`     | Port                                 | `5432` (Postgres) or `3306` (MySQL)   |
| `DB_NAME`     | Database name                        | `cs4332`                              |
| `DB_USER`     | Username                             | `cs4332`                              |
| `DB_PASSWORD` | Password                             | (from `.env`)                         |
| `API_KEY`     | Value expected in `x-api-key` header | `dev-api-key-change-in-production`    |
| `INIT_SCHEMA` | Create tables on startup (demo only) | `true` or `false`                     |


**Fail-fast:** If `DB_VENDOR` is invalid or any required DB var is missing, the app raises `ValueError` on import.

---

## db.py

- `**engine`** — SQLAlchemy engine built from `DATABASE_URL` (Postgres or MySQL).
- `**SessionLocal**` — Session factory. Used by `get_db()` and the seed script.
- `**get_db()**` — FastAPI dependency. Yields a session and closes it after the request.
- `**init_schema_with_retry()**` — Waits for the DB to be reachable, then runs `Base.metadata.create_all()`.
- `**init_schema()**` — Creates tables directly (used internally and by seed script).

---

## security.py

- `**require_service_key(x_api_key)**` — Async dependency. Reads `x-api-key` header. Raises `HTTPException(401)` if missing or invalid.
- Used by `app.api.deps` and applied to all routes via `dependencies=[Depends(require_service_key)]`.

---

## Usage

- `**app.api.deps**` imports `get_db` and `require_service_key` from here and re-exports them.
- `**app.main**` imports `INIT_SCHEMA` and `init_schema_with_retry` for the startup event.
- `**scripts/seed_library_data.py**` imports `SessionLocal`, `engine` for seeding.

