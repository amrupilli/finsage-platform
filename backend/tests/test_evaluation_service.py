from app.services.evaluation_service import (
    build_system_evaluation_summary,
    evaluate_scam_model,
    validate_simulation_metrics,
)

def test_evaluate_scam_model_returns_metrics() -> None:
    y_true = [1, 0, 1, 0]
    y_pred = [1, 0, 0, 0]

    metrics = evaluate_scam_model(y_true, y_pred)

    assert "accuracy" in metrics
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1_score" in metrics

    assert 0 <= metrics["accuracy"] <= 1
    assert 0 <= metrics["precision"] <= 1
    assert 0 <= metrics["recall"] <= 1
    assert 0 <= metrics["f1_score"] <= 1

def test_validate_simulation_metrics_returns_validation_flags() -> None:
    metrics = {
        "expected_final_value": 1250.0,
        "probability_of_loss": 0.28,
        "estimated_volatility": 0.12,
        "max_drawdown": 0.18,
        "percentiles": {
            "p10": 900.0,
            "p50": 1250.0,
            "p90": 1700.0,
        },
    }

    validation = validate_simulation_metrics(metrics)

    assert validation["expected_final_value_positive"] is True
    assert validation["probability_of_loss_valid"] is True
    assert validation["estimated_volatility_non_negative"] is True
    assert validation["max_drawdown_non_negative"] is True
    assert validation["percentiles_ordered"] is True

def test_build_system_evaluation_summary_contains_key_sections() -> None:
    scam_metrics = {
        "accuracy": 0.85,
        "precision": 0.8,
        "recall": 0.75,
        "f1_score": 0.77,
    }

    simulation_validation = {
        "expected_final_value_positive": True,
        "probability_of_loss_valid": True,
        "estimated_volatility_non_negative": True,
        "max_drawdown_non_negative": True,
        "percentiles_ordered": True,
    }

    summary = build_system_evaluation_summary(
        scam_metrics=scam_metrics,
        simulation_validation=simulation_validation,
    )

    assert "scam_detection" in summary
    assert "simulation_validation" in summary
    assert "implemented_modules" in summary
    assert "summary" in summary

    assert summary["simulation_validation"]["passed_checks"] == 5
    assert "monte_carlo_simulation" in summary["implemented_modules"]
    assert "scam_detection" in summary["implemented_modules"]