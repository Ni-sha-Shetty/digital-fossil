import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.session import Session as SessionModel
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.schemas.session import SessionResponse

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.get("", response_model=List[SessionResponse])
def list_sessions(
    anomaly_only: bool = False,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(SessionModel)
    if anomaly_only:
        query = query.filter(SessionModel.is_anomaly == True)

    db_sessions = query.order_by(SessionModel.start_time.desc()).offset(skip).limit(limit).all()
    
    results = []
    for s in db_sessions:
        results.append(SessionResponse(
            id=s.id,
            session_id=s.session_id,
            start_time=s.start_time,
            end_time=s.end_time,
            duration_seconds=s.duration_seconds,
            event_count=s.event_count,
            involved_files=json.loads(s.involved_files or "[]"),
            involved_directories=json.loads(s.involved_directories or "[]"),
            detected_processes=json.loads(s.detected_processes or "[]"),
            anomaly_score=s.anomaly_score,
            is_anomaly=s.is_anomaly,
            confidence_score=s.confidence_score,
            status=s.status,
            scenario_tag=s.scenario_tag,
            created_at=s.created_at
        ))
    return results

@router.get("/{session_id}", response_model=SessionResponse)
def get_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    s = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return SessionResponse(
        id=s.id,
        session_id=s.session_id,
        start_time=s.start_time,
        end_time=s.end_time,
        duration_seconds=s.duration_seconds,
        event_count=s.event_count,
        involved_files=json.loads(s.involved_files or "[]"),
        involved_directories=json.loads(s.involved_directories or "[]"),
        detected_processes=json.loads(s.detected_processes or "[]"),
        anomaly_score=s.anomaly_score,
        is_anomaly=s.is_anomaly,
        confidence_score=s.confidence_score,
        status=s.status,
        scenario_tag=s.scenario_tag,
        created_at=s.created_at
    )
