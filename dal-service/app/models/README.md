# app/models — SQLAlchemy ORM Models

This package defines the database schema as Python classes. Each model maps to a table; attributes map to columns. Repositories use these models for queries and persistence.

---

## Structure

| File | Purpose |
|------|---------|
| **`base.py`** | `DeclarativeBase` — base class all models inherit from. |
| **`user.py`** | `User` — id, email, password_hash. Maps to `users` table. |
| **`library.py`** | `Student`, `Book`, `Loan` — library domain. Maps to `students`, `books`, `loans`. |
| **`__init__.py`** | Re-exports `Base`, `User`, `Student`, `Book`, `Loan`. Use `from app.models import User`. |

---

## Models Overview

| Model | Table | Key Fields |
|-------|-------|------------|
| **User** | `users` | id, email (unique), password_hash |
| **Student** | `students` | id, name, email (unique), max_books_allowed (default 3) |
| **Book** | `books` | id, title, isbn (unique), copies_available |
| **Loan** | `loans` | id, student_id (FK), book_id (FK), borrowed_at, due_date, returned_at |

---

## Conventions

- **`__tablename__`** — Explicit table name (snake_case).
- **`Mapped[T]`** — Type hint for the column.
- **`mapped_column(...)`** — Column definition (Integer, String, DateTime, ForeignKey).
- **`returned_at` (Loan)** — `NULL` means the book is still borrowed.

---

## Usage

- **`app.core.db`** — Imports `Base` for `create_all()` and metadata.
- **`app.repositories/*`** — Import models for queries: `db.query(User).filter(...)`.
- **`scripts/seed_library_data.py`** — Imports for bulk `insert()`.

---

## Adding a New Model

1. Add a new file (e.g. `author.py`) or extend `library.py`.
2. Inherit from `Base`, set `__tablename__`, define columns.
3. Import and re-export in `__init__.py`.
4. Run with `INIT_SCHEMA=true` to create the table (or use migrations in production).
