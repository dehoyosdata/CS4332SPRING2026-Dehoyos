"""Loan repository: direct DB operations."""

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Loan


def get_loan_by_id(db: Session, loan_id: int) -> Loan | None:
    """Return loan by ID, or None if not found."""
    return db.query(Loan).filter(Loan.id == loan_id).first()


def create_loan(
    db: Session, student_id: int, book_id: int, due_date: datetime
) -> Loan:
    """Create and persist a loan."""
    loan = Loan(student_id=student_id, book_id=book_id, due_date=due_date)
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan


def mark_returned(db: Session, loan_id: int, returned_at: datetime) -> Loan | None:
    """Set returned_at for a loan. Returns updated loan or None."""
    loan = get_loan_by_id(db, loan_id)
    if not loan:
        return None
    loan.returned_at = returned_at
    db.commit()
    db.refresh(loan)
    return loan


def count_active_loans_for_student(db: Session, student_id: int) -> int:
    """Count loans where returned_at IS NULL for a student."""
    return db.query(Loan).filter(
        Loan.student_id == student_id,
        Loan.returned_at.is_(None),
    ).count()


def get_active_loans(db: Session) -> list[Loan]:
    """Return all loans not yet returned."""
    return db.query(Loan).filter(Loan.returned_at.is_(None)).all()


def get_overdue_loans(db: Session) -> list[Loan]:
    """Return active loans past due date."""
    now = datetime.utcnow()
    return (
        db.query(Loan)
        .filter(Loan.returned_at.is_(None), Loan.due_date < now)
        .all()
    )


def get_student_loans(db: Session, student_id: int) -> list[Loan]:
    """Return all loans for a student (history)."""
    return db.query(Loan).filter(Loan.student_id == student_id).all()


def get_late_return_count_by_student(db: Session, limit: int = 10) -> list[tuple[int, int]]:
    """Return (student_id, late_count) for students with most late returns.
    Late = returned_at > due_date.
    """
    subq = (
        db.query(Loan.student_id, func.count(Loan.id).label("late_count"))
        .filter(Loan.returned_at.isnot(None))
        .filter(Loan.returned_at > Loan.due_date)
        .group_by(Loan.student_id)
        .subquery()
    )
    rows = (
        db.query(subq.c.student_id, subq.c.late_count)
        .order_by(subq.c.late_count.desc())
        .limit(limit)
        .all()
    )
    return [(r.student_id, r.late_count) for r in rows]


def get_on_time_return_count_by_student(db: Session, limit: int = 10) -> list[tuple[int, int]]:
    """Return (student_id, on_time_count) for students with most on-time returns.
    On-time = returned_at <= due_date.
    """
    subq = (
        db.query(Loan.student_id, func.count(Loan.id).label("on_time_count"))
        .filter(Loan.returned_at.isnot(None))
        .filter(Loan.returned_at <= Loan.due_date)
        .group_by(Loan.student_id)
        .subquery()
    )
    rows = (
        db.query(subq.c.student_id, subq.c.on_time_count)
        .order_by(subq.c.on_time_count.desc())
        .limit(limit)
        .all()
    )
    return [(r.student_id, r.on_time_count) for r in rows]
