# app/api — Presentation Layer

This package contains all HTTP route handlers. Each module defines an `APIRouter` that `main.py` registers with the FastAPI app.

---

## Structure


| File              | Purpose                                                                                                                                  |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `**deps.py**`     | Shared dependencies. Re-exports `get_db` and `require_service_key` from `app.core`. All routes use these for DB access and API-key auth. |
| `**health.py**`   | `GET /health` — Lightweight DB connectivity check.                                                                                       |
| `**users.py**`    | `POST /users`, `GET /users/by-email` — User creation and lookup.                                                                         |
| `**students.py**` | `POST /students`, `GET /students/{id}`, `GET /students/{id}/loans` — Student CRUD and loan history.                                      |
| `**books.py**`    | `POST /books`, `GET /books/{id}` — Book creation and lookup.                                                                             |
| `**loans.py**`    | `POST /loans`, `PATCH /loans/{id}/return`, `GET /loans/active`, `GET /loans/overdue` — Borrow, return, and query loans.                  |
| `**reports.py**`  | `GET /reports/bad-history`, `GET /reports/good-history` — Student rankings by late/on-time returns.                                      |


---

## How It Works

1. **Routers** — Each module defines an `APIRouter` with a `prefix` (e.g. `/users`) and `tags` for OpenAPI docs.
2. **Dependencies** — `Depends(require_service_key)` ensures the `x-api-key` header is valid. `Depends(get_db)` injects a database session.
3. **Request validation** — Pydantic schemas (e.g. `UserCreate`) validate the request body. Invalid data returns 422.
4. **Response shaping** — `response_model=UserOut` tells FastAPI how to serialize the return value to JSON.
5. **Service calls** — Route handlers call the service layer; they do not talk to the database directly.

---

## Example: Adding a New Endpoint

1. Add the route in the appropriate module (e.g. `students.py`).
2. Use `Depends(get_db)` and `Depends(require_service_key)`.
3. Define a Pydantic schema for the request/response if needed.
4. Call the relevant service and return a schema instance.
5. `main.py` already includes the router — no changes needed there.

---

## Dependencies

- `**app.core`** — config, db, security (via `deps.py`)
- `**app.schemas**` — request/response models
- `**app.services**` — business logic

