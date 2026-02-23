# app/services — Business Logic Layer

This package contains the business logic. Services orchestrate repository calls, enforce rules (e.g. no duplicate emails, max books per student), and do domain-specific work (e.g. password hashing). They do **not** handle HTTP or SQL directly.

---

## Structure

| File | Purpose |
|------|---------|
| **`users_service.py`** | Create user (hash password, check duplicate email). Get user by email. |
| **`students_service.py`** | Create student (check duplicate). Get student by ID. |
| **`books_service.py`** | Create book (check duplicate ISBN). Get book by ID. |
| **`loans_service.py`** | Borrow book (validate student, book, limit, copies). Return book. Get active/overdue loans, student loan history. |
| **`reports_service.py`** | Bad history (students with most late returns). Good history (most on-time returns). |

---

## Responsibilities

- **Validation** — Does the student exist? Does the book have copies? Is the student under their max?
- **Orchestration** — Calls multiple repositories in the right order (e.g. create loan → decrement copies).
- **Business rules** — Hash passwords, check uniqueness before insert, compute due dates.

---

## What Services Do NOT Do

- Parse HTTP requests or return HTTP responses.
- Run raw SQL or talk to the database directly (that’s the repository layer).
- Know about Pydantic schemas (handled by the API layer).

---

## Dependencies

- **`app.repositories`** — All services call repository functions.
- **`app.utils.hashing`** — `users_service` uses `hash_password()`.

---

## Example: `borrow_book_service`

1. Fetch student and book from repositories.
2. If either is missing → `ValueError`.
3. Check active loan count vs `max_books_allowed`.
4. Check `copies_available > 0`.
5. Create loan via `loans_repo.create_loan()`.
6. Decrement copies via `books_repo.decrement_copies()`.
7. Return the loan.
