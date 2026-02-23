"""Loan endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_service_key
from app.schemas import LoanCreate, LoanOut
from app.services import loans_service

router = APIRouter(prefix="/loans", tags=["loans"])


@router.post("", response_model=LoanOut, dependencies=[Depends(require_service_key)])
def create_loan(
    body: LoanCreate,
    db: Session = Depends(get_db),
) -> LoanOut:
    """Borrow a book. Returns 400 on validation error (student limit, no copies)."""
    try:
        loan = loans_service.borrow_book_service(db, body.student_id, body.book_id)
        return LoanOut.model_validate(loan)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch(
    "/{loan_id}/return",
    response_model=LoanOut,
    dependencies=[Depends(require_service_key)],
)
def return_loan(
    loan_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
) -> LoanOut:
    """Record book return. Returns 400 if loan not found or already returned."""
    try:
        loan = loans_service.return_book_service(db, loan_id)
        return LoanOut.model_validate(loan)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/active",
    response_model=list[LoanOut],
    dependencies=[Depends(require_service_key)],
)
def get_active_loans(db: Session = Depends(get_db)) -> list[LoanOut]:
    """Get all loans not yet returned."""
    loans = loans_service.get_active_loans_service(db)
    return [LoanOut.model_validate(loan) for loan in loans]


@router.get(
    "/overdue",
    response_model=list[LoanOut],
    dependencies=[Depends(require_service_key)],
)
def get_overdue_loans(db: Session = Depends(get_db)) -> list[LoanOut]:
    """Get active loans past due date."""
    loans = loans_service.get_overdue_loans_service(db)
    return [LoanOut.model_validate(loan) for loan in loans]
