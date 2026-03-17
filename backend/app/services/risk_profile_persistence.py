from sqlalchemy.orm import Session

from app.models.risk_profile import RiskProfileSnapshot
from app.schemas.risk_profile import RiskProfileResult


def save_risk_profile_snapshot(
    db: Session,
    session_id: int,
    risk_profile: RiskProfileResult,
) -> RiskProfileSnapshot:
    existing_snapshot = (
        db.query(RiskProfileSnapshot)
        .filter(RiskProfileSnapshot.session_id == session_id)
        .first()
    )

    dimension_scores_payload = [
        {
            "dimension": item.dimension,
            "score": item.score,
            "rationale": item.rationale,
        }
        for item in risk_profile.dimension_scores
    ]

    if existing_snapshot:
        existing_snapshot.profile_label = risk_profile.profile
        existing_snapshot.total_score = risk_profile.total_score
        existing_snapshot.summary = risk_profile.summary
        existing_snapshot.dimension_scores = dimension_scores_payload

        db.add(existing_snapshot)
        db.commit()
        db.refresh(existing_snapshot)
        return existing_snapshot

    snapshot = RiskProfileSnapshot(
        session_id=session_id,
        profile_label=risk_profile.profile,
        total_score=risk_profile.total_score,
        summary=risk_profile.summary,
        dimension_scores=dimension_scores_payload,
    )

    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot