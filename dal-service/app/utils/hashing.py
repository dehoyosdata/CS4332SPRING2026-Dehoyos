"""Password hashing utilities.

PLACEHOLDER ONLY: Uses SHA256 for classroom demos. Real production systems must use
bcrypt, argon2, or scrypt. SHA256 is not suitable for password storage.
"""

import hashlib


def hash_password(password: str) -> str:
    """Hash password with SHA256. Placeholder only; use bcrypt/argon2 in production."""
    return hashlib.sha256(password.encode()).hexdigest()
