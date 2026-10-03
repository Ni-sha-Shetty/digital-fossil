import logging
import numpy as np
from typing import Dict, Any, List, Optional
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from app.ml.dataset import generate_synthetic_ml_dataset
from app.engine.feature_extractor import PAIRWISE_FEATURE_NAMES, extract_pairwise_features
from app.schemas.event import EventNormalized

logger = logging.getLogger("digital_fossil.related_classifier")

class RelatedEventClassifier:
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.lr_model = LogisticRegression(random_state=random_state, max_iter=500)
        self.rf_model = RandomForestClassifier(n_estimators=100, random_state=random_state, max_depth=6)
        self.metrics: List[Dict[str, Any]] = []
        self.is_trained = False
        self.train_and_evaluate()

    def train_and_evaluate(self):
        """
        Trains and rigorously evaluates Logistic Regression and Random Forest models
        on synthetic labeled pairwise data. Computes REAL evaluation numbers.
        """
        try:
            X_train, X_test, y_train, y_test = generate_synthetic_ml_dataset(
                n_samples=600,
                random_state=self.random_state
            )

            # Fit Logistic Regression
            self.lr_model.fit(X_train, y_train)
            lr_preds = self.lr_model.predict(X_test)
            lr_cm = confusion_matrix(y_test, lr_preds).tolist()
            
            lr_coefs = {}
            if hasattr(self.lr_model, "coef_"):
                for idx, name in enumerate(PAIRWISE_FEATURE_NAMES):
                    lr_coefs[name] = round(float(self.lr_model.coef_[0][idx]), 4)

            lr_metrics = {
                "model_name": "Logistic Regression (Interpretable Linear Baseline)",
                "accuracy": round(float(accuracy_score(y_test, lr_preds)), 4),
                "precision": round(float(precision_score(y_test, lr_preds, zero_division=0)), 4),
                "recall": round(float(recall_score(y_test, lr_preds, zero_division=0)), 4),
                "f1_score": round(float(f1_score(y_test, lr_preds, zero_division=0)), 4),
                "confusion_matrix": lr_cm,
                "feature_importances": lr_coefs,
                "sample_count": len(y_test)
            }

            # Fit Random Forest
            self.rf_model.fit(X_train, y_train)
            rf_preds = self.rf_model.predict(X_test)
            rf_cm = confusion_matrix(y_test, rf_preds).tolist()
            
            rf_importances = {}
            if hasattr(self.rf_model, "feature_importances_"):
                for idx, name in enumerate(PAIRWISE_FEATURE_NAMES):
                    rf_importances[name] = round(float(self.rf_model.feature_importances_[idx]), 4)

            rf_metrics = {
                "model_name": "Random Forest (Non-linear Ensemble)",
                "accuracy": round(float(accuracy_score(y_test, rf_preds)), 4),
                "precision": round(float(precision_score(y_test, rf_preds, zero_division=0)), 4),
                "recall": round(float(recall_score(y_test, rf_preds, zero_division=0)), 4),
                "f1_score": round(float(f1_score(y_test, rf_preds, zero_division=0)), 4),
                "confusion_matrix": rf_cm,
                "feature_importances": rf_importances,
                "sample_count": len(y_test)
            }

            self.metrics = [lr_metrics, rf_metrics]
            self.is_trained = True
            logger.info("Trained and evaluated Logistic Regression & Random Forest classifiers successfully.")
        except Exception as e:
            logger.error(f"Error training related classifiers: {e}", exc_info=True)

    def predict_pair(self, evt1: EventNormalized, evt2: EventNormalized) -> float:
        """Returns ensemble probability that the two events are related."""
        if not self.is_trained:
            return 0.5
        features = extract_pairwise_features(evt1, evt2).reshape(1, -1)
        lr_prob = float(self.lr_model.predict_proba(features)[0][1])
        rf_prob = float(self.rf_model.predict_proba(features)[0][1])
        return round((lr_prob + rf_prob) / 2.0, 4)

    def predict_features(self, feature_vector: np.ndarray) -> Dict[str, Any]:
        """Predicts from raw feature array."""
        if not self.is_trained:
            return {
                "is_related": False,
                "probability": 0.5,
                "logistic_regression_prob": 0.5,
                "random_forest_prob": 0.5,
                "feature_contributions": {}
            }
        X = feature_vector.reshape(1, -1)
        lr_prob = float(self.lr_model.predict_proba(X)[0][1])
        rf_prob = float(self.rf_model.predict_proba(X)[0][1])
        avg_prob = round((lr_prob + rf_prob) / 2.0, 4)

        contributions = {}
        for idx, name in enumerate(PAIRWISE_FEATURE_NAMES):
            contributions[name] = round(float(feature_vector[idx]), 4)

        return {
            "is_related": bool(avg_prob >= 0.50),
            "probability": avg_prob,
            "logistic_regression_prob": round(lr_prob, 4),
            "random_forest_prob": round(rf_prob, 4),
            "feature_contributions": contributions
        }

# Global singleton
related_classifier = RelatedEventClassifier()
