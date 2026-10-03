import math
import difflib
import os
from typing import Dict, Any, Tuple
from app.schemas.event import EventNormalized

# Explicit scoring weights totaling 1.0
WEIGHT_TIME = 0.30
WEIGHT_NAME = 0.25
WEIGHT_SEQUENCE = 0.20
WEIGHT_DIRECTORY = 0.15
WEIGHT_EXTENSION = 0.10

COMPATIBLE_EXTENSIONS = {
    ("docx", "pdf"), ("doc", "pdf"), ("pptx", "pdf"),
    ("odt", "pdf"), ("rtf", "pdf"), ("txt", "pdf"),
    ("png", "jpg"), ("jpeg", "png"), ("raw", "jpg"), ("svg", "png"),
    ("zip", "png"), ("zip", "jpg"), ("zip", "docx"), ("tar", "gz"),
    ("py", "pyc"), ("c", "o"), ("cpp", "exe"), ("ts", "js")
}

SEQUENCE_TRANSITIONS = {
    ("FILE_CREATED", "FILE_MODIFIED"): 0.90,
    ("FILE_MODIFIED", "FILE_MODIFIED"): 0.80,
    ("FILE_MODIFIED", "FILE_MOVED"): 0.85,
    ("FILE_MODIFIED", "FILE_RENAMED"): 0.85,
    ("FILE_CREATED", "FILE_MOVED"): 0.80,
    ("FILE_MOVED", "FILE_DELETED"): 0.80,
    ("FILE_MODIFIED", "FILE_DELETED"): 0.75,
    ("PROCESS_STARTED", "FILE_CREATED"): 0.85,
    ("PROCESS_STARTED", "FILE_MODIFIED"): 0.80,
    ("PROCESS_STARTED", "FILE_ACCESSED"): 0.85,
    ("FILE_MOVED", "PROCESS_STARTED"): 0.70,
    ("FILE_CREATED", "PROCESS_STARTED"): 0.65
}

def calculate_filename_similarity(name1: str, name2: str) -> float:
    """Calculates Levenshtein-like ratio between filename base names ignoring extensions."""
    if not name1 or not name2:
        return 0.0
    base1, _ = os.path.splitext(name1.lower())
    base2, _ = os.path.splitext(name2.lower())
    
    if base1 == base2:
        return 1.0
    
    # Strip common suffixes like _copy, -converted, (1), etc.
    base1_clean = base1.replace("_copy", "").replace("-copy", "").replace(" (1)", "").replace("-converted", "")
    base2_clean = base2.replace("_copy", "").replace("-copy", "").replace(" (1)", "").replace("-converted", "")
    
    if base1_clean == base2_clean and len(base1_clean) > 2:
        return 0.95
        
    matcher = difflib.SequenceMatcher(None, base1, base2)
    return round(matcher.ratio(), 4)

def check_extension_compatibility(ext1: str, ext2: str) -> float:
    e1, e2 = ext1.lower().lstrip("."), ext2.lower().lstrip(".")
    if e1 == e2:
        return 1.0
    if (e1, e2) in COMPATIBLE_EXTENSIONS or (e2, e1) in COMPATIBLE_EXTENSIONS:
        return 0.80
    return 0.20

def calculate_directory_similarity(dir1: str, dir2: str) -> float:
    d1 = dir1.replace("\\", "/").rstrip("/")
    d2 = dir2.replace("\\", "/").rstrip("/")
    if d1 == d2:
        return 1.0
    if d1.startswith(d2) or d2.startswith(d1):
        return 0.60
    return 0.15

def calculate_sequence_score(event1_type: str, event2_type: str) -> float:
    pair = (event1_type, event2_type)
    if pair in SEQUENCE_TRANSITIONS:
        return SEQUENCE_TRANSITIONS[pair]
    # Reverse order if time allows
    rev_pair = (event2_type, event1_type)
    if rev_pair in SEQUENCE_TRANSITIONS:
        return max(0.20, SEQUENCE_TRANSITIONS[rev_pair] - 0.20)
    return 0.30

