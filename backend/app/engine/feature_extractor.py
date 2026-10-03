from typing import List, Dict, Any
import numpy as np
from app.schemas.event import EventNormalized
from app.engine.correlator import (
    calculate_filename_similarity,
    calculate_sequence_score,
    calculate_directory_similarity
)

SESSION_FEATURE_NAMES = [
    "event_count",
    "duration_seconds",
    "mod_count",
    "del_count",
    "rename_count",
    "create_count",
    "avg_time_between_events",
    "unique_files_count",
    "unique_dirs_count",
    "process_count"
]

PAIRWISE_FEATURE_NAMES = [
    "time_diff_sec",
    "filename_sim",
    "same_directory",
    "same_extension",
    "seq_compatible",
    "size_ratio"
]

def extract_session_features(events: List[EventNormalized]) -> np.ndarray:
    """
    Extracts an engineered feature vector for session-level anomaly detection.
    """
    if not events:
        return np.zeros(len(SESSION_FEATURE_NAMES), dtype=float)

    sorted_events = sorted(events, key=lambda e: e.timestamp)
    count = len(sorted_events)
    
    start_ts = sorted_events[0].timestamp
    end_ts = sorted_events[-1].timestamp
    duration = max(1.0, (end_ts - start_ts).total_seconds())

    mod_count = sum(1 for e in sorted_events if e.event_type == "FILE_MODIFIED")
    del_count = sum(1 for e in sorted_events if e.event_type == "FILE_DELETED")
    rename_count = sum(1 for e in sorted_events if e.event_type in ("FILE_RENAMED", "FILE_MOVED"))
    create_count = sum(1 for e in sorted_events if e.event_type == "FILE_CREATED")

    if count > 1:
        time_deltas = [
            (sorted_events[i].timestamp - sorted_events[i - 1].timestamp).total_seconds()
            for i in range(1, count)
        ]
        avg_time = float(np.mean(time_deltas))
    else:
        avg_time = 0.0

    unique_files = len({e.file_name for e in sorted_events if e.file_name})
    unique_dirs = len({e.directory for e in sorted_events if e.directory})
    unique_procs = len({e.process_name for e in sorted_events if e.process_name})

    vector = [
        float(count),
        float(duration),
        float(mod_count),
        float(del_count),
        float(rename_count),
        float(create_count),
        float(avg_time),
        float(unique_files),
        float(unique_dirs),
        float(unique_procs)
    ]
    return np.array(vector, dtype=float)

def extract_pairwise_features(evt1: EventNormalized, evt2: EventNormalized) -> np.ndarray:
    """
    Extracts a feature vector for supervised binary classification of event correlation.
    """
    time_diff = abs((evt2.timestamp - evt1.timestamp).total_seconds())
    sim_name = calculate_filename_similarity(evt1.file_name, evt2.file_name)
    same_dir = 1.0 if evt1.directory.lower() == evt2.directory.lower() else 0.0
    same_ext = 1.0 if evt1.extension.lower() == evt2.extension.lower() else 0.0
    
    if evt1.timestamp <= evt2.timestamp:
        seq = calculate_sequence_score(evt1.event_type, evt2.event_type)
    else:
        seq = calculate_sequence_score(evt2.event_type, evt1.event_type)

    max_size = max(evt1.file_size, evt2.file_size, 1)
    min_size = max(0, min(evt1.file_size, evt2.file_size))
    size_ratio = min_size / max_size

    vector = [
        float(time_diff),
        float(sim_name),
        float(same_dir),
        float(same_ext),
        float(seq),
        float(size_ratio)
    ]
    return np.array(vector, dtype=float)
