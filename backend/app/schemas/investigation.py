from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict

class ObservedFact(BaseModel):
    id: str
    event_id: str
    timestamp: datetime
    statement: str
    event_type: str
    file_name: str
    path: str
    process_name: Optional[str] = None
    file_size: int

class InferenceItem(BaseModel):
    id: str
    statement: str
    primary_file: str
    related_file: Optional[str] = None
    supporting_evidence_ids: List[str]
    correlation_score: float
    reasoning_factors: Dict[str, Any]
    ml_probability: Optional[float] = None
    status: str = "proposed"

class HypothesisItem(BaseModel):
    id: str
    hypothesis_text: str
    supporting_evidence_ids: List[str]
    contradicting_evidence_ids: List[str]
    confidence: float
    confidence_label: str
    reasoning_summary: str
    uncertainty_statement: str

class MissingEvidenceItem(BaseModel):
    id: str
    description: str
    significance: str
    expected_event_type: Optional[str] = None

class ConflictingEvidenceItem(BaseModel):
    id: str
    description: str
    conflict_type: str
    impact_on_confidence: str

class GraphNode(BaseModel):
    id: str
    label: str
    type: str
    timestamp: Optional[str] = None
    size: Optional[int] = None
    is_anomaly: Optional[bool] = False
    metadata: Dict[str, Any] = {}

class GraphEdge(BaseModel):
    source: str
    target: str
    label: str
    relationship_type: str
    score: float
    evidence_ids: List[str] = []

class GraphData(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]

class NoteCreate(BaseModel):
    content: str

class NoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    investigation_id: str
    author_email: str
    author_role: str
    content: str
    created_at: datetime

class ReviewerVerdictRequest(BaseModel):
    verdict: str
    comment: str

class InvestigationSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    investigation_id: str
    session_id: str
    title: str
    status: str
    reviewer_verdict: Optional[str] = None
    reviewer_comment: Optional[str] = None
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    overall_confidence: float
    confidence_label: str
    observed_facts_count: int
    inferences_count: int
    hypotheses_count: int
    unknowns_count: int
    summary: str
    created_at: datetime
    updated_at: datetime

class InvestigationDetail(InvestigationSummary):
    session_start: datetime
    session_end: datetime
    session_duration: float
    is_anomaly: bool
    anomaly_score: float
    observed_facts: List[ObservedFact]
    inferences: List[InferenceItem]
    hypotheses: List[HypothesisItem]
    missing_evidence: List[MissingEvidenceItem]
    conflicting_evidence: List[ConflictingEvidenceItem]
    ai_explanation: str
    graph: GraphData
    notes: List[NoteResponse]
