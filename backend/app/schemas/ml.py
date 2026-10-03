from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class ClassificationMetrics(BaseModel):
    model_name: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    confusion_matrix: List[List[int]]
    feature_importances: Dict[str, float]
    sample_count: int

class MLStatusResponse(BaseModel):
    is_trained: bool
    models: List[ClassificationMetrics]
    anomaly_detector_summary: Dict[str, Any]

class PairwisePredictionRequest(BaseModel):
    time_diff_sec: float
    filename_sim: float
    same_directory: bool
    same_extension: bool
    seq_compatible: bool
    size_ratio: float

class PairwisePredictionResponse(BaseModel):
    is_related: bool
    probability: float
    logistic_regression_prob: float
    random_forest_prob: float
    feature_contributions: Dict[str, float]

class AnomalyExplanation(BaseModel):
    is_anomaly: bool
    score: float
    threshold: float
    message: str
    contributing_factors: Dict[str, float]
