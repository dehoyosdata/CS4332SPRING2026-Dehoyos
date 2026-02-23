"""User service: business logic for user creation and lookup."""

from sqlalchemy.orm import Session

from app.repositories import users_repo
from app.utils.hashing import hash_password


def create_user_service(db: Session, email: str, password: str):
    """Create user: check duplicates, hash password, call repo.
    Raises ValueError if email already exists.
    """
    existing = users_repo.get_user_by_email(db, email)
    if existing:
        raise ValueError("User with this email already exists")
    pwd_hash = hash_password(password)
    return users_repo.create_user(db, email, pwd_hash)


def get_user_by_email_service(db: Session, email: str):
    """Get user by email. Returns None if not found."""
    return users_repo.get_user_by_email(db, email)
