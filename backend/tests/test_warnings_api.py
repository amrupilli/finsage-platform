from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def register_and_login_user() -> dict[str, str]:
    register_payload = {
        "email": "scamtester@example.com",
        "password": "StrongPassword123!",
        "full_name": "Scam Tester",
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


def test_scam_check_requires_authentication() -> None:
    response = client.post(
        "/warnings/scam-check",
        json={
            "text": "Guaranteed profit with 20% daily return. Act now.",
        },
    )

    assert response.status_code in {401, 403}


def test_scam_check_returns_prediction_for_authenticated_user() -> None:
    headers = register_and_login_user()

    response = client.post(
        "/warnings/scam-check",
        json={
            "text": "Guaranteed profit with 20% daily return. Act now and send your wallet address.",
        },
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["input_text"]
    assert data["predicted_label"] in {"safe", "suspicious", "scam"}
    assert data["risk_level"] in {"low", "medium", "high"}
    assert 0.0 <= data["scam_probability"] <= 1.0
    assert len(data["warning_signals"]) >= 1
    assert len(data["investment_checklist"]) >= 5
    assert data["explanation"]
    assert data["educational_message"]