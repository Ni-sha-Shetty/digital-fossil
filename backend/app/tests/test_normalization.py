import pytest
from datetime import datetime
from app.engine.normalizer import (
    normalize_raw_event,
    parse_flexible_timestamp,
    normalize_path_and_filename,
    normalize_event_type
)

def test_flexible_timestamp_iso():
    ts_str = "2026-10-03T10:02:11"
    dt = parse_flexible_timestamp(ts_str)
    assert isinstance(dt, datetime)
    assert dt.hour == 10 and dt.minute == 2 and dt.second == 11

def test_flexible_timestamp_epoch():
    epoch = 1700000000 # Unix seconds
    dt = parse_flexible_timestamp(epoch)
    assert isinstance(dt, datetime)
    assert dt.year >= 2023

def test_flexible_timestamp_malformed_fallback():
    # Should not crash; falls back gracefully to current UTC time
    dt = parse_flexible_timestamp("invalid_date_string_xyz")
    assert isinstance(dt, datetime)

def test_normalize_event_type_aliases():
    assert normalize_event_type("created") == "FILE_CREATED"
    assert normalize_event_type("modified") == "FILE_MODIFIED"
    assert normalize_event_type("file_moved") == "FILE_MOVED"
    assert normalize_event_type("delete") == "FILE_DELETED"
    assert normalize_event_type("process_start") == "PROCESS_STARTED"
    assert normalize_event_type("UNKNOWN_CUSTOM") == "FILE_MODIFIED" # safe default

def test_normalize_path_and_filename():
    p, name, ext, dirname = normalize_path_and_filename("C:\\Users\\Analyst\\report.docx", None)
    assert name == "report.docx"
    assert ext == "docx"
    assert "Analyst" in dirname

def test_normalize_raw_event_success():
    raw = {
        "timestamp": "2026-10-03T12:00:00",
        "action": "create",
        "path": "/data/test/document.pdf",
        "size": 45000,
        "process": "word.exe"
    }
    norm = normalize_raw_event(raw)
    assert norm is not None
    assert norm.event_type == "FILE_CREATED"
    assert norm.file_name == "document.pdf"
    assert norm.extension == "pdf"
    assert norm.file_size == 45000
    assert norm.process_name == "word.exe"
    assert norm.event_id.startswith("EVT-")

def test_normalize_raw_event_empty_resilience():
    # Pipeline should never crash on completely blank input
    norm = normalize_raw_event({})
    assert norm is not None
    assert norm.file_name == "unknown_file"
    assert norm.event_type == "FILE_MODIFIED"
