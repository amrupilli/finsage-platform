import uuid

from fastapi.testclient import TestClient

from app.db.database import SessionLocal
from app.main import app
from app.models.portfolio import PortfolioScenarioSnapshot

client = TestClient(app)


def create_user_and_token() -> str:
    unique_email = f"portfolio_persist_{uuid.uuid4().hex[:8]}@example.com"
    password = "securepass123"

    register_response = client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "full_name": "Portfolio Persistence User",
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


def test_portfolio_scenario_snapshot_is_saved_to_database() -> None:
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

    portfolio_response = client.get(
        f"/onboarding/{session_id}/portfolio-scenario",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert portfolio_response.status_code == 200

    db = SessionLocal()
    try:
        snapshot = (
            db.query(PortfolioScenarioSnapshot)
            .filter(PortfolioScenarioSnapshot.session_id == session_id)
            .first()
        )

        assert snapshot is not None
        assert snapshot.portfolio_type == "Conservative Learning Portfolio"
        assert snapshot.total_budget == 100.0
        assert snapshot.summary != ""
        assert isinstance(snapshot.allocations, list)
        assert len(snapshot.allocations) == 3
    finally:
        db.close()