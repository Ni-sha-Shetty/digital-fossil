import logging
import numpy as np
from sklearn.ensemble import IsolationForest
from app.ml.dataset import generate_session_anomaly_training_data
from app.engine.feature_extractor import SESSION_FEATURE_NAMES

logger = logging.getLogger("digital_fossil.anomaly_detector")

class SessionAnomalyDetector:
    def __init__(self, contamination: float = 0.10, random_state: int = 42):
        self.contamination = contamination
        self.random_state = random_state
        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
            n_estimators=100
        )
        self.is_trained = False
        self.feature_means = np.zeros(len(SESSION_FEATURE_NAMES))
        self._train_default_baseline()

    def _train_default_baseline(self):
        try:
            X_train = generate_session_anomaly_training_data(n_sessions=200, random_state=self.random_state)
            self.model.fit(X_train)
            self.feature_means = np.mean(X_train, axis=0)
            self.is_trained = True
            logger.info("Isolation Forest anomaly detector initialized with synthetic baseline.")
        except Exception as e:
            logger.error(f"Failed to fit Isolation Forest: {e}")

    def evaluate_session(self, feature_vector: np.ndarray) -> dict:
        """
        Evaluates a session's feature vector.
        Returns:
        - is_anomaly (bool)
        - anomaly_score (float, 0.0 to 1.0, higher means more anomalous)
        - explanation (str)
        - contributing_factors (dict)
        """
        if not self.is_trained or feature_vector is None or len(feature_vector) == 0:
            return {
                "is_anomaly": False,
                "anomaly_score": 0.0,
                "message": "Anomaly detector not yet initialized.",
                "contributing_factors": {}
            }

        X = feature_vector.reshape(1, -1)
        pred = self.model.predict(X)[0] # -1 = anomaly, 1 = normal
        decision_val = self.model.decision_function(X)[0] # negative is anomalous

        # Map decision function to 0.0 (very normal) .. 1.0 (highly atypical)
        # Decision function is typically in range [-0.3, +0.2]
        score = 1.0 / (1.0 + np.exp(decision_val * 6.0))
        score = round(float(np.clip(score, 0.0, 1.0)), 4)
        is_anomaly = bool(pred == -1 or score > 0.60)

        # Factor contributions: features diverging most from mean
        contributions = {}
        for idx, name in enumerate(SESSION_FEATURE_NAMES):
            diff = float(feature_vector[idx] - self.feature_means[idx])
            contributions[name] = round(diff, 2)

        # Filter to top 3 diverging factors
        sorted_divergence = sorted(contributions.items(), key=lambda kv: abs(kv[1]), reverse=True)[:3]
        top_factors = dict(sorted_divergence)

        message = (
            "Activity shows statistically significant deviation from learned baseline patterns. "
            "Note: Anomaly does not mean malicious; it indicates atypical frequency, volume, or lifecycle events."
            if is_anomaly else
            "Activity parameters conform with baseline operational expectations."
        )

        return {
            "is_anomaly": is_anomaly,
            "anomaly_score": score,
            "message": message,
            "contributing_factors": top_factors
        }

# Global singleton
anomaly_detector = SessionAnomalyDetector()
