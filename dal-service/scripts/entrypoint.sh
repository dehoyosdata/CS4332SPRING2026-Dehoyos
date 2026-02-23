#!/bin/sh
# Run seed script first when SEED_LIBRARY_DATA=true, then start uvicorn.
set -e

if [ "$SEED_LIBRARY_DATA" = "true" ]; then
  echo "[entrypoint] Running seed script (SEED_LIBRARY_DATA=true)..."
  python scripts/seed_library_data.py
  echo "[entrypoint] Seed complete."
fi

exec uvicorn app.main:app --host 0.0.0.0 --port 8000
