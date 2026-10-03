import pytest
from datetime import datetime, timedelta
from app.engine.inference_engine import reconstruct_session_activity
from app.schemas.event import EventNormalized

def test_inference_reconstruction_structure():
    now = datetime(2026, 10, 3, 10, 0, 0)
    events = [
        EventNormalized(
            event_id="EVT-01",
            timestamp=now,
            event_type="FILE_CREATED",
            path="C:/docs/report.docx",
            file_name="report.docx",
            extension="docx",
            directory="C:/docs",
            file_size=50000,
            source="test",
            process_name="WINWORD.EXE"
        ),
        EventNormalized(
            event_id="EVT-02",
            timestamp=now + timedelta(seconds=6),
            event_type="FILE_CREATED",
            path="C:/docs/report.pdf",
            file_name="report.pdf",
            extension="pdf",
            directory="C:/docs",
            file_size=120000,
            source="test",
            process_name="WINWORD.EXE"
        ),
        EventNormalized(
            event_id="EVT-03",
            timestamp=now + timedelta(seconds=12),
            event_type="PROCESS_STARTED",
            path="C:/Program Files/OUTLOOK.EXE",
            file_name="OUTLOOK.EXE",
            extension="exe",
            directory="C:/Program Files",
            file_size=3000000,
            source="test",
            process_name="OUTLOOK.EXE"
        )
    ]

    res = reconstruct_session_activity(events, scenario_tag="document_workflow")
    
    # 1. Observed facts must match raw events count
    assert len(res.observed_facts) == 3
    for fact in res.observed_facts:
        assert fact.id.startswith("FACT-")
        assert fact.statement != ""

    # 2. Inferences must have supporting evidence IDs
    assert len(res.inferences) >= 1
    for inf in res.inferences:
        assert len(inf.supporting_evidence_ids) >= 2

    # 3. Primary hypothesis must have uncertainty statement
    assert len(res.hypotheses) >= 1
    hyp = res.hypotheses[0]
    assert hyp.confidence > 0.0
    assert hyp.confidence <= 0.98 # Never 100%
    assert "uncertainty" in hyp.uncertainty_statement.lower() or "no direct" in hyp.uncertainty_statement.lower()

    # 4. Missing evidence must be captured (no email transmission packet or converter daemon)
    assert len(res.missing_evidence) >= 1

def test_inference_lifecycle_conflict_penalty():
    # Modified after deletion should flag conflict
    now = datetime(2026, 10, 3, 10, 0, 0)
    events = [
        EventNormalized(
            event_id="EVT-01",
            timestamp=now,
            event_type="FILE_DELETED",
            path="C:/vault/key.txt",
            file_name="key.txt",
            extension="txt",
            directory="C:/vault",
            file_size=0,
            source="test"
        ),
        EventNormalized(
            event_id="EVT-02",
            timestamp=now + timedelta(seconds=5),
            event_type="FILE_MODIFIED",
            path="C:/vault/key.txt",
            file_name="key.txt",
            extension="txt",
            directory="C:/vault",
            file_size=200,
            source="test"
        )
    ]
    res = reconstruct_session_activity(events, scenario_tag="conflicting_evidence")
    assert len(res.conflicting_evidence) >= 1
    assert any("deletion" in c.description.lower() for c in res.conflicting_evidence)
