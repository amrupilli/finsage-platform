from app.schemas.report import ReportResponse


def test_report_schema_structure() -> None:
    report = ReportResponse(
        user_email="test@example.com",
        risk_profile={
            "profile": "Moderate",
            "summary": "Balanced approach.",
        },
        portfolio={
            "description": "Example portfolio",
            "allocations": {"Stocks": 60, "Bonds": 40},
        },
        simulation={
            "expected_return": 0.08,
            "probability_of_loss": 0.2,
            "summary": "Moderate growth potential.",
        },
        warnings=[],
        disclaimer="This is not financial advice.",
    )

    assert report.user_email == "test@example.com"
    assert report.risk_profile.profile == "Moderate"
    assert report.portfolio.allocations["Stocks"] == 60
    assert report.simulation.expected_return == 0.08