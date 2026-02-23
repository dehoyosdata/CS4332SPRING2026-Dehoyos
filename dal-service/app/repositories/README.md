# app/repositories — Data Access Layer

This package performs direct database operations. Repositories know about SQLAlchemy models and sessions; they do **not** implement business rules or HTTP handling. Each repository usually corresponds to one or more models.

---

## Structure

| File | Purpose |
|------|---------|
| **`users_repo.py`** | `get_user_by_email()`, `create_user()` |
| **`students_repo.py`** | `get_student_by_id()`, `get_student_by_email()`, `create_student()` |
| **`books_repo.py`** | `get_book_by_id()`, `get_book_by_isbn()`, `create_book()`, `increment_copies()`, `decrement_copies()` |
| **`loans_repo.py`** | `create_loan()`, `get_loan_by_id()`, `mark_returned()`, `get_active_loans()`, `get_overdue_loans()`, `get_student_loans()`, `count_active_loans_for_student()`, `get_late_return_count_by_student()`, `get_on_time_return_count_by_student()` |

---

## Conventions

- **Session** — First parameter is always `db: Session`. Callers (services) obtain it from `get_db()`.
- **Commit** — Repositories typically call `db.commit()` for write operations. Some operations (e.g. bulk insert in seed script) commit explicitly.
- **Return types** — Query functions return `Model | None` or `list[Model]`. Create functions return the created model.

---

## Usage

- **`app.services`** — All services call repository functions. Services pass the `db` session they receive from the route handler.
- **`scripts/seed_library_data.py`** — Uses `insert()` for bulk inserts; does not use repositories (direct DB access for performance).

---

## Adding a New Repository

1. Create `new_entity_repo.py`.
2. Define functions that take `db: Session` and perform queries/inserts.
3. Import models from `app.models`.
4. Call the new repository from the appropriate service.
