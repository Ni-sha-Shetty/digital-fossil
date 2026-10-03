from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.event import Event
from app.models.user import User
from app.auth.dependencies import get_current_user, require_admin
from app.schemas.event import EventResponse, EventListResponse
from app.services.pipeline_service import process_raw_events_pipeline
from app.services.audit_service import record_audit

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("", response_model=EventListResponse)
def list_events(
    filename: Optional[str] = None,
    event_type: Optional[str] = None,
    session_id: Optional[str] = None,
    source: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Event)

    if filename:
        query = query.filter(Event.file_name.ilike(f"%{filename}%"))
    if event_type:
        query = query.filter(Event.event_type == event_type.upper())
    if session_id:
        query = query.filter(Event.session_id == session_id)
    if source:
        query = query.filter(Event.source == source)

    total = query.count()
    events = query.order_by(Event.timestamp.desc()).offset(skip).limit(limit).all()

    return EventListResponse(total=total, events=events)

@router.post("/ingest")
def ingest_events(
    payload: Union[Dict[str, Any], List[Dict[str, Any]]],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    records = payload if isinstance(payload, list) else [payload]
    result = process_raw_events_pipeline(records, db=db, scenario_tag="live_ingest")
    
    record_audit(
        db=db,
        user_email=current_user.email,
        role=current_user.role,
        action="EVENTS_INGESTED",
        target=f"{len(records)} events",
        metadata={"processed": result["events_processed"], "sessions": result["sessions_created"]}
    )

    return {
        "status": "success",
        "events_received": len(records),
        "pipeline_result": result
    }
