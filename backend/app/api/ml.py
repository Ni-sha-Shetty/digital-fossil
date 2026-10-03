import numpy as np
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import User
from app.auth.dependencies import get_current_user, require_admin
from app.schemas.ml import (
    MLStatusResponse,
    ClassificationMetrics,
    PairwisePredictionRequest,
    PairwisePredictionResponse
)
from app.ml.related_classifier import related_classifier
from app.ml.anomaly_detector import anomaly_detector
from app.services.audit_service import record_audit

router = APIRouter(prefix="/ml", tags=["Machine Learning"])

@router.get("/status", response_model=MLStatusResponse)
def get_ml_status(current_user: User = Depends(get_current_user)):
    models_metrics = [
        ClassificationMetrics(**m) for m in related_classifier.metrics
    ]
    
    anomaly_summary = {
        "model": "Isolation Forest (scikit-learn)",
        "contamination": anomaly_detector.contamination,
        "n_estimators": 100,
        "is_trained": anomaly_detector.is_trained,
        "purpose": "Identify activity sessions that deviate from baseline frequency or lifecycle composition.",
        "note": "Anomaly does not equal malicious; it represents statistical novelty or burst velocity."
    }

    return MLStatusResponse(
        is_trained=related_classifier.is_trained and anomaly_detector.is_trained,
        models=models_metrics,
        anomaly_detector_summary=anomaly_summary
    )

@router.post("/predict-pair", response_model=PairwisePredictionResponse)
def predict_pairwise_relationship(
    payload: PairwisePredictionRequest,
    current_user: User = Depends(get_current_user)
):
    feature_vector = np.array([
        payload.time_diff_sec,
        payload.filename_sim,
        1.0 if payload.same_directory else 0.0,
        1.0 if payload.same_extension else 0.0,
        1.0 if payload.seq_compatible else 0.2,
        payload.size_ratio
    ], dtype=float)

    pred = related_classifier.predict_features(feature_vector)
    return PairwisePredictionResponse(**pred)

@router.post("/retrain")
def retrain_models(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    related_classifier.train_and_evaluate()
    anomaly_detector._train_default_baseline()
    
    record_audit(
        db=db,
        user_email=current_user.email,
        role=current_user.role,
        action="ML_MODELS_RETRAINED",
        target="IsolationForest & Classifiers"
    )

    return {
        "status": "success",
        "message": "Models retrained and evaluated successfully with updated synthetic feature distributions.",
        "metrics": related_classifier.metrics
    }
