from datetime import datetime
from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Text, Float
from app.database.connection import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String(64), unique=True, index=True, nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    event_type = Column(String(50), nullable=False, index=True) # FILE_CREATED, FILE_MODIFIED, etc.
    path = Column(String(1024), nullable=False)
    file_name = Column(String(255), nullable=False, index=True)
    extension = Column(String(50), nullable=False, index=True)
    directory = Column(String(1024), nullable=False)
    file_size = Column(BigInteger, default=0)
    source = Column(String(50), default="synthetic_demo") # synthetic_demo, watchdog_live, manual_import
    process_name = Column(String(100), nullable=True)
    session_id = Column(String(64), nullable=True, index=True)
    extra_metadata = Column(Text, default="{}") # JSON metadata
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Event {self.event_type} on {self.file_name} @ {self.timestamp}>"
