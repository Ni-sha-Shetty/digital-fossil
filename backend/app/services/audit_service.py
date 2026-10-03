import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.audit import AuditLog

logger = logging.getLogger("digital_fossil.audit")

def record_audit(
    db: Session,
    user_email: str,
    role: str,
    action: str,
    target: str,
    metadata: Optional[Dict[str, Any]] = None
) -> AuditLog:
    """Persists an immutable audit log entry for system traceability."""
    try:
        log_entry = AuditLog(
            timestamp=datetime.utcnow(),
            user_email=user_email,
            role=role,
            action=action.upper(),
            target=target,
            metadata_json=json.dumps(metadata or {})
        )
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        logger.info(f"AUDIT: [{role}] {user_email} -> {action} on {target}")
        return log_entry
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to record audit log: {e}")
        raise
