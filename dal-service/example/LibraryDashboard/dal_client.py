"""Client for the DAL API. Uses only existing endpoints."""

import requests

from config import DAL_API_KEY, DAL_API_URL

HEADERS = {
    "x-api-key": DAL_API_KEY,
    "Content-Type": "application/json",
}


def _url(path: str) -> str:
    return f"{DAL_API_URL.rstrip('/')}{path}"


def get_user_by_email(email: str) -> dict | None:
    """GET /users/by-email. Returns user dict or None (404)."""
    r = requests.get(
        _url("/users/by-email"),
        headers=HEADERS,
        params={"email": email},
        timeout=10,
    )
    if r.status_code == 200:
        return r.json()
    return None


def get_book(book_id: int) -> dict | None:
    """GET /books/{id}. Returns book dict or None."""
    r = requests.get(_url(f"/books/{book_id}"), headers=HEADERS, timeout=10)
    if r.status_code == 200:
        return r.json()
    return None


def get_active_loans() -> list[dict]:
    """GET /loans/active."""
    r = requests.get(_url("/loans/active"), headers=HEADERS, timeout=10)
    if r.status_code == 200:
        return r.json()
    return []


def get_overdue_loans() -> list[dict]:
    """GET /loans/overdue."""
    r = requests.get(_url("/loans/overdue"), headers=HEADERS, timeout=10)
    if r.status_code == 200:
        return r.json()
    return []


def get_bad_history(limit: int = 10) -> list[dict]:
    """GET /reports/bad-history."""
    r = requests.get(
        _url("/reports/bad-history"),
        headers=HEADERS,
        params={"limit": limit},
        timeout=10,
    )
    if r.status_code == 200:
        return r.json()
    return []


def get_good_history(limit: int = 10) -> list[dict]:
    """GET /reports/good-history."""
    r = requests.get(
        _url("/reports/good-history"),
        headers=HEADERS,
        params={"limit": limit},
        timeout=10,
    )
    if r.status_code == 200:
        return r.json()
    return []
