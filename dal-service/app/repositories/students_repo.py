"""Student repository: direct DB operations."""

from sqlalchemy.orm import Session

from app.models import Student


def get_student_by_id(db: Session, student_id: int) -> Student | None:
    """Return student by ID, or None if not found."""
    return db.query(Student).filter(Student.id == student_id).first()


def get_student_by_email(db: Session, email: str) -> Student | None:
    """Return student by email, or None if not found."""
    return db.query(Student).filter(Student.email == email).first()


def create_student(
    db: Session, name: str, email: str, max_books_allowed: int = 3
) -> Student:
    """Create and persist a student."""
    student = Student(name=name, email=email, max_books_allowed=max_books_allowed)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student
