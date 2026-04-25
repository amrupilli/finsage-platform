from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def register_and_login_user() -> dict[str, str]:
    register_payload = {
        "email": "flowtester@example.com",
        "password": "StrongPassword123!",
        "full_name": "Flow Tester",
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


def test_flow_requires_authentication() -> None:
    response = client.get("/flow/1")

    assert response.status_code in {401, 403}


@patch("app.api.flow.run_full_financial_flow")
def test_flow_returns_combined_output(mock_flow) -> None:
    headers = register_and_login_user()

    mock_flow.return_value = {
        "risk_profile": {
            "profile": "Moderate",
            "summary": "Balanced educational risk profile.",
        },
        "portfolio": {
            "summary": "Example educational portfolio scenario.",
            "allocations": [
                {
                    "category": "Stable Digital Assets",
                    "percentage": 60,
                },
                {
                    "category": "Growth Digital Assets",
                    "percentage": 40,
                },
            ],
        },
        "simulation": {
            "metrics": {
                "expected_final_value": 1250.0,
                "probability_of_loss": 0.28,
            },
            "summary": "Simulation shows moderate downside risk.",
        },
        "warnings": [
            {
                "category": "simulation_risk",
                "severity": "medium",
                "title": "Moderate downside risk",
                "message": "The simulation shows a meaningful chance of loss.",
                "recommended_action": "Review downside outcomes before interpreting the result.",
            }
        ],
    }

    response = client.get(
        "/flow/1",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "risk_profile" in data
    assert "portfolio" in data
    assert "simulation" in data
    assert "warnings" in data

    assert data["risk_profile"]["profile"] == "Moderate"
    assert len(data["portfolio"]["allocations"]) == 2
    assert data["simulation"]["metrics"]["probability_of_loss"] == 0.28
    assert data["warnings"][0]["severity"] == "medium"

    mock_flow.assert_called_once()