from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database.connection import Base

class SystemConfig(Base):
    __tablename__ = "system_configs"

    id = Column(Integer, primary_key=True, index=True)
    session_threshold_sec = Column(Integer, default=120)
    min_relationship_score = Column(Float, default=0.35)
    anomaly_threshold = Column(Float, default=0.10)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(String(255), default="system")

    def __repr__(self):
        return f"<SystemConfig session_th={self.session_threshold_sec}s min_rel={self.min_relationship_score}>"
