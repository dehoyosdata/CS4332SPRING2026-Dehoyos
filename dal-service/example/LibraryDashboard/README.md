# LibraryDashboard

Flask app that visualizes library data by querying the DAL API. Runs locally (not in Docker). **Uses only existing API endpoints** — no DAL modifications.

## API endpoints used

| Endpoint | Purpose |
|----------|---------|
| `GET /users/by-email` | Login (validates user exists) |
| `GET /books/{id}` | Book lookup by ID |
| `GET /loans/active` | Active loans |
| `GET /loans/overdue` | Overdue loans |
| `GET /reports/bad-history` | Top students with late returns |
| `GET /reports/good-history` | Top students with on-time returns |

## Quick start

```bash
cd LibraryDashboard
cp .env.example .env   # optional: edit .env to override DAL_API_URL, DAL_API_KEY

# Activate venv and install (if not already done)
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt

python app.py
```

Then open http://localhost:5000

**Prerequisites:** DAL API running (`docker compose --profile postgres up -d`). If seeded, use `alice@university.edu` … `jack@university.edu` (password `password123`). Or create via `POST /users`.

## Configuration

Copy `.env.example` to `.env` and adjust as needed:

| Variable | Default | Description |
|----------|---------|-------------|
| `DAL_API_URL` | `http://localhost:8000` | DAL API base URL |
| `DAL_API_KEY` | `dev-api-key-change-in-production` | Must match `API_KEY` in DAL `.env` |
| `FLASK_SECRET_KEY` | (required for sessions) | Set a random value for production |
