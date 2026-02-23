"""Loan service: business logic for borrowing and returning books."""

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.repositories import books_repo, loans_repo, students_repo

LOAN_DURATION_DAYS = 14


def borrow_book_service(db: Session, student_id: int, book_id: int):
    """
    Create a loan. Checks: student exists, book exists, student under limit,
    book has copies. Decrements copies_available.
    Raises ValueError on validation failure.
    """
    student = students_repo.get_student_by_id(db, student_id)
    if not student:
        raise ValueError("Student not found")
    book = books_repo.get_book_by_id(db, book_id)
    if not book:
        raise ValueError("Book not found")
    active_count = loans_repo.count_active_loans_for_student(db, student_id)
    if active_count >= student.max_books_allowed:
        raise ValueError(
            f"Student has reached max books allowed ({student.max_books_allowed})"
        )
    if book.copies_available < 1:
        raise ValueError("No copies available")
    due_date = datetime.utcnow() + timedelta(days=LOAN_DURATION_DAYS)
    loan = loans_repo.create_loan(db, student_id, book_id, due_date)
    books_repo.decrement_copies(db, book_id)
    return loan


def return_book_service(db: Session, loan_id: int):
    """
    Record return. Sets returned_at, increments copies_available.
    Raises ValueError if loan not found or already returned.
    """
    loan = loans_repo.get_loan_by_id(db, loan_id)
    if not loan:
        raise ValueError("Loan not found")
    if loan.returned_at is not None:
        raise ValueError("Loan already returned")
    now = datetime.utcnow()
    loans_repo.mark_returned(db, loan_id, now)
    books_repo.increment_copies(db, loan.book_id)
    return loans_repo.get_loan_by_id(db, loan_id)


def get_active_loans_service(db: Session):
    """Return all active (not yet returned) loans."""
    return loans_repo.get_active_loans(db)


def get_overdue_loans_service(db: Session):
    """Return active loans past due date."""
    return loans_repo.get_overdue_loans(db)


def get_student_loans_service(db: Session, student_id: int):
    """Return loan history for a student."""
    return loans_repo.get_student_loans(db, student_id)
