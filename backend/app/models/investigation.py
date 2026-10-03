from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from app.database.connection import Base

class Investigation(Base):
    __tablename__ = "investigations"

    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(String(64), unique=True, index=True, nullable=False)
    session_id = Column(String(64), index=True, nullable=False)
    title = Column(String(255), nullable=False)
    status = Column(String(50), default="open") # open, in_review, approved, flagged, closed
    reviewer_verdict = Column(String(50), nullable=True) # approved, flagged
    reviewer_comment = Column(Text, nullable=True)
    reviewed_by = Column(String(255), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    overall_confidence = Column(Float, default=0.0)
    confidence_label = Column(String(20), default="MEDIUM") # HIGH, MEDIUM, LOW
    observed_facts_count = Column(Integer, default=0)
    inferences_count = Column(Integer, default=0)
    hypotheses_count = Column(Integer, default=0)
    unknowns_count = Column(Integer, default=0)
    summary = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Investigation {self.investigation_id} status={self.status} session={self.session_id}>"

class InvestigationNote(Base):
    __tablename__ = "investigation_notes"

    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(String(64), index=True, nullable=False)
    author_email = Column(String(255), nullable=False)
    author_role = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<InvestigationNote inv={self.investigation_id} by={self.author_email}>"
