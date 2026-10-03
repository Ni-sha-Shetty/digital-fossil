import pytest
from datetime import datetime, timedelta
from app.engine.correlator import (
    calculate_filename_similarity,
    calculate_temporal_score,
    compute_pairwise_correlation,
    check_extension_compatibility
)
from app.schemas.event import EventNormalized

def test_filename_similarity():
    assert calculate_filename_similarity("report.docx", "report.pdf") == 1.0 # identical base name
    assert calculate_filename_similarity("report_v1.docx", "report_v2.docx") > 0.80
    assert calculate_filename_similarity("totally_unrelated.jpg", "database_dump.sql") < 0.35

def test_extension_compatibility():
    assert check_extension_compatibility("docx", "pdf") == 0.80
    assert check_extension_compatibility("png", "jpg") == 0.80
    assert check_extension_compatibility("pdf", "pdf") == 1.00
    assert check_extension_compatibility("exe", "mp3") == 0.20

def test_temporal_exponential_decay():
    assert calculate_temporal_score(0.0) == 1.0
    # Half life is 60s -> should be ~0.50 at 60s
    assert 0.48 <= calculate_temporal_score(60.0) <= 0.52
    # At 3600s -> ~0.0
    assert calculate_temporal_score(3600.0) < 0.01

def test_pairwise_correlation_high():
    now = datetime(2026, 10, 3, 10, 0, 0)
    e1 = EventNormalized(
        event_id="EVT-01",
        timestamp=now,
        event_type="FILE_CREATED",
        path="/work/Q3_Report.docx",
        file_name="Q3_Report.docx",
        extension="docx",
        directory="/work",
        file_size=50000,
        source="test",
        process_name="word.exe"
    )
    e2 = EventNormalized(
        event_id="EVT-02",
        timestamp=now + timedelta(seconds=6),
        event_type="FILE_CREATED",
        path="/work/Q3_Report.pdf",
        file_name="Q3_Report.pdf",
        extension="pdf",
        directory="/work",
        file_size=120000,
        source="test",
        process_name="word.exe"
    )

    score, breakdown = compute_pairwise_correlation(e1, e2)
    # 6s gap, same base name, compatible ext, same dir, same process -> score should be high (> 0.75)
    assert score >= 0.75
    assert "factors" in breakdown
    assert breakdown["factors"]["filename_similarity"]["score"] == 1.0
    assert breakdown["factors"]["temporal_proximity"]["score"] > 0.90
