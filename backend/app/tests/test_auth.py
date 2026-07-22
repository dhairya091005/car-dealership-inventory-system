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