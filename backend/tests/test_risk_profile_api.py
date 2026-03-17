import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_user_and_token() -> str:
    unique_email = f"riskprofile_{uuid.uuid4().hex[:8]}@example.com"
    password = "securepass123"

    register_response = client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "full_name": "Risk Profile User",
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


def test_get_risk_profile_endpoint() -> None:
    access_token = create_user_and_token()

    start_response = client.post(
        "/onboarding/start",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert start_response.status_code == 200

    session_id = start_response.json()["session_id"]

    messages = [
        "I want to learn safely",
        "I am a beginner",
        "Around 100 pounds",
        "Short term",
        "I would panic and sell",
    ]

    for msg in messages:
        response = client.post(
            f"/onboarding/{session_id}/message",
            json={"message_text": msg},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200

    risk_response = client.get(
        f"/onboarding/{session_id}/risk-profile",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert risk_response.status_code == 200

    data = risk_response.json()
    assert "profile" in data
    assert "total_score" in data
    assert "dimension_scores" in data
    assert "summary" in data