import hashlib
import logging
import os
import re
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from app.schemas.event import EventNormalized

logger = logging.getLogger("digital_fossil.normalizer")

# Canonical event types
VALID_EVENT_TYPES = {
    "FILE_CREATED",
    "FILE_MODIFIED",
    "FILE_MOVED",
    "FILE_RENAMED",
    "FILE_DELETED",
    "FILE_ACCESSED",
    "PROCESS_STARTED",
    "PROCESS_STOPPED",
    "DIRECTORY_CREATED",
    "DIRECTORY_DELETED"
}

EVENT_TYPE_MAPPINGS = {
    "created": "FILE_CREATED",
    "create": "FILE_CREATED",
    "new": "FILE_CREATED",
    "file_created": "FILE_CREATED",
    "modified": "FILE_MODIFIED",
    "modify": "FILE_MODIFIED",
    "change": "FILE_MODIFIED",
    "file_modified": "FILE_MODIFIED",
    "moved": "FILE_MOVED",
    "move": "FILE_MOVED",
    "file_moved": "FILE_MOVED",
    "renamed": "FILE_RENAMED",
    "rename": "FILE_RENAMED",
    "file_renamed": "FILE_RENAMED",
    "deleted": "FILE_DELETED",
    "delete": "FILE_DELETED",
    "removed": "FILE_DELETED",
    "file_deleted": "FILE_DELETED",
    "accessed": "FILE_ACCESSED",
    "read": "FILE_ACCESSED",
    "open": "FILE_ACCESSED",
    "process_start": "PROCESS_STARTED",
    "process_started": "PROCESS_STARTED",
    "process_stop": "PROCESS_STOPPED",
    "process_stopped": "PROCESS_STOPPED",
}

def parse_flexible_timestamp(val: Any) -> datetime:
    """Parses ISO strings, unix timestamps (sec or ms), or returns current UTC time on failure."""
    if isinstance(val, datetime):
        return val if val.tzinfo is None else val.astimezone(timezone.utc).replace(tzinfo=None)
    
    if isinstance(val, (int, float)):
        # Milliseconds if > 1e11
        if val > 1e11:
            val = val / 1000.0
        try:
            return datetime.utcfromtimestamp(val)
        except Exception:
            return datetime.utcnow()

    if isinstance(val, str):
        val = val.strip()
        # Try ISO format
        for fmt in (
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
            "%H:%M:%S",
            "%d/%m/%Y %H:%M:%S"
        ):
            try:
                dt = datetime.strptime(val, fmt)
                if fmt == "%H:%M:%S":
                    # Attach current date
                    today = datetime.utcnow().date()
                    dt = datetime.combine(today, dt.time())
                return dt
            except ValueError:
                continue
    
    logger.warning(f"Could not parse timestamp '{val}', falling back to UTC now.")
    return datetime.utcnow()

def normalize_event_type(raw_type: Optional[str]) -> str:
    if not raw_type:
        return "FILE_MODIFIED"
    cleaned = raw_type.strip().lower().replace(" ", "_").replace("-", "_")
    if cleaned in EVENT_TYPE_MAPPINGS:
        return EVENT_TYPE_MAPPINGS[cleaned]
    upper = raw_type.strip().upper()
    if upper in VALID_EVENT_TYPES:
        return upper
    return "FILE_MODIFIED"

def normalize_path_and_filename(raw_path: Optional[str], raw_name: Optional[str]) -> tuple[str, str, str, str]:
    """Returns (canonical_path, file_name, extension, directory)."""
    p = (raw_path or raw_name or "unknown_file").replace("\\", "/")
    
    # Clean redundant slashes
    p = re.sub(r"/+", "/", p)
    
    filename = raw_name or os.path.basename(p) or "unknown_file"
    dirname = os.path.dirname(p) or "/"
    
    # Extract extension
    _, ext = os.path.splitext(filename)
    extension = ext.lower().lstrip(".") if ext else "none"
    
    return p, filename, extension, dirname

def normalize_raw_event(raw: Dict[str, Any]) -> Optional[EventNormalized]:
    """
    Converts any arbitrary raw dictionary or event log entry into a canonical EventNormalized object.
    Never crashes on malformed entries; logs issues and sanitizes data.
    """
    try:
        # Check alternate field names
        raw_type = raw.get("event_type") or raw.get("type") or raw.get("action")
        raw_ts = raw.get("timestamp") or raw.get("time") or raw.get("datetime") or raw.get("date")
        raw_path = raw.get("path") or raw.get("file_path") or raw.get("filepath")
        raw_name = raw.get("file_name") or raw.get("filename") or raw.get("name")
        raw_size = raw.get("file_size") or raw.get("size") or 0
        raw_proc = raw.get("process_name") or raw.get("process") or raw.get("app")
        source = raw.get("source") or "unknown"
        
        # Parse timestamp
        timestamp = parse_flexible_timestamp(raw_ts)
        event_type = normalize_event_type(raw_type)
        path, file_name, extension, directory = normalize_path_and_filename(raw_path, raw_name)
        
        try:
            file_size = max(0, int(raw_size))
        except (ValueError, TypeError):
            file_size = 0
            
        process_name = str(raw_proc).strip() if raw_proc else None
        if process_name and process_name.lower() in ("none", "null", ""):
            process_name = None

        # Build stable deterministic hash ID if not provided
        existing_id = raw.get("id") or raw.get("event_id")
        if existing_id and isinstance(existing_id, str) and len(existing_id) >= 6:
            event_id = existing_id
        else:
            seed = f"{timestamp.isoformat()}_{event_type}_{path}_{file_size}_{process_name or ''}"
            event_id = f"EVT-{hashlib.sha256(seed.encode('utf-8')).hexdigest()[:12].upper()}"

        extra_metadata = raw.get("metadata") or {}
        if not isinstance(extra_metadata, dict):
            extra_metadata = {"raw_metadata": str(extra_metadata)}

        return EventNormalized(
            event_id=event_id,
            timestamp=timestamp,
            event_type=event_type,
            path=path,
            file_name=file_name,
            extension=extension,
            directory=directory,
            file_size=file_size,
            source=source,
            process_name=process_name,
            session_id=raw.get("session_id"),
            extra_metadata=extra_metadata
        )
    except Exception as e:
        logger.error(f"Failed to normalize event record: {raw}. Error: {str(e)}", exc_info=True)
        return None
