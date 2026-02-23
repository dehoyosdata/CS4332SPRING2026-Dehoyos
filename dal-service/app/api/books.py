"""Book endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_service_key
from app.schemas import BookCreate, BookOut
from app.services import books_service

router = APIRouter(prefix="/books", tags=["books"])


@router.post("", response_model=BookOut, dependencies=[Depends(require_service_key)])
def create_book(
    body: BookCreate,
    db: Session = Depends(get_db),
) -> BookOut:
    """Create a book. Returns 409 if ISBN already exists."""
    try:
        book = books_service.create_book_service(
            db, body.title, body.isbn, body.copies_available
        )
        return BookOut.model_validate(book)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Book with this ISBN already exists")
    except ValueError as e:
        if "already exists" in str(e):
            raise HTTPException(status_code=409, detail="Book with this ISBN already exists")
        raise


@router.get(
    "/{book_id}",
    response_model=BookOut,
    dependencies=[Depends(require_service_key)],
)
def get_book(
    book_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
) -> BookOut:
    """Get book by ID. Returns 404 if not found."""
    book = books_service.get_book_by_id_service(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookOut.model_validate(book)
