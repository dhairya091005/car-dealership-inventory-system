"""
test_admin.py — Tests for admin user management endpoints.

Written BEFORE implementation (TDD Red phase).
Endpoints under test:
  POST /api/admin/promote-user — promote a user to ADMIN (admin only)
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ── Helpers ───────────────────────────────────────────────────────────────────
def register_and_login(email: str, username: str, password: str = "password123") -> str:
    client.post(
        "/api/auth/register",
        json={"username": username, "email": email, "password": password},
    )
    resp = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    return resp.json()["access_token"]


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def make_admin(email: str, db_session) -> None:
    """Directly promote a user to ADMIN via the test DB."""
    from app.models.user import User
    user = db_session.query(User).filter(User.email == email).first()
    user.role = "ADMIN"
    db_session.commit()


# ── POST /api/admin/promote-user ──────────────────────────────────────────────
def test_admin_can_promote_user(db_session):
    """An admin can promote a regular user to ADMIN by email."""
    from app.models.user import User

    # Create admin
    admin_token = register_and_login("admin@test.com", "adminuser")
    make_admin("admin@test.com", db_session)

    # Create a regular user to promote
    register_and_login("regular@test.com", "regularuser")

    response = client.post(
        "/api/admin/promote-user",
        json={"email": "regular@test.com"},
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "regular@test.com"
    assert data["role"] == "ADMIN"


def test_regular_user_cannot_promote(db_session):
    """A regular (non-admin) user cannot access the promote endpoint."""
    # Register two regular users
    regular_token = register_and_login("user1@test.com", "user1")
    register_and_login("user2@test.com", "user2")

    response = client.post(
        "/api/admin/promote-user",
        json={"email": "user2@test.com"},
        headers=auth_headers(regular_token),
    )

    assert response.status_code == 403


def test_promote_nonexistent_user(db_session):
    """Promoting a user who doesn't exist returns 404."""
    admin_token = register_and_login("admin@test.com", "adminuser")
    make_admin("admin@test.com", db_session)

    response = client.post(
        "/api/admin/promote-user",
        json={"email": "ghost@nowhere.com"},
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 404


def test_promote_unauthenticated():
    """Unauthenticated request to promote endpoint is rejected."""
    response = client.post(
        "/api/admin/promote-user",
        json={"email": "someone@test.com"},
    )
    assert response.status_code == 403


def test_promote_already_admin(db_session):
    """Promoting an already-admin user returns 200 with no error (idempotent)."""
    admin_token = register_and_login("admin@test.com", "adminuser")
    make_admin("admin@test.com", db_session)

    # Try to promote themselves (already admin)
    response = client.post(
        "/api/admin/promote-user",
        json={"email": "admin@test.com"},
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 200
    assert response.json()["role"] == "ADMIN"
