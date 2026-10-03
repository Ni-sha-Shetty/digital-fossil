import pytest
from datetime import datetime, timedelta
from app.engine.sessionizer import sessionize_events
from app.schemas.event import EventNormalized

def create_dummy_event(offset_sec: int, fname: str = "doc.txt") -> EventNormalized:
    base = datetime(2026, 10, 3, 10, 0, 0)
    ts = base + timedelta(seconds=offset_sec)
    return EventNormalized(
        event_id=f"EVT-{offset_sec:04d}",
        timestamp=ts,
        event_type="FILE_MODIFIED",
        path=f"/path/{fname}",
        file_name=fname,
        extension="txt",
        directory="/path",
        file_size=1024,
        source="test"
    )

def test_sessionize_empty():
    assert sessionize_events([]) == []

def test_sessionize_single_cluster():
    # 4 events spaced 10 seconds apart -> 1 session
    events = [create_dummy_event(i * 10) for i in range(4)]
    sessions = sessionize_events(events, threshold_seconds=120)
    assert len(sessions) == 1
    assert sessions[0].event_count == 4
    assert sessions[0].duration_seconds == 30.0

def test_sessionize_multiple_clusters():
    # 2 events close together, then 300s gap, then 2 events
    events = [
        create_dummy_event(0),
        create_dummy_event(20),
        create_dummy_event(320), # gap = 300s > 120s
        create_dummy_event(340)
    ]
    sessions = sessionize_events(events, threshold_seconds=120)
    assert len(sessions) == 2
    assert sessions[0].event_count == 2
    assert sessions[1].event_count == 2
    assert sessions[0].session_id != sessions[1].session_id
