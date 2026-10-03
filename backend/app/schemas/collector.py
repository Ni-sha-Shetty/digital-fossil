from typing import Optional
from pydantic import BaseModel

class CollectorStatusResponse(BaseModel):
    is_running: bool
    monitored_directory: str
    events_captured: int
    privacy_notice: str
    message: str

class CollectorStartRequest(BaseModel):
    directory_path: Optional[str] = None
