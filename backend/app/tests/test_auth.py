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