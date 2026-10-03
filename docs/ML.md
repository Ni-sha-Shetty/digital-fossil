# DIGITAL FOSSIL: Machine Learning Methodology & Explainability

## 1. Machine Learning Philosophy in Forensics

Machine learning in digital forensics must prioritize **explainability and verifiable calibration** over opaque "black-box" predictions. The Digital Fossil ML subsystem serves two dedicated functions:

1. **Unsupervised Session Anomaly Detection** (detecting behavioral velocity and volume deviations).
2. **Supervised Pairwise Event-Relation Classification** (estimating the likelihood that two events share an underlying operator workflow).

---

## 2. Component 1: Unsupervised Session Anomaly Detection

### 2.1 Model Selection: Isolation Forest
We employ `sklearn.ensemble.IsolationForest` configured with:
- `n_estimators`: 100
- `contamination`: 0.10 (configurable dynamically by the System Administrator)
- `random_state`: 42 (ensures reproducibility)

### 2.2 Feature Vector Architecture
For each session, `feature_extractor.extract_session_features` constructs a 10-dimensional numerical representation:
1. `event_count`: Total events clustered in the session.
2. `duration_seconds`: Total elapsed time from start to completion.
3. `mod_count`: Frequency of `FILE_MODIFIED` events.
4. `del_count`: Frequency of `FILE_DELETED` events.
5. `rename_count`: Frequency of `FILE_MOVED` or `FILE_RENAMED` events.
6. `create_count`: Frequency of initial file creations.
7. `avg_time_between_events`: Mean delta time between consecutive operations.
8. `unique_files_count`: Cardinality of distinct files involved.
9. `unique_dirs_count`: Cardinality of distinct folder paths accessed.
10. `process_count`: Number of distinct application processes recorded.

### 2.3 Critical Epistemic Principle
> **ANOMALY DOES NOT MEAN MALICIOUS.**
> In Digital Fossil, statistical anomaly signifies only that an activity session deviates from learned baseline cadences. Legitimate administrative cleanup scripts, bulk compression tasks, or mass code refactorings often trigger anomaly scores. The UI explicitly discloses this distinction to prevent confirmation bias.

---

## 3. Component 2: Supervised Related-Event Classifier

### 3.1 Model Selection & Justification
- **Baseline Model: Logistic Regression**
  - Linear, fully interpretable model.
  - Exposes exact coefficients indicating how time differences, directory sharing, and name similarity influence relationship probability.
- **Ensemble Model: Random Forest**
  - 100 decision trees with depth capped at 6 to prevent overfitting.
  - Captures non-linear feature interactions (e.g. short time gap combined with compatible lifecycle sequences).

### 3.2 Evaluation Methodology
Models are trained and tested on a reproducible synthetic dataset generated via `generate_synthetic_ml_dataset`:
- 80/20 train/test split.
- **Actual Evaluation Metrics Computed:**
  - Accuracy
  - Precision
  - Recall
  - F1-Score
  - Full 2x2 Confusion Matrix (True Negatives, False Positives, False Negatives, True Positives)
  - Feature importances and linear coefficients

All metrics displayed in the user interface reflect actual execution of scikit-learn metrics functions on test splits. No values are hardcoded or fabricated.
