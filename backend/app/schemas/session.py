from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: str
    start_time: datetime
    end_time: datetime
    duration_seconds: float
    event_count: int
    involved_files: List[str]
    involved_directories: List[str]
    detected_processes: List[str]
    anomaly_score: float
    is_anomaly: bool
    confidence_score: float
    status: str
    scenario_tag: str
    created_at: datetime

class SessionDetail(SessionResponse):
    pass
