"""User endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_service_key
from app.schemas import UserCreate, UserOut
from app.services import users_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserOut, dependencies=[Depends(require_service_key)])
def create_user(
    body: UserCreate,
    db: Session = Depends(get_db),
) -> UserOut:
    """Create a user. Returns 409 if email already exists."""
    try:
        user = users_service.create_user_service(db, body.email, body.password)
        return UserOut.model_validate(user)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="User with this email already exists")
    except ValueError as e:
        if "already exists" in str(e):
            raise HTTPException(status_code=409, detail="User with this email already exists")
        raise


@router.get(
    "/by-email",
    response_model=UserOut,
    dependencies=[Depends(require_service_key)],
)
def get_user_by_email(
    email: str = Query(..., examples=["test@example.com", "student@university.edu"]),
    db: Session = Depends(get_db),
) -> UserOut:
    """Get user by email query param. Returns 404 if not found."""
    user = users_service.get_user_by_email_service(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut.model_validate(user)
