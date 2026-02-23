"""Book repository: direct DB operations."""

from sqlalchemy.orm import Session

from app.models import Book


def get_book_by_id(db: Session, book_id: int) -> Book | None:
    """Return book by ID, or None if not found."""
    return db.query(Book).filter(Book.id == book_id).first()


def get_book_by_isbn(db: Session, isbn: str) -> Book | None:
    """Return book by ISBN, or None if not found."""
    return db.query(Book).filter(Book.isbn == isbn).first()


def create_book(
    db: Session, title: str, isbn: str, copies_available: int = 1
) -> Book:
    """Create and persist a book."""
    book = Book(title=title, isbn=isbn, copies_available=copies_available)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def increment_copies(db: Session, book_id: int, amount: int = 1) -> Book | None:
    """Increment copies_available. Returns updated book or None."""
    book = get_book_by_id(db, book_id)
    if not book:
        return None
    book.copies_available += amount
    db.commit()
    db.refresh(book)
    return book


def decrement_copies(db: Session, book_id: int, amount: int = 1) -> Book | None:
    """Decrement copies_available. Returns updated book or None."""
    book = get_book_by_id(db, book_id)
    if not book:
        return None
    book.copies_available -= amount
    db.commit()
    db.refresh(book)
    return book
