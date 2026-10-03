from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db, SessionLocal
from app.models.user import User
from app.auth.dependencies import get_current_user, require_admin
from app.schemas.collector import CollectorStatusResponse, CollectorStartRequest
from app.collectors.folder_monitor import folder_monitor
from app.services.pipeline_service import process_raw_events_pipeline
from app.services.audit_service import record_audit

router = APIRouter(prefix="/collector", tags=["Collector"])

def on_live_event_captured(record: dict):
    """Callback executed when a filesystem event occurs in the monitored folder."""
    db = SessionLocal()
    try:
        process_raw_events_pipeline([record], db=db, scenario_tag="live_capture")
    except Exception as e:
        pass
    finally:
        db.close()

@router.get("/status", response_model=CollectorStatusResponse)
def get_collector_status(current_user: User = Depends(get_current_user)):
    return CollectorStatusResponse(**folder_monitor.get_status())

@router.post("/start")
def start_collector(
    payload: CollectorStartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    try:
        folder_monitor.start(
            directory_path=payload.directory_path,
            event_callback=on_live_event_captured
        )
        record_audit(
            db=db,
            user_email=current_user.email,
            role=current_user.role,
            action="COLLECTOR_STARTED",
            target=folder_monitor.monitored_directory,
            metadata={"directory": folder_monitor.monitored_directory}
        )
        return {
            "status": "success",
            "message": f"Collector active on: {folder_monitor.monitored_directory}",
            "privacy_notice": "Monitoring is strictly limited to this explicitly selected directory. Only safe metadata captured."
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start collector: {str(e)}")

@router.post("/stop")
def stop_collector(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    folder_monitor.stop()
    record_audit(
        db=db,
        user_email=current_user.email,
        role=current_user.role,
        action="COLLECTOR_STOPPED",
        target=folder_monitor.monitored_directory
    )
    return {
        "status": "success",
        "message": "Collector stopped successfully."
    }
