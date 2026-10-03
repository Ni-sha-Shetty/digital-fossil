from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from app.database.connection import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    user_email = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    action = Column(String(100), nullable=False, index=True)
    target = Column(String(255), nullable=False)
    metadata_json = Column(Text, default="{}")

    def __repr__(self):
        return f"<AuditLog {self.timestamp} {self.user_email} [{self.action}] on {self.target}>"
