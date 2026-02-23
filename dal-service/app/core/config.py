"""Load configuration from environment. Fail-fast if required vars are missing."""

import os
from typing import Literal

from dotenv import load_dotenv

load_dotenv()

DB_VENDOR = os.environ.get("DB_VENDOR", "").lower()
if DB_VENDOR not in ("postgres", "mysql"):
    raise ValueError(
        f"DB_VENDOR must be one of: postgres, mysql. Got: {DB_VENDOR!r}"
    )

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

for name, val in [
    ("DB_HOST", DB_HOST),
    ("DB_PORT", DB_PORT),
    ("DB_NAME", DB_NAME),
    ("DB_USER", DB_USER),
    ("DB_PASSWORD", DB_PASSWORD),
]:
    if not val:
        raise ValueError(f"Missing required env var: {name}")

API_KEY = os.environ.get("API_KEY", "dev-api-key-change-in-production")
INIT_SCHEMA = os.environ.get("INIT_SCHEMA", "false").lower() in ("true", "1", "yes")

# CORS: comma-separated origins (e.g. http://localhost:3000,http://localhost:5000)
CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:3000,http://localhost:5000").split(",")

DBVendor = Literal["postgres", "mysql"]
