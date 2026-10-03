from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import User
from app.auth.dependencies import require_investigator
from app.services.pipeline_service import get_investigation_detail
from app.services.report_service import generate_pdf_report
from app.services.audit_service import record_audit

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/investigations/{investigation_id}/pdf")
def export_investigation_pdf(
    investigation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_investigator)
):
    inv_detail = get_investigation_detail(investigation_id, db)
    if not inv_detail:
        raise HTTPException(status_code=404, detail="Investigation not found")

    pdf_bytes = generate_pdf_report(inv_detail)

    record_audit(
        db=db,
        user_email=current_user.email,
        role=current_user.role,
        action="REPORT_EXPORTED",
        target=investigation_id,
        metadata={"format": "PDF", "size_bytes": len(pdf_bytes)}
    )

    filename = f"Digital_Fossil_Report_{investigation_id}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )
