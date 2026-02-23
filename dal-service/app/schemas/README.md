# app/schemas — Pydantic Schemas & Library Domain

This package defines the shape of HTTP requests and responses. FastAPI uses these for validation and JSON serialization. Each domain entity typically has a `*Create` schema (request) and `*Out` schema (response).

---

## Package Structure

| File | Purpose |
|------|---------|
| **`users.py`** | `UserCreate`, `UserOut` — user creation and response. |
| **`library.py`** | `StudentCreate/Out`, `BookCreate/Out`, `LoanCreate/Out` — library domain. |
| **`__init__.py`** | Re-exports all schemas. Use `from app.schemas import UserCreate, UserOut`. |

---

## Schema Types

| Schema | Used For | Notes |
|--------|----------|-------|
| **`*Create`** | Request body validation | Often omits `id`; may have defaults. |
| **`*Out`** | Response serialization | Excludes sensitive fields (e.g. no `password_hash`). Uses `from_attributes=True` to build from ORM objects. |

---

## Conventions

- **`EmailStr`** — Pydantic's email validator (from `pydantic`).
- **`model_config = {"from_attributes": True}`** — Allows `Schema.model_validate(orm_object)`.
- **`model_config = {"json_schema_extra": {...}}`** — Adds examples to OpenAPI docs.

---

## Flow

1. **Request** — Client sends JSON. FastAPI validates against `UserCreate` (or similar). Invalid → 422.
2. **Handler** — Uses `body.email`, `body.password`, etc.
3. **Response** — Handler gets ORM object (e.g. `User`), does `UserOut.model_validate(user)`, returns it. FastAPI serializes to JSON.

---

## Usage

- **`app.api/*`** — All route modules import schemas for `body:`, `response_model=`, and `Query`/`Path` types.
- **`app.services`** — Typically do **not** use schemas; they work with plain Python types and ORM objects.

---

# Library Domain

A minimal library management domain for CS4332: students borrow books, return them, and we track history for reporting.

## Core Entities

| Entity | Purpose |
|--------|---------|
| **Student** | Person who can borrow books (id, name, email, max_books_allowed) |
| **Book** | Library item (id, title, isbn, copies_available) |
| **Loan** | A student borrowing a book (id, student_id, book_id, borrowed_at, due_date, returned_at) |

## Business Rules

- **Max books per student**: Configurable via `max_books_allowed` (default 3).
- **Loan duration**: 14 days from borrow date.
- **Returned**: `returned_at IS NULL` means book not yet returned.
- **Overdue**: Active loan where `due_date < today`.

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/students` | Create student |
| GET | `/students/{id}` | Get student by ID |
| GET | `/students/{id}/loans` | Loan history for student |
| POST | `/books` | Create book |
| GET | `/books/{id}` | Get book by ID |
| POST | `/loans` | Create loan (borrow book) |
| PATCH | `/loans/{id}/return` | Record return |
| GET | `/loans/active` | Loans not yet returned |
| GET | `/loans/overdue` | Active loans past due date |
| GET | `/reports/bad-history` | Top 10 students with most late/overdue returns |
| GET | `/reports/good-history` | Top 10 students with most on-time returns |

## Data Flow Examples

### 1. Student borrows book
```
POST /loans { "student_id": 1, "book_id": 5 }
→ Check student has < max_books_allowed
→ Check book has copies_available > 0
→ Create loan (borrowed_at=now, due_date=now+14)
→ Decrement copies_available
```

### 2. Student returns book
```
PATCH /loans/3/return
→ Set returned_at = now
→ Increment copies_available
```

### 3. Who hasn't returned yet?
```
GET /loans/active
→ WHERE returned_at IS NULL
```

### 4. Top 10 bad history
```
GET /reports/bad-history
→ Students with most overdue or late returns (returned_at > due_date)
```

### 5. Top 10 good history
```
GET /reports/good-history
→ Students with most on-time returns (returned_at <= due_date)
```

## Simplified Schema

```
students:  id, name, email, max_books_allowed (default 3)
books:     id, title, isbn, copies_available
loans:     id, student_id, book_id, borrowed_at, due_date, returned_at
```

## Simplifications (Classroom Version)

- No reservations.
- No renewal logic.
- No fines.
- Loan duration fixed at 14 days.
- "Bad history" = count of late returns.
- "Good history" = count of on-time returns.
