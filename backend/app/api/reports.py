from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.services.pdf_report_service import generate_report_pdf
from app.services.report_service import build_report_for_session

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/{session_id}/download")
def download_report(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    report = build_report_for_session(
        db=db,
        session_id=session_id,
        current_user=current_user,
    )

    pdf_bytes = generate_report_pdf(report)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="finsage-report-session-{session_id}.pdf"'
        },
    )