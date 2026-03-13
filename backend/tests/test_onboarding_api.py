import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_user_and_token() -> str:
    unique_email = f"onboarding_{uuid.uuid4().hex[:8]}@example.com"
    password = "securepass123"

    register_response = client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "full_name": "Onboarding User",
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

    return login_response.json()["access_token"]


def test_start_onboarding_session() -> None:
    access_token = create_user_and_token()

    response = client.post(
        "/onboarding/start",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["current_stage"] == "intro"
    assert data["is_completed"] is False
    assert "interested in digital investing or crypto" in data["assistant_message"]


def test_send_onboarding_message() -> None:
    access_token = create_user_and_token()

    start_response = client.post(
        "/onboarding/start",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert start_response.status_code == 200

    session_id = start_response.json()["session_id"]

    response = client.post(
        f"/onboarding/{session_id}/message",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"message_text": "I want to learn how crypto works safely."},
    )

    assert response.status_code == 200
    data = response.json()
    assert "assistant_message" in data
    assert data["is_completed"] is False