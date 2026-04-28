from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def register_and_login_user() -> dict[str, str]:
    register_payload = {
        "email": "validationtester@example.com",
        "password": "StrongPassword123!",
        "full_name": "Validation Tester",
    }

    client.post("/auth/register", json=register_payload)

    login_response = client.post(
        "/auth/login",
        json={
            "email": register_payload["email"],
            "password": register_payload["password"],
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def test_invalid_onboarding_answer_does_not_progress_stage() -> None:
    headers = register_and_login_user()

    start_response = client.post(
        "/onboarding/start",
        headers=headers,
    )

    assert start_response.status_code == 200

    start_data = start_response.json()
    session_id = start_data["session_id"]
    starting_stage = "goal"
    message_response = client.post(
        f"/onboarding/{session_id}/message",
        json={
            "message_text": "asdfgh",
        },
        headers=headers,
    )

    assert message_response.status_code == 200

    message_data = message_response.json()

    assert message_data["current_stage"] == starting_stage
    assert message_data["is_completed"] is False
    assert "more detail" in message_data["assistant_message"].lower()