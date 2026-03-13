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


def test_login_user_success() -> None:
    unique_email = f"login_{uuid.uuid4().hex[:8]}@example.com"
    password = "securepass123"

    register_response = client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "full_name": "Login User",
            "password": password,
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": unique_email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    data = login_response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_user_invalid_password() -> None:
    unique_email = f"wrongpass_{uuid.uuid4().hex[:8]}@example.com"

    register_response = client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "full_name": "Wrong Password User",
            "password": "securepass123",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": unique_email,
            "password": "wrongpass123",
        },
    )

    assert login_response.status_code == 401
    assert login_response.json() == {
        "detail": "Invalid email or password."
    }


def test_read_current_user_success() -> None:
    unique_email = f"me_{uuid.uuid4().hex[:8]}@example.com"
    password = "securepass123"

    register_response = client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "full_name": "Current User",
            "password": password,
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": unique_email,
            "password": password,
        },
    )

    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    me_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert me_response.status_code == 200
    data = me_response.json()
    assert data["email"] == unique_email
    assert data["full_name"] == "Current User"


def test_read_current_user_invalid_token() -> None:
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid_token"},
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid authentication token."
    }