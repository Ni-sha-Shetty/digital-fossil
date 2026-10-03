from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ThresholdConfigResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    session_threshold_sec: int
    min_relationship_score: float
    anomaly_threshold: float
    updated_at: datetime
    updated_by: str

class ThresholdConfigUpdate(BaseModel):
    session_threshold_sec: int
    min_relationship_score: float
    anomaly_threshold: float
