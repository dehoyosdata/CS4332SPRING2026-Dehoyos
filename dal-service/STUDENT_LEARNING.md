# Learning Guide for Students

This document explains the three core technologies used in this DAL service. Understanding them will help you read the code, make changes, and complete coursework.

---

## Overview

This project is built with:

| Technology | Role | Where to see it |
|------------|------|-----------------|
| **FastAPI** | Web framework: routes, HTTP handling, dependency injection | `app/main.py`, `app/api/` |
| **Pydantic** | Data validation and serialization (request/response shapes) | `app/schemas/` |
| **SQLAlchemy** | Database ORM and connection management | `app/core/db.py`, `app/models/`, `app/repositories/` |

---

## 1. FastAPI

**What it is:** A modern Python web framework for building APIs. It handles HTTP, routing, and integrates tightly with Pydantic and dependency injection.

### Key Concepts to Learn

- **Routers and endpoints** — How `@router.post("")` or `@router.get("/{id}")` map HTTP methods and paths to Python functions.
- **Dependency injection** — How `Depends(get_db)` and `Depends(require_service_key)` inject the database session and auth into your route handlers.
- **Request/response models** — How `response_model=UserOut` shapes the JSON response, and how `body: UserCreate` validates the request body.
- **HTTP status codes** — How `HTTPException(status_code=404, detail="...")` returns non-200 responses.

### In This Project

```
app/main.py          → Creates FastAPI app, registers routers
app/api/deps.py      → Defines get_db, require_service_key (dependencies)
app/api/users.py     → Router with POST /users, GET /users/by-email
```

Example flow when you call `POST /users`:

1. FastAPI receives the request.
2. `require_service_key` checks the `x-api-key` header.
3. `get_db` provides a database session.
4. The request body is validated against `UserCreate` (Pydantic).
5. Your handler runs and returns a `UserOut` (serialized to JSON).

### Suggested Resources

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/) — Sections on path operations, request body, dependencies.
- Focus on: **Path Operations**, **Request Body**, **Dependencies**.

---

## 2. Pydantic

**What it is:** A library for data validation using Python type hints. FastAPI uses Pydantic models for request bodies, query params, and response schemas.

### Key Concepts to Learn

- **BaseModel** — Base class for your schemas. Define fields with types; Pydantic validates and serializes automatically.
- **Field types** — `str`, `int`, `EmailStr`, `datetime`, etc. Invalid data raises a validation error (422).
- **`model_config`** — e.g. `from_attributes=True` lets you construct a Pydantic model from an ORM object (e.g. `UserOut.model_validate(user)`).
- **Request vs response schemas** — `UserCreate` for incoming data (may omit `id`), `UserOut` for responses (includes `id`, excludes `password_hash`).

### In This Project

```
app/schemas/users.py   → UserCreate (email, password), UserOut (id, email)
app/schemas/library.py → StudentCreate/Out, BookCreate/Out, LoanCreate/Out
```

**Request schema** — validates what the client sends:

```python
class UserCreate(BaseModel):
    email: EmailStr   # Must be valid email format
    password: str
```

**Response schema** — shapes what the API returns (no password):

```python
class UserOut(BaseModel):
    id: int
    email: EmailStr

    model_config = {"from_attributes": True}  # Can build from SQLAlchemy User
```

### Suggested Resources

- [Pydantic docs](https://docs.pydantic.dev/latest/) — Getting started, models.
- [FastAPI + Pydantic](https://fastapi.tiangolo.com/tutorial/body/) — How they work together.

---

## 3. SQLAlchemy

**What it is:** The most common Python ORM. It maps Python classes to database tables and lets you run queries in Python instead of raw SQL.

### Key Concepts to Learn

- **Declarative base** — A base class (`Base`) that all models inherit from.
- **Models and tables** — `__tablename__` and column definitions (`mapped_column`, `Mapped`).
- **Engine and Session** — `create_engine()` connects to the DB; `Session` is used for queries and commits.
- **CRUD operations** — `db.add(obj)`, `db.commit()`, `db.query(Model).filter(...).first()`.

### In This Project

```
app/models/base.py    → DeclarativeBase
app/models/user.py    → User model (id, email, password_hash)
app/models/library.py → Student, Book, Loan models
app/core/db.py        → engine, SessionLocal, get_db, init_schema
app/repositories/     → Uses Session to query and persist
```

**Model example** (`app/models/user.py`):

```python
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
```

**Repository example** (`app/repositories/users_repo.py`):

```python
def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password_hash: str) -> User:
    user = User(email=email, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
```

### Suggested Resources

- [SQLAlchemy 2.0 tutorial](https://docs.sqlalchemy.org/en/20/tutorial/) — Core concepts, engine, sessions.
- Focus on: **ORM mapped classes**, **Creating and persisting objects**, **Select/query**.

---

## How They Work Together

```
HTTP Request                    →  FastAPI (route)
                                    ↓
Request JSON                    →  Pydantic (UserCreate) validates
                                    ↓
Route handler                   →  Calls service → repository
                                    ↓
SQLAlchemy                      →  Queries DB, returns User model
                                    ↓
User (ORM)                      →  Pydantic (UserOut.model_validate)
                                    ↓
JSON Response                   →  FastAPI returns to client
```

### Trace Through the Code

For `POST /users` with body `{"email":"alice@example.com","password":"secret"}`:

1. **`app/api/users.py`** — Route receives request, `body` is validated as `UserCreate`.
2. **`app/services/users_service.py`** — Business logic (hash password, check duplicates).
3. **`app/repositories/users_repo.py`** — `create_user(db, ...)` persists to DB via SQLAlchemy.
4. **`app/api/users.py`** — `UserOut.model_validate(user)` converts ORM object to response schema, FastAPI returns JSON.

---

## Quick Checklist

Before modifying this project, make sure you understand:

- [ ] How FastAPI routes and `Depends()` work
- [ ] How Pydantic models validate request bodies and shape responses
- [ ] How SQLAlchemy models map to tables and how repositories use `Session` for queries
- [ ] The flow: Route → Service → Repository → DB, and back with Pydantic response models

---

## Suggested Reading Order

1. **FastAPI** — Tutorial sections 1–7 (path ops, body, dependencies).
2. **Pydantic** — Models and validation basics.
3. **SQLAlchemy** — ORM tutorial, engine, Session, basic CRUD.

Once comfortable with these, you can extend this service (new endpoints, models, or reports) with confidence.
