"""Student endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_service_key
from app.schemas import LoanOut, StudentCreate, StudentOut
from app.services import loans_service, students_service

router = APIRouter(prefix="/students", tags=["students"])


@router.post("", response_model=StudentOut, dependencies=[Depends(require_service_key)])
def create_student(
    body: StudentCreate,
    db: Session = Depends(get_db),
) -> StudentOut:
    """Create a student. Returns 409 if email already exists."""
    try:
        student = students_service.create_student_service(
            db, body.name, body.email, body.max_books_allowed
        )
        return StudentOut.model_validate(student)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Student with this email already exists")
    except ValueError as e:
        if "already exists" in str(e):
            raise HTTPException(status_code=409, detail="Student with this email already exists")
        raise


@router.get(
    "/{student_id}",
    response_model=StudentOut,
    dependencies=[Depends(require_service_key)],
)
def get_student(
    student_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
) -> StudentOut:
    """Get student by ID. Returns 404 if not found."""
    student = students_service.get_student_by_id_service(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return StudentOut.model_validate(student)


@router.get(
    "/{student_id}/loans",
    response_model=list[LoanOut],
    dependencies=[Depends(require_service_key)],
)
def get_student_loans(
    student_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
) -> list[LoanOut]:
    """Get loan history for a student."""
    loans = loans_service.get_student_loans_service(db, student_id)
    return [LoanOut.model_validate(loan) for loan in loans]
