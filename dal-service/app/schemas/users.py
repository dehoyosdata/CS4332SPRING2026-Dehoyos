"""User request/response schemas."""

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Request schema for creating a user."""

    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"email": "student@university.edu", "password": "MySecurePass123"},
                {"email": "alice@example.com", "password": "changeme123"},
            ]
        }
    }


class UserOut(BaseModel):
    """Response schema for user (no password)."""

    id: int
    email: EmailStr

    model_config = {"from_attributes": True}
