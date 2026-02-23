# Example: Apps That Talk to the DAL API

This folder contains **example client applications** that consume the DAL (Data Access Layer) API. The DAL is the single source of truth for data; these apps never talk to the database directly—they only call HTTP endpoints.

---

## Why Build Client Apps?

The DAL API is **framework-agnostic**. You can build clients in any language or stack:

| Stack | Use case |
|-------|----------|
| **Flask / Django** | Web dashboards, admin tools |
| **React / Vue / Svelte** | Single-page apps, rich UIs |
| **Node.js / Express** | Backends that orchestrate multiple services |
| **Mobile (Swift / Kotlin)** | iOS / Android apps |
| **CLI scripts** | Automation, reporting, data export |

All of them talk to the same API: `http://localhost:8000` (or your deployed URL), with the `x-api-key` header.

---

## DAL API Endpoints (Reference)

All endpoints require `x-api-key: <API_KEY>` (from `.env`).

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Health + DB connectivity |
| POST | `/users` | Create user |
| GET | `/users/by-email?email=` | Get user by email |
| POST | `/students` | Create student |
| GET | `/students/{id}` | Get student |
| GET | `/students/{id}/loans` | Student loan history |
| POST | `/books` | Create book |
| GET | `/books/{id}` | Get book by ID |
| POST | `/loans` | Borrow book |
| PATCH | `/loans/{id}/return` | Return book |
| GET | `/loans/active` | Active loans |
| GET | `/loans/overdue` | Overdue loans |
| GET | `/reports/bad-history` | Top late returns |
| GET | `/reports/good-history` | Top on-time returns |

---

## App Ideas Students Can Build

### 1. **LibraryDashboard** (included)
Flask app with login, book lookup, charts, and tables. See `LibraryDashboard/` for a full reference.

### 2. **Mobile-style PWA**
A React or Vue SPA for students to:
- Browse available books (via repeated `GET /books/{id}` or batch calls)
- See their loan history (`GET /students/{id}/loans`)
- Check due dates and overdue status

### 3. **Librarian CLI**
A Python script or Node CLI that:
- Lists active/overdue loans
- Looks up students and books by ID
- Calls `PATCH /loans/{id}/return` to record returns

### 4. **Analytics / Reporting Tool**
- Fetches `bad-history` and `good-history`
- Plots trends over time (if you add date filters to the API)
- Exports to CSV or PDF

### 5. **Student Self-Service Portal**
- Login via `GET /users/by-email` (or a future auth endpoint)
- View and return loans
- Request new loans (calls `POST /loans`)

### 6. **Slack / Discord Bot**
- Commands like `/library status` → calls `/loans/active` and summarizes
- `/library return 123` → calls `PATCH /loans/123/return`

---

## Design Pattern: API Client Layer

Each app typically has a small **API client** that wraps HTTP calls:

```
Your App                    DAL API
    |                          |
    |  GET /loans/active       |
    |  x-api-key: xxx          |
    | -----------------------> |
    |  JSON response           |
    | <----------------------- |
    |                          |
    |  (Your app renders UI,    |
    |   runs business logic)   |
```

Example structure:
```
my-app/
├── api_client.py    # or dal_client.js — functions that call the DAL
├── app.py           # or main.tsx — your UI / routes
├── .env             # DAL_API_URL, DAL_API_KEY
└── requirements.txt
```

The client should:
- Use a base URL from config (e.g. `http://localhost:8000`)
- Send `x-api-key` on every request
- Handle errors (404, 401, 503)
- Optionally cache responses to avoid N+1 calls (see LibraryDashboard performance notes)

---

## Key Considerations

### Authentication
- The DAL uses **API-key** auth (`x-api-key` header). Your app stores this key and sends it.
- For end-user login, validate via `GET /users/by-email` (or a future login endpoint). Store the user in your session.

### Performance
- **Avoid N+1 calls**: If you fetch 100 loans and then fetch each book with `GET /books/{id}`, that’s 100 extra requests. Cache book lookups by `book_id`, or limit how many rows you enrich.
- **Use aggregated endpoints**: Prefer `GET /reports/bad-history` over fetching all loans and aggregating yourself.

### No DAL Changes
- These example apps use **only existing API endpoints**. Do not modify the DAL to add new routes for your project unless instructed.
- If the API doesn’t expose what you need, work within its limits (e.g. paginate, limit display, combine multiple calls).

---

## Quick Start (Any New App)

1. **Create a project** (Flask, React, Node, etc.).
2. **Add an API client** that calls the DAL with `requests` (Python), `fetch` (JS), or your language’s HTTP lib.
3. **Set env vars**: `DAL_API_URL=http://localhost:8000`, `DAL_API_KEY=dev-api-key-change-in-production`
4. **Start the DAL**: `docker compose --profile postgres up -d`
5. **Run your app** and point it at the DAL.

---

## LibraryDashboard as Reference

`LibraryDashboard/` is a complete Flask example. It shows:
- Config via `.env`
- A `dal_client` module for all API calls
- Session-based login (email validation)
- Dashboard with charts and tables
- Caching and display limits to avoid slow N+1 requests

Use it as a template when building your own client.
