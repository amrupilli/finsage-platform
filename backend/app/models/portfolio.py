from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.onboarding import OnboardingSession


class PortfolioScenarioSnapshot(Base):
    __tablename__ = "portfolio_scenario_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    session_id: Mapped[int] = mapped_column(
        ForeignKey("onboarding_sessions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    portfolio_type: Mapped[str] = mapped_column(String, nullable=False)
    total_budget: Mapped[float] = mapped_column(Float, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    allocations: Mapped[list] = mapped_column(JSON, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    session: Mapped["OnboardingSession"] = relationship(
        back_populates="portfolio_scenario_snapshot"
    )