"""LibraryDashboard — Flask app using DAL API endpoints only."""

from flask import Flask, redirect, render_template, request, session, url_for

import dal_client
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY


def login_required(f):
    from functools import wraps

    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return wrapper


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login: validates user exists via GET /users/by-email (demo: no password check)."""
    if request.method == "GET":
        return render_template("login.html", error=None)
    email = request.form.get("email", "").strip()
    if not email:
        return render_template("login.html", error="Email required")
    user = dal_client.get_user_by_email(email)
    if user:
        session["user"] = user
        return redirect(url_for("dashboard"))
    return render_template("login.html", error="User not found. Register via API first.", email=email)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
def index():
    if session.get("user"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    book_id = request.args.get("book_id", "").strip()
    book = None
    if book_id:
        try:
            book = dal_client.get_book(int(book_id))
        except ValueError:
            pass

    active_loans = dal_client.get_active_loans()
    overdue_loans = dal_client.get_overdue_loans()
    bad_history = dal_client.get_bad_history(limit=10)
    good_history = dal_client.get_good_history(limit=10)

    # Enrich loans with book details (cache by book_id to avoid N+1 API calls)
    DISPLAY_LIMIT = 50  # Only enrich first N loans for performance
    book_cache = {}

    def enrich_loans(loans, limit=DISPLAY_LIMIT):
        for loan in loans[:limit]:
            bid = loan["book_id"]
            if bid not in book_cache:
                b = dal_client.get_book(bid)
                book_cache[bid] = b
            b = book_cache[bid]
            loan["book_title"] = b["title"] if b else f"Book #{bid}"
            loan["book_isbn"] = b["isbn"] if b else ""
        return loans[:limit], len(loans)

    active_display, active_total = enrich_loans(active_loans)
    overdue_display, overdue_total = enrich_loans(overdue_loans)

    return render_template(
        "dashboard.html",
        user=session["user"],
        book=book,
        book_id=book_id,
        active_loans=active_display,
        overdue_loans=overdue_display,
        active_total=active_total,
        overdue_total=overdue_total,
        bad_history=bad_history,
        good_history=good_history,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
