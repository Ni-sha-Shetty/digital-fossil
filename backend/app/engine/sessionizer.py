import json
import logging
from datetime import datetime
from typing import List, Dict, Any
from app.schemas.event import EventNormalized

logger = logging.getLogger("digital_fossil.sessionizer")

class SessionizedGroup:
    def __init__(self, session_id: str, events: List[EventNormalized], scenario_tag: str = "general"):
        self.session_id = session_id
        self.events = events
        self.scenario_tag = scenario_tag
        
        sorted_events = sorted(events, key=lambda e: e.timestamp)
        self.start_time = sorted_events[0].timestamp if sorted_events else datetime.utcnow()
        self.end_time = sorted_events[-1].timestamp if sorted_events else datetime.utcnow()
        self.duration_seconds = max(0.0, (self.end_time - self.start_time).total_seconds())
        self.event_count = len(events)
        
        self.involved_files = sorted(list({e.file_name for e in events if e.file_name and e.file_name != "unknown_file"}))
        self.involved_directories = sorted(list({e.directory for e in events if e.directory}))
        self.detected_processes = sorted(list({e.process_name for e in events if e.process_name}))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_seconds": self.duration_seconds,
            "event_count": self.event_count,
            "involved_files": json.dumps(self.involved_files),
            "involved_directories": json.dumps(self.involved_directories),
            "detected_processes": json.dumps(self.detected_processes),
            "scenario_tag": self.scenario_tag
        }

def sessionize_events(
    events: List[EventNormalized],
    threshold_seconds: int = 120
) -> List[SessionizedGroup]:
    """
    Groups events chronologically into sessions. If the time delta between
    subsequent events exceeds threshold_seconds, a new session is created.
    """
    if not events:
        return []

    # Sort events strictly by timestamp
    sorted_events = sorted(events, key=lambda e: e.timestamp)
    
    sessions: List[SessionizedGroup] = []
    current_cluster: List[EventNormalized] = []
    session_index = 1

    for event in sorted_events:
        if not current_cluster:
            current_cluster.append(event)
            continue
        
        last_event = current_cluster[-1]
        time_gap = (event.timestamp - last_event.timestamp).total_seconds()
        
        if time_gap <= threshold_seconds:
            current_cluster.append(event)
        else:
            # Finalize current session
            tag = _infer_scenario_tag(current_cluster)
            ses_id = f"SES-{current_cluster[0].timestamp.strftime('%Y%m%d%H%M')}-{session_index:03d}"
            # Assign session_id to events
            for e in current_cluster:
                e.session_id = ses_id
            sessions.append(SessionizedGroup(ses_id, current_cluster, scenario_tag=tag))
            session_index += 1
            current_cluster = [event]

    if current_cluster:
        tag = _infer_scenario_tag(current_cluster)
        ses_id = f"SES-{current_cluster[0].timestamp.strftime('%Y%m%d%H%M')}-{session_index:03d}"
        for e in current_cluster:
            e.session_id = ses_id
        sessions.append(SessionizedGroup(ses_id, current_cluster, scenario_tag=tag))

    logger.info(f"Sessionized {len(events)} events into {len(sessions)} sessions (threshold={threshold_seconds}s)")
    return sessions

def _infer_scenario_tag(events: List[EventNormalized]) -> str:
    # Check if metadata already has a scenario
    for e in events:
        if "scenario" in e.extra_metadata:
            return str(e.extra_metadata["scenario"])
    return "general_activity"
