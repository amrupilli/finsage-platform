from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.schemas.report import ReportResponse
from app.schemas.warning import UserWarning


client = TestClient(app)


def register_and_login_user() -> dict[str, str]:
    register_payload = {
        "email": "reporttester@example.com",
        "password": "StrongPassword123!",
        "full_name": "Report Tester",
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


def build_sample_report() -> ReportResponse:
    return ReportResponse(
        user_email="student@example.com",
        risk_profile={
            "profile": "Moderate",
            "summary": "Balanced educational profile.",
        },
        portfolio={
            "description": "Example educational portfolio scenario.",
            "allocations": {
                "Stable Digital Assets": 60,
                "Growth Digital Assets": 40,
            },
        },
        simulation={
            "expected_return": 1250.0,
            "probability_of_loss": 0.28,
            "summary": "Moderate downside risk.",
        },
        warnings=[
            UserWarning(
                category="simulation_risk",
                severity="medium",
                title="Moderate downside risk",
                message="Simulation shows a meaningful chance of loss.",
                recommended_action="Review downside outcomes.",
            )
        ],
        disclaimer="This is not financial advice.",
    )


def test_report_download_requires_authentication() -> None:
    response = client.get("/reports/1/download")

    assert response.status_code in {401, 403}


@patch("app.api.reports.generate_report_pdf")
@patch("app.api.reports.build_report_for_session")
def test_report_download_returns_pdf_for_authenticated_user(
    mock_build_report,
    mock_generate_pdf,
) -> None:
    headers = register_and_login_user()

    mock_build_report.return_value = build_sample_report()
    mock_generate_pdf.return_value = b"%PDF-1.4 fake pdf content"

    response = client.get(
        "/reports/1/download",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment" in response.headers["content-disposition"]
    assert response.content.startswith(b"%PDF")