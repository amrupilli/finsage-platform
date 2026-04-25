from app.schemas.report import ReportResponse
from app.schemas.warning import UserWarning
from app.services.pdf_report_service import generate_report_pdf


def test_generate_report_pdf_returns_pdf_bytes() -> None:
    report = ReportResponse(
        user_email="student@example.com",
        risk_profile={
            "profile": "Moderate",
            "summary": "The user has a balanced educational risk profile.",
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
            "summary": "The simulation shows moderate downside risk.",
        },
        warnings=[
            UserWarning(
                category="simulation_risk",
                severity="medium",
                title="Moderate downside risk",
                message="The simulation shows a meaningful chance of loss.",
                recommended_action="Review downside outcomes before interpreting the result.",
            )
        ],
        disclaimer="This is not financial advice.",
    )

    pdf_bytes = generate_report_pdf(report)

    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes.startswith(b"%PDF")
    assert len(pdf_bytes) > 1000