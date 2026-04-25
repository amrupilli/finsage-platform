from typing import Dict

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def evaluate_scam_model(
    
    y_true: list[int],
    y_pred: list[int],
) -> Dict[str, float]:
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1_score": f1_score(y_true, y_pred, zero_division=0),
    }
def validate_simulation_metrics(metrics: dict) -> dict[str, bool]:
    percentiles = metrics.get("percentiles", {})

    p10 = percentiles.get("p10")
    p50 = percentiles.get("p50")
    p90 = percentiles.get("p90")

    return {
        "expected_final_value_positive": metrics.get("expected_final_value", 0) > 0,
        "probability_of_loss_valid": 0 <= metrics.get("probability_of_loss", -1) <= 1,
        "estimated_volatility_non_negative": metrics.get("estimated_volatility", -1) >= 0,
        "max_drawdown_non_negative": metrics.get("max_drawdown", -1) >= 0,
        "percentiles_ordered": p10 is not None
        and p50 is not None
        and p90 is not None
        and p10 <= p50 <= p90,
    }
def build_system_evaluation_summary(
    scam_metrics: dict[str, float],
    simulation_validation: dict[str, bool],
) -> dict:
    passed_simulation_checks = sum(
        1 for passed in simulation_validation.values() if passed
    )

    total_simulation_checks = len(simulation_validation)

    return {
        "scam_detection": {
            "metrics": scam_metrics,
            "evaluation_method": "Supervised classification metrics using labelled scam-risk examples.",
        },
        "simulation_validation": {
            "checks": simulation_validation,
            "passed_checks": passed_simulation_checks,
            "total_checks": total_simulation_checks,
        },
        "implemented_modules": [
            "authentication",
            "conversational_onboarding",
            "risk_profiling",
            "portfolio_generation",
            "monte_carlo_simulation",
            "scam_detection",
            "warning_explanations",
            "pdf_report_generation",
            "full_product_flow",
        ],
        "summary": (
            "The backend evaluation combines ML classification metrics, "
            "Monte Carlo output validation, and integration-level system checks."
        ),
    }