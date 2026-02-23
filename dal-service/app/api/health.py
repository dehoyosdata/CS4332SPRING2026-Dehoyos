"""Health check endpoint."""

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_service_key

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


@router.get("/health", dependencies=[Depends(require_service_key)])
def health(db: Session = Depends(get_db)) -> dict:
    """Lightweight DB check via SELECT 1 (vendor-safe)."""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        logger.exception("Health check failed")
        raise HTTPException(status_code=503, detail=f"Database check failed: {e}")
