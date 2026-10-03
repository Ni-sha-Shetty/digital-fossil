import pytest
import numpy as np
from app.ml.anomaly_detector import anomaly_detector
from app.ml.related_classifier import related_classifier
from app.engine.feature_extractor import SESSION_FEATURE_NAMES, PAIRWISE_FEATURE_NAMES

def test_anomaly_detector_training():
    assert anomaly_detector.is_trained is True

def test_anomaly_detector_normal_evaluation():
    # Construct normal session feature vector
    normal_vec = np.array([5, 30.0, 3, 0, 0, 2, 6.0, 3, 1, 1], dtype=float)
    res = anomaly_detector.evaluate_session(normal_vec)
    assert "is_anomaly" in res
    assert "anomaly_score" in res
    assert 0.0 <= res["anomaly_score"] <= 1.0

def test_anomaly_detector_atypical_evaluation():
    # Highly atypical burst: 50 events, 20 deletions, 20 renames within 5s
    atypical_vec = np.array([50, 5.0, 5, 20, 20, 5, 0.1, 40, 10, 5], dtype=float)
    res = anomaly_detector.evaluate_session(atypical_vec)
    assert res["anomaly_score"] > 0.40
    assert len(res["contributing_factors"]) > 0

def test_related_classifier_metrics():
    assert related_classifier.is_trained is True
    assert len(related_classifier.metrics) == 2
    
    lr_metrics = related_classifier.metrics[0]
    rf_metrics = related_classifier.metrics[1]

    # Verify actual calculated metrics
    assert lr_metrics["accuracy"] > 0.70
    assert rf_metrics["accuracy"] > 0.70
    assert lr_metrics["f1_score"] > 0.70
    assert rf_metrics["f1_score"] > 0.70
    assert len(lr_metrics["confusion_matrix"]) == 2
    assert len(rf_metrics["confusion_matrix"]) == 2

def test_related_classifier_prediction():
    # Strongly related features: 4s time diff, 1.0 name sim, same dir, same ext, compatible seq
    strong_features = np.array([4.0, 1.0, 1.0, 1.0, 0.9, 0.8], dtype=float)
    pred = related_classifier.predict_features(strong_features)
    assert pred["is_related"] is True
    assert pred["probability"] > 0.70
