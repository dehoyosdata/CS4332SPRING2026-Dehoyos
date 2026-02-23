"""Pydantic schemas. Re-exports for backwards compatibility."""

from app.schemas.library import (
    BookCreate,
    BookOut,
    LoanCreate,
    LoanOut,
    StudentCreate,
    StudentOut,
)
from app.schemas.users import UserCreate, UserOut

__all__ = [
    "UserCreate",
    "UserOut",
    "StudentCreate",
    "StudentOut",
    "BookCreate",
    "BookOut",
    "LoanCreate",
    "LoanOut",
]
