# DIGITAL FOSSIL: System Architecture & Dataflow

## 1. Executive Architecture Overview

**Digital Fossil** is an explainable digital activity reconstruction engine designed to ingest discrete filesystem and operating system events, cluster them into bounded activity sessions, extract multi-dimensional feature graphs, and synthesize deterministic, evidence-backed hypotheses of operator actions without ever conflating facts with inferences.

```
                    +-----------------------------+
                    |        EVENT SOURCES        |
                    |  - Synthetic Benchmarks (A) |
                    |  - Watchdog Live Folder (B) |
                    +--------------+--------------+
                                   |
                                   v
                    +-----------------------------+
                    |    INGESTION & NORMALIZER   |
                    |  - Resilient Field Parsing  |
                    |  - SHA-256 Event Deduplication
                    |  - Canonical Event Model    |
                    +--------------+--------------+
                                   |
                                   v
                    +-----------------------------+
                    |    TEMPORAL SESSIONIZER     |
                    |  - Configurable Delta Gate  |
                    |  - Activity Bounding        |
                    +--------------+--------------+
                                   |
                                   v
                    +-----------------------------+
                    |    STATISTICAL ANOMALY ML   |
                    |  - Scikit-learn Isolation   |
                    |    Forest (Contamination 10%)
                    |  - Behavioral Divergence    |
                    +--------------+--------------+
                                   |
                                   v
                    +-----------------------------+
                    |     CORRELATION & GRAPH     |
                    |  - NetworkX Multi-Graph     |
                    |  - Levenshtein / Seq Scores |
                    |  - Exponential Time Decay   |
                    +--------------+--------------+
                                   |
                                   v
                    +-----------------------------+
                    | DETERMINISTIC INFERENCE ENG |
                    |  - OBSERVED FACTS (Direct)  |
                    |  - INFERENCES (Derived)     |
                    |  - HYPOTHESES (Uncertain)   |
                    |  - GAPS & CONFLICTS (Audit) |
                    +--------------+--------------+
                                   |
                                   v
                    +-----------------------------+
                    |   CONFIDENCE SCORING ENG    |
                    |  - Penalty / Bonus Formula  |
                    |  - Non-Statistical Cap      |
                    +--------------+--------------+
                                   |
                                   v
                    +-----------------------------+
                    |    ROLE-BASED PRESENTATION  |
                    |  - Investigator Console     |
                    |  - Reviewer Quality Gate    |
                    |  - Admin Governance Center  |
                    +-----------------------------+
```

---

## 2. Component Design & Modularity

### 2.1 Backend Architecture
The backend is structured under `backend/app/` following strict separation of concerns:
- **`engine/`**: Core mathematical and logic processing pipelines:
  - `normalizer.py`: Sanitizes heterogeneous timestamps, paths, and event aliases into canonical dataclasses.
  - `sessionizer.py`: Time-series clustering bounding events into coherent operator sessions based on an admin-configurable threshold (default: 120s).
  - `correlator.py`: Multi-factor pairwise scoring engine combining exponential temporal decay, filename sequence matching, directory locality, extension compatibility, and process lineage.
  - `feature_extractor.py`: Extracts numeric vectors for both session-level anomaly analysis and event-pair relation modeling.
  - `confidence_scorer.py`: Transparent composite scoring function with penalties for gaps and contradictions.
  - `inference_engine.py`: Epistemic categorization engine strictly enforcing fact-inference-hypothesis separation.
  - `explanation.py`: Constructs sanitized JSON evidence packages and dispatches to optional LLMs or a deterministic template generator.
- **`graph/`**:
  - `builder.py`: Implements a multi-type directed knowledge graph using NetworkX. Nodes represent Sessions, Directories, Files, Events, and Processes; edges represent relationship transitions, containment, and derivations.
- **`ml/`**:
  - `anomaly_detector.py`: Scikit-learn Isolation Forest model detecting behavioral novelty.
  - `related_classifier.py`: Interpretable Logistic Regression baseline and Random Forest classifier trained on reproducible synthetic features.
  - `dataset.py`: Synthetic feature and benchmark generators.
- **`collectors/`**:
  - `folder_monitor.py`: Watchdog-based filesystem listener restricted to an explicitly selected directory. Enforces defensive privacy constraints.
- **`database/`**:
  - `connection.py`: Thread-safe SQLite engine with SQLAlchemy 2.0 session factory.
  - `init_db.py`: Database schema provisioning and benchmark dataset seeding.
- **`models/` & `schemas/`**:
  - Pydantic v2 schemas for robust request/response validation and SQLAlchemy ORM models.
- **`api/`**:
  - Modular FastAPI routers with role-based JWT dependency injection.

---

## 3. Epistemic Separation Guarantee

A foundational architectural requirement of Digital Fossil is **Epistemic Hygiene**:
1. **Observed Facts**: 1-to-1 representation of verifiable telemetry records. No inference or extrapolation is allowed in this tier.
2. **Inferences**: Derived correlations between two or more observed records, explicitly annotated with supporting event IDs and factor scoring breakdowns.
3. **Hypotheses**: Plausible explanatory reconstructions of human intent. Each hypothesis MUST include an **explicit uncertainty disclosure** detailing what assumptions cannot be proven from telemetry alone.
4. **Unknowns & Gaps**: Explicit cataloging of missing steps in the chain of custody (e.g., missing converter daemon, missing network transmission log) and contradictory telemetry.
