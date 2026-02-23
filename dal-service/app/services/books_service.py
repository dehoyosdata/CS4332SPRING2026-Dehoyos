"""Book service: business logic for books."""

from sqlalchemy.orm import Session

from app.repositories import books_repo


def create_book_service(
    db: Session, title: str, isbn: str, copies_available: int = 1
):
    """Create book. Raises ValueError if ISBN already exists."""
    existing = books_repo.get_book_by_isbn(db, isbn)
    if existing:
        raise ValueError("Book with this ISBN already exists")
    return books_repo.create_book(db, title, isbn, copies_available)


def get_book_by_id_service(db: Session, book_id: int):
    """Get book by ID. Returns None if not found."""
    return books_repo.get_book_by_id(db, book_id)
