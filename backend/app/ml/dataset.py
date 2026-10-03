import numpy as np
from typing import Tuple

def generate_synthetic_ml_dataset(
    n_samples: int = 500,
    random_state: int = 42
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Generates synthetic pairwise event features and labels for training and testing.
    Features:
    [time_diff_sec, filename_sim, same_directory, same_extension, seq_compatible, size_ratio]
    y: 1 = Related, 0 = Unrelated
    """
    rng = np.random.RandomState(random_state)
    
    n_positive = n_samples // 2
    n_negative = n_samples - n_positive

    # Positive samples: related files/events (e.g. docx -> pdf, image curation)
    # Short time diff, high filename similarity, same or parent directory, compatible seq
    pos_time = rng.exponential(scale=15.0, size=n_positive) # mostly 0 - 60s
    pos_name_sim = rng.beta(a=8, b=2, size=n_positive) # skewed towards 0.7 - 1.0
    pos_same_dir = rng.choice([1.0, 0.0], size=n_positive, p=[0.75, 0.25])
    pos_same_ext = rng.choice([1.0, 0.0], size=n_positive, p=[0.60, 0.40])
    pos_seq = rng.uniform(low=0.7, high=1.0, size=n_positive)
    pos_size_ratio = rng.uniform(low=0.4, high=1.0, size=n_positive)

    X_pos = np.column_stack([pos_time, pos_name_sim, pos_same_dir, pos_same_ext, pos_seq, pos_size_ratio])
    y_pos = np.ones(n_positive, dtype=int)

    # Negative samples: unrelated background activity
    # Large time diff, low filename similarity, random directory, unrelated seq
    neg_time = rng.uniform(low=60.0, high=600.0, size=n_negative)
    neg_name_sim = rng.beta(a=1.5, b=6, size=n_negative) # skewed towards 0.0 - 0.3
    neg_same_dir = rng.choice([1.0, 0.0], size=n_negative, p=[0.20, 0.80])
    neg_same_ext = rng.choice([1.0, 0.0], size=n_negative, p=[0.25, 0.75])
    neg_seq = rng.uniform(low=0.1, high=0.5, size=n_negative)
    neg_size_ratio = rng.uniform(low=0.01, high=0.5, size=n_negative)

    X_neg = np.column_stack([neg_time, neg_name_sim, neg_same_dir, neg_same_ext, neg_seq, neg_size_ratio])
    y_neg = np.zeros(n_negative, dtype=int)

    X = np.vstack([X_pos, X_neg])
    y = np.concatenate([y_pos, y_neg])

    # Shuffle
    indices = rng.permutation(len(X))
    X = X[indices]
    y = y[indices]

    # Split 80/20 train/test
    split_idx = int(0.8 * len(X))
    return X[:split_idx], X[split_idx:], y[:split_idx], y[split_idx:]

def generate_session_anomaly_training_data(
    n_sessions: int = 150,
    random_state: int = 42
) -> np.ndarray:
    """
    Generates typical/normal session feature vectors for Isolation Forest training.
    Features:
    [event_count, duration_seconds, mod_count, del_count, rename_count, create_count, avg_time_between_events, unique_files, unique_dirs, process_count]
    """
    rng = np.random.RandomState(random_state)
    
    event_count = rng.randint(3, 12, size=n_sessions)
    duration = event_count * rng.uniform(2.0, 8.0, size=n_sessions)
    mod_count = np.maximum(0, event_count - rng.randint(1, 4, size=n_sessions))
    del_count = rng.choice([0, 1], size=n_sessions, p=[0.90, 0.10])
    rename_count = rng.choice([0, 1], size=n_sessions, p=[0.85, 0.15])
    create_count = rng.randint(1, 4, size=n_sessions)
    avg_time = duration / np.maximum(1, event_count - 1)
    unique_files = np.maximum(1, event_count // 2)
    unique_dirs = np.maximum(1, event_count // 4)
    process_count = rng.randint(1, 3, size=n_sessions)

    return np.column_stack([
        event_count, duration, mod_count, del_count, rename_count,
        create_count, avg_time, unique_files, unique_dirs, process_count
    ])
