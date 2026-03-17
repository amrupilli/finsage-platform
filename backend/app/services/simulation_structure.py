from app.schemas.simulation import PortfolioSimulationResult
from app.services.simulation_config import PROFILE_SIMULATION_ASSUMPTIONS


def get_simulation_assumptions(profile: str) -> dict:
    if profile not in PROFILE_SIMULATION_ASSUMPTIONS:
        raise ValueError(f"Unsupported risk profile: {profile}")

    return PROFILE_SIMULATION_ASSUMPTIONS[profile]


def build_simulation_summary(profile: str, months: int) -> str:
    return (
        f"This Monte Carlo simulation models a {months}-month outlook for a {profile} portfolio scenario. "
        f"It is designed to illustrate uncertainty, variability, and downside risk in an educational way."
    )