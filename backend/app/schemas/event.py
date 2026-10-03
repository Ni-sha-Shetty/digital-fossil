from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, ConfigDict

class EventRaw(BaseModel):
    id: Optional[str] = None
    timestamp: Optional[Any] = None
    event_type: Optional[str] = None
    type: Optional[str] = None
    path: Optional[str] = None
    file_path: Optional[str] = None
    file_name: Optional[str] = None
    filename: Optional[str] = None
    extension: Optional[str] = None
    ext: Optional[str] = None
    directory: Optional[str] = None
    folder: Optional[str] = None
    file_size: Optional[int] = 0
    size: Optional[int] = 0
    source: Optional[str] = "unknown"
    process_name: Optional[str] = None
    process: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class EventNormalized(BaseModel):
    event_id: str
    timestamp: datetime
    event_type: str
    path: str
    file_name: str
    extension: str
    directory: str
    file_size: int
    source: str
    process_name: Optional[str] = None
    session_id: Optional[str] = None
    extra_metadata: Dict[str, Any] = Field(default_factory=dict)

class EventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: str
    timestamp: datetime
    event_type: str
    path: str
    file_name: str
    extension: str
    directory: str
    file_size: int
    source: str
    process_name: Optional[str] = None
    session_id: Optional[str] = None
    created_at: datetime

class EventListResponse(BaseModel):
    total: int
    events: List[EventResponse]
