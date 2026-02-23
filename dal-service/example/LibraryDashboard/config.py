"""LibraryDashboard configuration. Loads .env from this package directory."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from LibraryDashboard/ (works regardless of CWD)
_env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_env_path)

DAL_API_URL = os.environ.get("DAL_API_URL", "http://localhost:8000")
DAL_API_KEY = os.environ.get("DAL_API_KEY", "dev-api-key-change-in-production")
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "library-dashboard-secret")
