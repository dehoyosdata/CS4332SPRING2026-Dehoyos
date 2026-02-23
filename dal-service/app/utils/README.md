# app/utils — Shared Utilities

This package holds small helper modules used across the application.

---

## Structure

| File | Purpose |
|------|---------|
| **`hashing.py`** | `hash_password()` — hashes passwords before storing in the database. |

---

## hashing.py

- **`hash_password(password: str) -> str`** — Returns a hex-encoded SHA256 hash of the password.

**Security note:** This uses SHA256 as a **classroom placeholder only**. SHA256 is not suitable for production password storage (no salt, fast to compute, vulnerable to rainbow tables). Real systems must use bcrypt, argon2, or scrypt.

---

## Usage

- **`app.services.users_service`** — Hashes passwords before creating users.
- **`scripts/seed_library_data.py`** — Hashes passwords when seeding user records.