def calculate_temporal_score(time_diff_seconds: float, half_life_seconds: float = 60.0) -> float:
    """
    Transparent exponential decay scoring:
    Score is 1.0 at 0 seconds, ~0.5 at 60s, ~0.25 at 120s, approaching 0.0 for large gaps.
    """
    dt = abs(time_diff_seconds)
    # Decay constant lambda = ln(2) / half_life
    decay_lambda = math.log(2) / half_life_seconds
    score = math.exp(-decay_lambda * dt)
    return round(max(0.0, min(1.0, score)), 4)

def compute_pairwise_correlation(
    evt1: EventNormalized,
    evt2: EventNormalized
) -> Tuple[float, Dict[str, Any]]:
    """
    Computes a composite relationship score between two events with complete factor breakdown.
    Formula:
    Score = (w_time * S_time) + (w_name * S_name) + (w_seq * S_seq) + (w_dir * S_dir) + (w_ext * S_ext)
    """
    time_diff_sec = abs((evt2.timestamp - evt1.timestamp).total_seconds())
    time_score = calculate_temporal_score(time_diff_sec)
    name_score = calculate_filename_similarity(evt1.file_name, evt2.file_name)
    ext_score = check_extension_compatibility(evt1.extension, evt2.extension)
    dir_score = calculate_directory_similarity(evt1.directory, evt2.directory)
    
    # Chronological ordering check
    if evt1.timestamp <= evt2.timestamp:
        seq_score = calculate_sequence_score(evt1.event_type, evt2.event_type)
    else:
        seq_score = calculate_sequence_score(evt2.event_type, evt1.event_type)

    # Process bonus: if the same process touched both or process launched right before file action
    process_bonus = 0.0
    if evt1.process_name and evt2.process_name and evt1.process_name.lower() == evt2.process_name.lower():
        process_bonus = 0.05

    composite_score = (
        (WEIGHT_TIME * time_score) +
        (WEIGHT_NAME * name_score) +
        (WEIGHT_SEQUENCE * seq_score) +
        (WEIGHT_DIRECTORY * dir_score) +
        (WEIGHT_EXTENSION * ext_score) +
        process_bonus
    )
    composite_score = round(max(0.0, min(1.0, composite_score)), 4)

    breakdown = {
        "composite_score": composite_score,
        "time_diff_seconds": round(time_diff_sec, 2),
        "factors": {
            "temporal_proximity": {
                "score": time_score,
                "weight": WEIGHT_TIME,
                "weighted_contribution": round(time_score * WEIGHT_TIME, 4),
                "details": f"Time gap of {time_diff_sec:.1f}s evaluated with exponential decay (half-life 60s)"
            },
            "filename_similarity": {
                "score": name_score,
                "weight": WEIGHT_NAME,
                "weighted_contribution": round(name_score * WEIGHT_NAME, 4),
                "details": f"Comparing '{evt1.file_name}' and '{evt2.file_name}'"
            },
            "sequence_compatibility": {
                "score": seq_score,
                "weight": WEIGHT_SEQUENCE,
                "weighted_contribution": round(seq_score * WEIGHT_SEQUENCE, 4),
                "details": f"Order: {evt1.event_type} -> {evt2.event_type}"
            },
            "directory_locality": {
                "score": dir_score,
                "weight": WEIGHT_DIRECTORY,
                "weighted_contribution": round(dir_score * WEIGHT_DIRECTORY, 4),
                "details": f"Paths: '{evt1.directory}' vs '{evt2.directory}'"
            },
            "extension_compatibility": {
                "score": ext_score,
                "weight": WEIGHT_EXTENSION,
                "weighted_contribution": round(ext_score * WEIGHT_EXTENSION, 4),
                "details": f"Extensions: '{evt1.extension}' vs '{evt2.extension}'"
            }
        },
        "process_bonus": process_bonus
    }

    return composite_score, breakdown
