import json
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import User
from app.models.event import Event
from app.models.session import Session as SessionModel
from app.models.investigation import Investigation
from app.models.config import SystemConfig
from app.models.audit import AuditLog
from app.auth.security import hash_password
from app.auth.dependencies import require_admin
from app.schemas.auth import UserCreate, UserResponse
from app.schemas.config import ThresholdConfigResponse, ThresholdConfigUpdate
from app.collectors.folder_monitor import folder_monitor
from app.database.init_db import reset_demo_database
from app.services.audit_service import record_audit

router = APIRouter(prefix="/admin", tags=["Administration"])

@router.get("/stats")
def get_system_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    total_events = db.query(Event).count()
    total_sessions = db.query(SessionModel).count()
    total_investigations = db.query(Investigation).count()
    anomalous_sessions = db.query(SessionModel).filter(SessionModel.is_anomaly == True).count()
    total_users = db.query(User).count()
    approved_count = db.query(Investigation).filter(Investigation.reviewer_verdict == "approved").count()
    flagged_count = db.query(Investigation).filter(Investigation.reviewer_verdict == "flagged").count()

    collector_status = folder_monitor.get_status()

    return {
        "total_events": total_events,
        "total_sessions": total_sessions,
        "total_investigations": total_investigations,
        "anomalous_sessions": anomalous_sessions,
        "total_users": total_users,
        "approved_investigations": approved_count,
        "flagged_investigations": flagged_count,
        "collector_running": collector_status["is_running"],
        "collector_directory": collector_status["monitored_directory"],
        "database_status": "ONLINE (SQLite WAL)",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/users", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return db.query(User).order_by(User.id.asc()).all()

@router.post("/users", response_model=UserResponse)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    if payload.role not in ("investigator", "reviewer", "admin"):
        raise HTTPException(status_code=400, detail="Invalid role. Must be investigator, reviewer, or admin")

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        role=payload.role,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    record_audit(
        db=db,
        user_email=current_user.email,
        role=current_user.role,
        action="USER_CREATED",
        target=user.email,
        metadata={"role": user.role}
    )
    return user

@router.get("/thresholds", response_model=ThresholdConfigResponse)
def get_thresholds(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    cfg = db.query(SystemConfig).first()
    if not cfg:
        cfg = SystemConfig(session_threshold_sec=120, min_relationship_score=0.35, anomaly_threshold=0.10)
        db.add(cfg)
        db.commit()
        db.refresh(cfg)
    return cfg

@router.put("/thresholds", response_model=ThresholdConfigResponse)
def update_thresholds(
    payload: ThresholdConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    cfg = db.query(SystemConfig).first()
    if not cfg:
        cfg = SystemConfig()
        db.add(cfg)

    cfg.session_threshold_sec = payload.session_threshold_sec
    cfg.min_relationship_score = payload.min_relationship_score
    cfg.anomaly_threshold = payload.anomaly_threshold
    cfg.updated_by = current_user.email
    cfg.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(cfg)

    record_audit(
        db=db,
        user_email=current_user.email,
        role=current_user.role,
        action="THRESHOLDS_UPDATED",
        target="SYSTEM_CONFIG",
        metadata={
            "session_threshold_sec": cfg.session_threshold_sec,
            "min_relationship_score": cfg.min_relationship_score,
            "anomaly_threshold": cfg.anomaly_threshold
        }
    )
    return cfg

@router.get("/audit-logs")
def get_audit_logs(
    action: Optional[str] = None,
    user_email: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    query = db.query(AuditLog)
    if action:
        query = query.filter(AuditLog.action.ilike(f"%{action}%"))
    if user_email:
        query = query.filter(AuditLog.user_email.ilike(f"%{user_email}%"))

    total = query.count()
    logs = query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()

    return {
        "total": total,
        "logs": [
            {
                "id": l.id,
                "timestamp": l.timestamp.isoformat(),
                "user_email": l.user_email,
                "role": l.role,
                "action": l.action,
                "target": l.target,
                "metadata": json.loads(l.metadata_json or "{}")
            }
            for l in logs
        ]
    }

@router.post("/reset-demo")
def reset_demo_data_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    success = reset_demo_database()
    if not success:
        raise HTTPException(status_code=500, detail="Failed to reset demo dataset")

    record_audit(
        db=db,
        user_email=current_user.email,
        role=current_user.role,
        action="DEMO_DATA_RESET",
        target="DATABASE",
        metadata={"scenarios": 6}
    )
    return {
        "status": "success",
        "message": "Demo datasets successfully restored to standard 6 benchmark scenarios."
    }
