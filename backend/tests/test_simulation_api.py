import random
import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_user_and_token() -> str:
    unique_email = f"simulation_{uuid.uuid4().hex[:8]}@example.com"
    password = "securepass123"

    register_response = client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "full_name": "Simulation User",
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


def complete_full_flow_until_portfolio(access_token: str) -> int:
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

    portfolio_response = client.get(
        f"/onboarding/{session_id}/portfolio-scenario",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert portfolio_response.status_code == 200

    return session_id


def test_get_simulation_success() -> None:
    random.seed(42)

    access_token = create_user_and_token()
    session_id = complete_full_flow_until_portfolio(access_token)

    response = client.get(
        f"/onboarding/{session_id}/simulation",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["initial_budget"] == 100.0
    assert data["num_simulations"] == 1000
    assert data["time_horizon_months"] == 12
    assert "metrics" in data
    assert "sample_path" in data
    assert len(data["sample_path"]) == 13
    assert "percentile_band" in data
    assert len(data["percentile_band"]) == 13


def test_get_simulation_requires_portfolio_snapshot() -> None:
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

    risk_response = client.get(
        f"/onboarding/{session_id}/risk-profile",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert risk_response.status_code == 200

    response = client.get(
        f"/onboarding/{session_id}/simulation",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400
    assert "Portfolio scenario must be generated" in response.json()["detail"]