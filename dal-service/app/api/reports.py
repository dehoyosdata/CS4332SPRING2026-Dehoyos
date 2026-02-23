"""Reports endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_service_key
from app.schemas import StudentOut
from app.services import reports_service

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get(
    "/bad-history",
    dependencies=[Depends(require_service_key)],
)
def get_bad_history(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[dict]:
    """Top students with most late returns (returned_at > due_date)."""
    items = reports_service.get_bad_history_service(db, limit=limit)
    return [
        {"student": StudentOut.model_validate(item["student"]), "late_count": item["late_count"]}
        for item in items
    ]


@router.get(
    "/good-history",
    dependencies=[Depends(require_service_key)],
)
def get_good_history(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[dict]:
    """Top students with most on-time returns (returned_at <= due_date)."""
    items = reports_service.get_good_history_service(db, limit=limit)
    return [
        {
            "student": StudentOut.model_validate(item["student"]),
            "on_time_count": item["on_time_count"],
        }
        for item in items
    ]
