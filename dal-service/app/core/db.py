"""SQLAlchemy engine, session factory, and dependency for FastAPI."""

import logging
import time
from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import (
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
    DB_VENDOR,
)
from app.models import Base

logger = logging.getLogger(__name__)

_urls = {
    "postgres": f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    "mysql": f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
}
DATABASE_URL = _urls[DB_VENDOR]

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


_last_connect_error: str | None = None


def _can_connect() -> bool:
    """Test if DB is reachable via SELECT 1."""
    global _last_connect_error
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        _last_connect_error = None
        return True
    except Exception as e:
        _last_connect_error = str(e)
        return False


def init_schema() -> None:
    """Create tables if INIT_SCHEMA is enabled. Use cautiously (demo only)."""
    Base.metadata.create_all(bind=engine)


def init_schema_with_retry(max_attempts: int = 24, delay_seconds: int = 5) -> None:
    """
    Wait for DB to be ready, then create schema.
    """
    for attempt in range(1, max_attempts + 1):
        if _can_connect():
            logger.info("Database connection OK (attempt %d)", attempt)
            init_schema()
            return
        logger.warning(
            "Database not ready (attempt %d/%d), retrying in %ds... (error: %s)",
            attempt,
            max_attempts,
            delay_seconds,
            _last_connect_error or "unknown",
        )
        time.sleep(delay_seconds)
    raise RuntimeError(
        f"Database unavailable after {max_attempts} attempts."
    )
