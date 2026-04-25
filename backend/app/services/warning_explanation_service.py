from app.schemas.scam_detection import ScamPredictionResponse
from app.schemas.warning import UserWarning


def build_warning_from_scam_prediction(
    prediction: ScamPredictionResponse,
) -> UserWarning:
    if prediction.risk_level == "high":
        return UserWarning(
            category="scam_risk",
            severity="high",
            title="High scam-risk language detected",
            message=(
                "This message contains strong warning signs such as guaranteed returns, "
                "urgency pressure, unrealistic profit claims, or private contact requests."
            ),
            recommended_action=(
                "Do not send money or wallet details. Check independent sources and treat the claim as high risk."
            ),
        )

    if prediction.risk_level == "medium":
        return UserWarning(
            category="scam_risk",
            severity="medium",
            title="Some suspicious investment signals detected",
            message=(
                "This message contains some risk indicators. It may not be a confirmed scam, "
                "but the wording suggests caution is needed."
            ),
            recommended_action=(
                "Slow down, compare the claim with trusted sources, and check whether risks are clearly explained."
            ),
        )

    return UserWarning(
        category="educational_guidance",
        severity="low",
        title="No major scam-risk language detected",
        message=(
            "The message does not contain strong scam indicators based on the current model and rule checks."
        ),
        recommended_action=(
            "Still research independently. A low-risk result does not mean the investment itself is safe."
        ),
    )


def build_simulation_warning(probability_of_loss: float) -> UserWarning:
    if probability_of_loss >= 0.5:
        return UserWarning(
            category="simulation_risk",
            severity="high",
            title="High probability of loss in simulated outcomes",
            message=(
                "The simulation suggests that many projected outcomes may finish below the starting value."
            ),
            recommended_action=(
                "Review the risk profile, reduce exposure, or compare lower-risk scenarios before interpreting results."
            ),
        )

    if probability_of_loss >= 0.25:
        return UserWarning(
            category="simulation_risk",
            severity="medium",
            title="Moderate downside risk in simulation",
            message=(
                "The simulation shows a meaningful chance of ending below the starting value."
            ),
            recommended_action=(
                "Compare the median outcome with downside percentiles before drawing conclusions."
            ),
        )

    return UserWarning(
        category="educational_guidance",
        severity="low",
        title="Lower simulated downside risk",
        message=(
            "The simulation shows a lower probability of loss under the current assumptions."
        ),
        recommended_action=(
            "Remember that simulations are simplified educational models, not guaranteed forecasts."
        ),
    )


def build_portfolio_concentration_warning(
    largest_allocation_percentage: float,
) -> UserWarning:
    if largest_allocation_percentage >= 60:
        return UserWarning(
            category="portfolio_risk",
            severity="high",
            title="High portfolio concentration detected",
            message=(
                "A large share of the scenario is concentrated in one asset category, which may increase risk."
            ),
            recommended_action=(
                "Consider reviewing diversification and comparing a more balanced educational scenario."
            ),
        )

    if largest_allocation_percentage >= 40:
        return UserWarning(
            category="portfolio_risk",
            severity="medium",
            title="Moderate concentration risk",
            message=(
                "One asset category has a relatively large allocation, so the outcome may depend heavily on that category."
            ),
            recommended_action=(
                "Check how diversification affects the simulation range and downside outcomes."
            ),
        )

    return UserWarning(
        category="educational_guidance",
        severity="low",
        title="No major concentration warning",
        message=(
            "The portfolio scenario appears reasonably diversified based on allocation size."
        ),
        recommended_action=(
            "Still review all asset categories and remember that diversification does not remove all risk."
        ),
    )