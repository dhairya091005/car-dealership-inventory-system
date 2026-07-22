"""
test_inventory.py — Tests for inventory management endpoints.

Written BEFORE implementation (TDD Red phase).
Endpoints under test:
  POST /api/vehicles/:id/purchase  — buy a vehicle (quantity decreases by 1)
  POST /api/vehicles/:id/restock   — restock a vehicle (admin only)
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


def add_vehicle(token: str, quantity: int = 5) -> int:
    """Helper: add a vehicle and return its id."""
    resp = client.post(
        "/api/vehicles",
        json={
            "make": "Toyota",
            "model": "Camry",
            "category": "Sedan",
            "price": 25000.0,
            "quantity": quantity,
        },
        headers=auth_headers(token),
    )
    return resp.json()["id"]


# ── POST /api/vehicles/:id/purchase ──────────────────────────────────────────
def test_purchase_decreases_quantity():
    """Purchasing a vehicle reduces its quantity by 1."""
    token = register_and_login("buyer@test.com", "buyer")
    vehicle_id = add_vehicle(token, quantity=5)

    response = client.post(
        f"/api/vehicles/{vehicle_id}/purchase",
        headers=auth_headers(token),
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == 4


def test_purchase_out_of_stock():
    """Purchasing a vehicle with quantity 0 should return 400."""
    token = register_and_login("buyer2@test.com", "buyer2")
    vehicle_id = add_vehicle(token, quantity=0)

    response = client.post(
        f"/api/vehicles/{vehicle_id}/purchase",
        headers=auth_headers(token),
    )

    assert response.status_code == 400
    assert "out of stock" in response.json()["detail"].lower()


def test_purchase_nonexistent_vehicle():
    """Purchasing a vehicle that doesn't exist returns 404."""
    token = register_and_login("buyer3@test.com", "buyer3")

    response = client.post(
        "/api/vehicles/9999/purchase",
        headers=auth_headers(token),
    )

    assert response.status_code == 404


def test_purchase_unauthenticated():
    """Purchase request without a token is rejected."""
    response = client.post("/api/vehicles/1/purchase")
    assert response.status_code == 403


# ── POST /api/vehicles/:id/restock ───────────────────────────────────────────
def test_restock_increases_quantity(db_session):
    """Admin can restock a vehicle, increasing its quantity."""
    from app.models.user import User

    admin_token = register_and_login("admin@test.com", "admin")
    admin = db_session.query(User).filter(User.email == "admin@test.com").first()
    admin.role = "ADMIN"
    db_session.commit()

    vehicle_id = add_vehicle(admin_token, quantity=2)

    response = client.post(
        f"/api/vehicles/{vehicle_id}/restock",
        json={"quantity": 10},
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == 12


def test_restock_forbidden_for_regular_user():
    """Regular user cannot restock — should return 403."""
    token = register_and_login("user@test.com", "regularuser")
    vehicle_id = add_vehicle(token, quantity=2)

    response = client.post(
        f"/api/vehicles/{vehicle_id}/restock",
        json={"quantity": 10},
        headers=auth_headers(token),
    )

    assert response.status_code == 403


def test_restock_nonexistent_vehicle(db_session):
    """Restocking a vehicle that doesn't exist returns 404."""
    from app.models.user import User

    admin_token = register_and_login("admin2@test.com", "admin2")
    admin = db_session.query(User).filter(User.email == "admin2@test.com").first()
    admin.role = "ADMIN"
    db_session.commit()

    response = client.post(
        "/api/vehicles/9999/restock",
        json={"quantity": 5},
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 404


def test_restock_invalid_quantity(db_session):
    """Restocking with quantity <= 0 should return 422 (validation error)."""
    from app.models.user import User

    admin_token = register_and_login("admin3@test.com", "admin3")
    admin = db_session.query(User).filter(User.email == "admin3@test.com").first()
    admin.role = "ADMIN"
    db_session.commit()

    vehicle_id = add_vehicle(admin_token, quantity=2)

    response = client.post(
        f"/api/vehicles/{vehicle_id}/restock",
        json={"quantity": 0},
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 422
