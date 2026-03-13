import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_user_success() -> None:
    unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"

    response = client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "full_name": "Test User",
            "password": "securepass123",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["email"] == unique_email
    assert data["full_name"] == "Test User"
    assert data["is_active"] is True
    assert "id" in data
    assert "created_at" in data
    assert "password" not in data


def test_register_user_duplicate_email() -> None:
    unique_email = f"duplicate_{uuid.uuid4().hex[:8]}@example.com"

    first_response = client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "full_name": "Duplicate User",
            "password": "securepass123",
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "full_name": "Duplicate User",
            "password": "securepass123",
        },
    )

    assert second_response.status_code == 400
    assert second_response.json() == {
        "detail": "A user with this email already exists."
    }