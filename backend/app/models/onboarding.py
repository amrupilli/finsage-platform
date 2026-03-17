from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
if TYPE_CHECKING:
    from app.models.risk_profile import RiskProfileSnapshot
    from app.models.portfolio import PortfolioScenarioSnapshot

class OnboardingSession(Base):
    __tablename__ = "onboarding_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    answers: Mapped[list["OnboardingAnswer"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )


    risk_profile_snapshot: Mapped["RiskProfileSnapshot | None"] = relationship(
    back_populates="session",
    uselist=False,
    cascade="all, delete-orphan",
)
    portfolio_scenario_snapshot: Mapped["PortfolioScenarioSnapshot | None"] = relationship(
    back_populates="session",
    uselist=False,
    cascade="all, delete-orphan",
)

class OnboardingAnswer(Base):
    __tablename__ = "onboarding_answers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("onboarding_sessions.id"),
        nullable=False,
        index=True,
    )
    question_key: Mapped[str] = mapped_column(String(100), nullable=False)
    answer_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    session: Mapped["OnboardingSession"] = relationship(back_populates="answers")