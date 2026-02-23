# 🎯 CS4332 DAL Challenge — Level Up Your Skills!

Hey there, future architect! 👋

Before you build the next Uber-for-Libraries (or whatever's hot on Hacker News), let's make sure you really *get* this project. It's not just "another CRUD API"—it's a **Data Access Layer as a Service**, and that pattern shows up everywhere: microservices, mobile backends, multi-tenant SaaS, you name it.

Think of it like learning to drive: you've got the wheel (your app), the pedals (HTTP calls), and the engine (the database). The DAL is the **gearbox**—it keeps you from grinding gears every time you want to fetch a book. 🚗

---

## 🌍 Real-World Vibe

**Where does this pattern actually show up?**

- **Stripe, Twilio, SendGrid** — You call their APIs; they hide databases and internal complexity from you.
- **Internal platforms** — One team owns the DAL, others build dashboards, mobile apps, and CLIs on top of it.
- **Multi-database setups** — Same API, different DBs (Postgres today, maybe CockroachDB later). Clients don't care.

**What's different in "real" production?**

- Auth would be JWT/OAuth, not just an API key.
- You'd use migrations (Alembic), not `create_all()`.
- Rate limiting, observability, and scaling would be first-class. But the *idea*—one API as the gatekeeper to your data—is exactly what we're practicing here.

---

## 📋 Your Challenge Checklist

### 1. 🧩 Understand the Big Picture
**Can you go over this project and understand what we're actually trying to do?**

Walk through: `app/`, `scripts/`, `example/`. Trace a request from curl → FastAPI → Service → Repository → SQLAlchemy → DB. Draw it if it helps!

---

### 2. 📚 Define the DAL
**What is a DAL? And why are we doing this here?**

Hint: It's not "a database." It's a *layer*. Think: Who talks to whom? Who *doesn't* talk to the DB directly?

---

### 3. 🗄️ Hands-On: DBeaver
**Did you successfully run this project and connect to DBeaver and understand what's happening?**

- Start Docker, run the seed.
- Connect DBeaver to Postgres (or MySQL).
- Open `users`, `students`, `books`, `loans`.
- Run a few queries. See the data that your API is serving.

---

### 4. 🖼️ Explore the Example
**Did you understand what's happening in the example folder?**

- Run LibraryDashboard.
- Log in with `alice@university.edu`.
- See how it calls the DAL API and renders the UI.
- Read `example/README.md` for app ideas.

---

### 5. 🚀 Extend the DAL
**Can you extend the current DAL service to add a few more creative endpoints that help upgrade our LibraryDashboard with more visualizations?**

Ideas: most-borrowed books, overdue rate by month, books-by-subject, etc. Remember: no client talks to the DB—everything goes through the API.

---

### 6. 🌐 New Domain
**Can you extend this example to implement some other real-world data?**

Examples: inventory, events, courses, support tickets. Pick a domain you care about, add models, migrations (or schema init), and endpoints. Then build a small client (Flask, React, CLI) that uses your new DAL.

---

### 7. 🔬 SQLAlchemy Under the Hood
**Do you know how SQLAlchemy is running your SQL query under the hood?**

- Where does `db.query(User).filter(...)` become `SELECT * FROM users WHERE ...`?
- What's the difference between the Session, the Engine, and the connection pool?
- Open `app/repositories/` and trace one function end-to-end.

---

### 8. 👁️ See the SQL
**Are you able to go and see how these queries are actually translated?**

Enable SQLAlchemy echoing:
```python
engine = create_engine(DATABASE_URL, echo=True)  # Logs SQL to stdout
```
Run a request and watch the SQL in the terminal. Compare it to what you expected.

---

### 9. 🧪 Implement API Tests
**Can you add tests for the DAL API?**

Create a `tests/` folder and implement pytest tests that run without Docker. Use an in-memory SQLite DB so tests are fast and isolated.

**How:**
- Add `pytest` and `httpx` to `requirements.txt`
- Support `TESTING=1` in `config.py` and `db.py`: when set, skip Postgres/MySQL validation and use `sqlite:///:memory:` with `StaticPool`
- Set `TESTING=1` in `conftest.py` (e.g. via `os.environ`) *before* importing the app
- Use FastAPI’s `TestClient` and `app.dependency_overrides[get_db]` to inject a test DB session
- Create tables with `Base.metadata.create_all(bind=engine)` before each test (or in a fixture)
- Tear down tables after each test so the next test gets a clean DB

**What to test:**
- `GET /health` — returns 422 without API key, 401 with wrong key, 200 with valid key
- `POST /users` — creates user and returns UserOut; returns 409 for duplicate email
- `GET /users/by-email` — returns user when found, 404 when not found

Run with: `pytest tests/ -v`

---

## 🏁 You're Done When…

- You can explain the DAL pattern to a teammate in one minute.
- You've run the project, seeded data, and connected DBeaver.
- You've added at least one new endpoint and used it in a client (e.g., LibraryDashboard or your own).
- You've seen raw SQL in the logs and matched it to a repository call.

Have fun building! 🎉
