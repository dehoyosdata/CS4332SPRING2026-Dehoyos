"""Student service: business logic for students."""

from sqlalchemy.orm import Session

from app.repositories import students_repo


def create_student_service(
    db: Session, name: str, email: str, max_books_allowed: int = 3
):
    """Create student. Raises ValueError if email already exists."""
    existing = students_repo.get_student_by_email(db, email)
    if existing:
        raise ValueError("Student with this email already exists")
    return students_repo.create_student(db, name, email, max_books_allowed)


def get_student_by_id_service(db: Session, student_id: int):
    """Get student by ID. Returns None if not found."""
    return students_repo.get_student_by_id(db, student_id)
