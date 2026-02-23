"""Library domain schemas."""

from datetime import datetime

from pydantic import BaseModel, EmailStr


class StudentCreate(BaseModel):
    """Request schema for creating a student."""

    name: str
    email: EmailStr
    max_books_allowed: int = 3


class StudentOut(BaseModel):
    """Response schema for student."""

    id: int
    name: str
    email: EmailStr
    max_books_allowed: int

    model_config = {"from_attributes": True}


class BookCreate(BaseModel):
    """Request schema for creating a book."""

    title: str
    isbn: str
    copies_available: int = 1


class BookOut(BaseModel):
    """Response schema for book."""

    id: int
    title: str
    isbn: str
    copies_available: int

    model_config = {"from_attributes": True}


class LoanCreate(BaseModel):
    """Request schema for creating a loan (borrow book)."""

    student_id: int
    book_id: int


class LoanOut(BaseModel):
    """Response schema for loan."""

    id: int
    student_id: int
    book_id: int
    borrowed_at: datetime
    due_date: datetime
    returned_at: datetime | None

    model_config = {"from_attributes": True}
