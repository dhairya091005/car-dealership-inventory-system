from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_user():
    response = client.post(
        "/api/auth/register",
        json={
            "username": "john",
            "email": "john@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 201


def test_duplicate_email():
    client.post(
        "/api/auth/register",
        json={
            "username": "john",
            "email": "john@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/auth/register",
        json={
            "username": "john2",
            "email": "john@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 400

def test_login_user():
    # Register user first
    client.post(
        "/api/auth/register",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "password123"
        }
    )

    # Try logging in
    response = client.post(
        "/api/auth/login",
        json={
            "email": "alice@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200