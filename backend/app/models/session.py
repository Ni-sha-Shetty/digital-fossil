from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text
from app.database.connection import Base

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), unique=True, index=True, nullable=False)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False)
    duration_seconds = Column(Float, default=0.0)
    event_count = Column(Integer, default=0)
    involved_files = Column(Text, default="[]") # JSON list of file names
    involved_directories = Column(Text, default="[]") # JSON list
    detected_processes = Column(Text, default="[]") # JSON list
    anomaly_score = Column(Float, default=0.0)
    is_anomaly = Column(Boolean, default=False)
    confidence_score = Column(Float, default=0.0)
    status = Column(String(50), default="analyzed")
    scenario_tag = Column(String(100), default="general") # document_workflow, etc.
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Session {self.session_id} events={self.event_count} anomaly={self.is_anomaly}>"
