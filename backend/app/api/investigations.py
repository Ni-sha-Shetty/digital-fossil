from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import User
from app.models.investigation import Investigation, InvestigationNote
from app.models.session import Session as SessionModel
from app.auth.dependencies import get_current_user, require_investigator, require_reviewer
from app.schemas.investigation import (
    InvestigationSummary, InvestigationDetail, NoteCreate, NoteResponse, ReviewerVerdictRequest
)
from app.services.pipeline_service import get_investigation_detail
from app.services.audit_service import record_audit

router = APIRouter(prefix="/investigations", tags=["Investigations"])

@router.get("", response_model=List[InvestigationSummary])
def list_investigations(
    search: Optional[str] = None,
    status_filter: Optional[str] = None,
    confidence_filter: Optional[str] = None,
    anomaly_only: Optional[bool] = False,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Investigation)

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Investigation.title.ilike(search_pattern)) |
            (Investigation.investigation_id.ilike(search_pattern)) |
            (Investigation.session_id.ilike(search_pattern))
        )

    if status_filter:
        query = query.filter(Investigation.status == status_filter)

    if confidence_filter:
        query = query.filter(Investigation.confidence_label == confidence_filter.upper())

    if anomaly_only:
        anomalous_sessions = db.query(SessionModel.session_id).filter(SessionModel.is_anomaly == True).subquery()
        query = query.filter(Investigation.session_id.in_(anomalous_sessions))

    investigations = query.order_by(Investigation.created_at.desc()).offset(skip).limit(limit).all()
    return investigations

@router.get("/{investigation_id}", response_model=InvestigationDetail)
def get_investigation(
    investigation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    detail = get_investigation_detail(investigation_id, db)
    if not detail:
        raise HTTPException(status_code=404, detail=f"Investigation '{investigation_id}' not found.")
    
    # Audit view
    record_audit(
        db=db,
        user_email=current_user.email,
        role=current_user.role,
        action="INVESTIGATION_VIEWED",
        target=investigation_id
    )
    return detail

@router.post("/{investigation_id}/notes", response_model=NoteResponse)
def add_investigation_note(
    investigation_id: str,
    payload: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_investigator)
):
    inv = db.query(Investigation).filter(Investigation.investigation_id == investigation_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Investigation not found")

    note = InvestigationNote(
        investigation_id=investigation_id,
        author_email=current_user.email,
        author_role=current_user.role,
        content=payload.content.strip()
    )
    db.add(note)
    db.commit()
    db.refresh(note)

    record_audit(
        db=db,
        user_email=current_user.email,
        role=current_user.role,
        action="NOTE_ADDED",
        target=investigation_id,
        metadata={"note_id": note.id}
    )
    return note

@router.post("/{investigation_id}/verdict")
def set_reviewer_verdict(
    investigation_id: str,
    payload: ReviewerVerdictRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_reviewer)
):
    """
    Reviewer action: APPROVE or FLAG an inference/investigation.
    Requires comment, especially if flagged. Does NOT allow altering raw events.
    """
    inv = db.query(Investigation).filter(Investigation.investigation_id == investigation_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Investigation not found")

    verdict = payload.verdict.lower()
    if verdict not in ("approved", "flagged"):
        raise HTTPException(status_code=400, detail="Verdict must be 'approved' or 'flagged'")

    if verdict == "flagged" and not payload.comment.strip():
        raise HTTPException(status_code=400, detail="A detailed comment is required when flagging an inference.")

    inv.reviewer_verdict = verdict
    inv.reviewer_comment = payload.comment.strip()
    inv.reviewed_by = current_user.email
    inv.reviewed_at = datetime.utcnow()
    inv.status = "approved" if verdict == "approved" else "flagged"

    db.commit()

    record_audit(
        db=db,
        user_email=current_user.email,
        role=current_user.role,
        action=f"INFERENCE_{verdict.upper()}",
        target=investigation_id,
        metadata={"verdict": verdict, "comment": payload.comment}
    )

    return {
        "status": "success",
        "investigation_id": investigation_id,
        "reviewer_verdict": inv.reviewer_verdict,
        "reviewer_comment": inv.reviewer_comment,
        "reviewed_by": inv.reviewed_by,
        "reviewed_at": inv.reviewed_at
    }
