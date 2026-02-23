"""FastAPI application: routes, startup, and dependencies."""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import books, health, loans, reports, students, users
from app.core.config import CORS_ORIGINS, INIT_SCHEMA
from app.core.db import init_schema_with_retry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="CS4332 DAL Service")

# CORS for browser clients (e.g. React, Vue, LibraryDashboard on different port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in CORS_ORIGINS if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router)
app.include_router(users.router)
app.include_router(students.router)
app.include_router(books.router)
app.include_router(loans.router)
app.include_router(reports.router)


@app.on_event("startup")
def startup_event() -> None:
    """Ensure schema exists if INIT_SCHEMA=true. Demo-only; use migrations in production."""
    if INIT_SCHEMA:
        logger.info("INIT_SCHEMA=true: creating tables (demo only)")
        try:
            init_schema_with_retry()
            logger.info("Schema init completed")
        except Exception as e:
            logger.warning("Schema init failed (some vendors need manual setup): %s", e)
    else:
        logger.info("INIT_SCHEMA=false: skipping table creation")
