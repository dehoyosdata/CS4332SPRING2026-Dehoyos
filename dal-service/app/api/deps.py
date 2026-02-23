"""Shared dependencies: re-export get_db and require_service_key."""

from app.core.db import get_db
from app.core.security import require_service_key

__all__ = ["get_db", "require_service_key"]
