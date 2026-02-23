"""Reports service: bad/good history rankings."""

from sqlalchemy.orm import Session

from app.repositories import loans_repo, students_repo


def get_bad_history_service(db: Session, limit: int = 10):
    """
    Top students with most late returns (returned_at > due_date).
    Returns list of {student, late_count}.
    """
    pairs = loans_repo.get_late_return_count_by_student(db, limit=limit)
    result = []
    for student_id, late_count in pairs:
        student = students_repo.get_student_by_id(db, student_id)
        if student:
            result.append({"student": student, "late_count": late_count})
    return result


def get_good_history_service(db: Session, limit: int = 10):
    """
    Top students with most on-time returns (returned_at <= due_date).
    Returns list of {student, on_time_count}.
    """
    pairs = loans_repo.get_on_time_return_count_by_student(db, limit=limit)
    result = []
    for student_id, on_time_count in pairs:
        student = students_repo.get_student_by_id(db, student_id)
        if student:
            result.append({"student": student, "on_time_count": on_time_count})
    return result
