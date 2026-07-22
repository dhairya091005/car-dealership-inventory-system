"""
test_vehicles.py — Tests for vehicle CRUD endpoints.

Written BEFORE implementation (TDD Red phase).
Endpoints under test:
  POST   /api/vehicles          — add vehicle (protected)
  GET    /api/vehicles          — list all vehicles (protected)
  GET    /api/vehicles/search   — search by make/model/category/price (protected)
  PUT    /api/vehicles/:id      — update vehicle (protected)
  DELETE /api/vehicles/:id      — delete vehicle (admin only)
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ── Helpers ───────────────────────────────────────────────────────────────────
def register_and_login(email: str, username: str, password: str = "password123") -> str:
    """Register a user and return their JWT access token."""
    client.post(
        "/api/auth/register",
        json={"username": username, "email": email, "password": password},
    )
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    return response.json()["access_token"]


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


SAMPLE_VEHICLE = {
    "make": "Toyota",
    "model": "Camry",
    "category": "Sedan",
    "price": 25000.0,
    "quantity": 10,
}


# ── POST /api/vehicles ────────────────────────────────────────────────────────
def test_add_vehicle_authenticated():
    """Authenticated user can add a vehicle."""
    token = register_and_login("user@test.com", "testuser")
    response = client.post(
        "/api/vehicles", json=SAMPLE_VEHICLE, headers=auth_headers(token)
    )
    assert response.status_code == 201
    data = response.json()
    assert data["make"] == "Toyota"
    assert data["model"] == "Camry"
    assert data["id"] is not None


def test_add_vehicle_unauthenticated():
    """Request with no Authorization header should be rejected (403 from HTTPBearer)."""
    response = client.post("/api/vehicles", json=SAMPLE_VEHICLE)
    assert response.status_code == 403


# ── GET /api/vehicles ─────────────────────────────────────────────────────────
def test_get_all_vehicles():
    """Authenticated user can retrieve the full vehicle list."""
    token = register_and_login("user2@test.com", "testuser2")
    # Add a vehicle first
    client.post("/api/vehicles", json=SAMPLE_VEHICLE, headers=auth_headers(token))

    response = client.get("/api/vehicles", headers=auth_headers(token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_vehicles_unauthenticated():
    """Request with no Authorization header should be rejected (403 from HTTPBearer)."""
    response = client.get("/api/vehicles")
    assert response.status_code == 403


# ── GET /api/vehicles/search ──────────────────────────────────────────────────
def test_search_vehicles_by_make():
    """Search endpoint filters vehicles by make."""
    token = register_and_login("user3@test.com", "testuser3")
    client.post("/api/vehicles", json=SAMPLE_VEHICLE, headers=auth_headers(token))
    client.post(
        "/api/vehicles",
        json={**SAMPLE_VEHICLE, "make": "Honda", "model": "Civic"},
        headers=auth_headers(token),
    )

    response = client.get(
        "/api/vehicles/search?make=Toyota", headers=auth_headers(token)
    )
    assert response.status_code == 200
    results = response.json()
    assert all(v["make"] == "Toyota" for v in results)


def test_search_vehicles_by_price_range():
    """Search endpoint filters vehicles by min/max price."""
    token = register_and_login("user4@test.com", "testuser4")
    client.post("/api/vehicles", json=SAMPLE_VEHICLE, headers=auth_headers(token))
    client.post(
        "/api/vehicles",
        json={**SAMPLE_VEHICLE, "price": 60000.0, "model": "Land Cruiser"},
        headers=auth_headers(token),
    )

    response = client.get(
        "/api/vehicles/search?min_price=10000&max_price=30000",
        headers=auth_headers(token),
    )
    assert response.status_code == 200
    results = response.json()
    assert all(10000 <= v["price"] <= 30000 for v in results)


# ── PUT /api/vehicles/:id ─────────────────────────────────────────────────────
def test_update_vehicle():
    """Authenticated user can update a vehicle."""
    token = register_and_login("user5@test.com", "testuser5")
    create_resp = client.post(
        "/api/vehicles", json=SAMPLE_VEHICLE, headers=auth_headers(token)
    )
    vehicle_id = create_resp.json()["id"]

    response = client.put(
        f"/api/vehicles/{vehicle_id}",
        json={**SAMPLE_VEHICLE, "price": 27000.0},
        headers=auth_headers(token),
    )
    assert response.status_code == 200
    assert response.json()["price"] == 27000.0


def test_update_nonexistent_vehicle():
    """Updating a vehicle that doesn't exist returns 404."""
    token = register_and_login("user6@test.com", "testuser6")
    response = client.put(
        "/api/vehicles/9999",
        json=SAMPLE_VEHICLE,
        headers=auth_headers(token),
    )
    assert response.status_code == 404


# ── DELETE /api/vehicles/:id ──────────────────────────────────────────────────
def test_delete_vehicle_as_admin(db_session):
    """Admin user can delete a vehicle."""
    from app.models.user import User

    # Register and promote to ADMIN via direct DB access
    admin_token = register_and_login("admin@test.com", "adminuser")
    admin = db_session.query(User).filter(User.email == "admin@test.com").first()
    admin.role = "ADMIN"
    db_session.commit()

    # Admin adds a vehicle
    create_resp = client.post(
        "/api/vehicles", json=SAMPLE_VEHICLE, headers=auth_headers(admin_token)
    )
    vehicle_id = create_resp.json()["id"]

    response = client.delete(
        f"/api/vehicles/{vehicle_id}", headers=auth_headers(admin_token)
    )
    assert response.status_code == 204


def test_delete_vehicle_as_regular_user(db_session):
    """Regular user (non-admin) cannot delete a vehicle — should return 403."""
    from app.models.user import User

    # Register a regular user
    user_token = register_and_login("regular@test.com", "regularuser")

    # Register and promote admin
    admin_token = register_and_login("admin2@test.com", "adminuser2")
    admin = db_session.query(User).filter(User.email == "admin2@test.com").first()
    admin.role = "ADMIN"
    db_session.commit()

    # Admin adds a vehicle
    create_resp = client.post(
        "/api/vehicles", json=SAMPLE_VEHICLE, headers=auth_headers(admin_token)
    )
    vehicle_id = create_resp.json()["id"]

    # Regular user tries to delete — should be forbidden
    response = client.delete(
        f"/api/vehicles/{vehicle_id}", headers=auth_headers(user_token)
    )
    assert response.status_code == 403

