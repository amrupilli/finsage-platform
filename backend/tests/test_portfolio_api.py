import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_user_and_token() -> str:
    unique_email = f"portfolio_{uuid.uuid4().hex[:8]}@example.com"
    password = "securepass123"

    register_response = client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "full_name": "Portfolio User",
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


def complete_onboarding_and_generate_risk_profile(access_token: str) -> int:
    start_response = client.post(
        "/onboarding/start",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert start_response.status_code == 200

    session_id = start_response.json()["session_id"]

    messages = [
        "I want to learn safely",
        "I am a beginner",
        "100 pounds",
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

    return session_id


def test_get_portfolio_scenario_success() -> None:
    access_token = create_user_and_token()
    session_id = complete_onboarding_and_generate_risk_profile(access_token)

    response = client.get(
        f"/onboarding/{session_id}/portfolio-scenario",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["portfolio_type"] == "Conservative Learning Portfolio"
    assert data["total_budget"] == 100.0
    assert len(data["allocations"]) == 3


def test_get_portfolio_scenario_requires_risk_profile() -> None:
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
        "100 pounds",
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

    response = client.get(
        f"/onboarding/{session_id}/portfolio-scenario",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400
    assert "Risk profile must be generated" in response.json()["detail"]