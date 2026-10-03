# DIGITAL FOSSIL
### Explainable Digital Activity Reconstruction Engine
> *"Don't just show what happened. Reconstruct what likely happened — and prove why."*

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.14-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-cyan.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-Isolation%20Forest%20%2B%20Classifiers-orange.svg)](https://scikit-learn.org/)
[![NetworkX](https://img.shields.io/badge/NetworkX-Multi--Relational%20Graphs-red.svg)](https://networkx.org/)
[![Tests](https://img.shields.io/badge/Tests-31%20Passed-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-purple.svg)]()

---

## 1. The Core Product Problem

Modern operating systems produce immense volumes of low-level telemetry:
- `10:02:11` — `report.docx` created
- `10:02:15` — `report.docx` modified
- `10:02:21` — `report.pdf` created
- `10:02:23` — `report.pdf` moved to Outbox
- `10:02:29` — `OUTLOOK.EXE` process started

Examining these events individually leaves analysts with disconnected data points. Conversely, naive automated tools commit dangerous epistemic leaps, stating as fact that: *"The user converted report.docx to PDF and emailed it to external parties"* — even when no document conversion utility or email transmission log was ever captured.

### The Innovation
**Digital Fossil** bridges this divide by reconstructing raw events into meaningful activity sessions while **strictly separating confirmed facts from derived inferences and uncertain hypotheses**, providing mathematically transparent confidence scores and explicit disclosures of what remains unknown.

```
+-----------------------------------------------------------------------------------+
| OBSERVED FACTS (Verifiable OS Telemetry)                                          |
| • [FACT-01] 'Q3_Financial_Report.docx' created at 10:02:11 UTC                    |
| • [FACT-02] 'Q3_Financial_Report.pdf' created 6 seconds later in same folder      |
| • [FACT-03] 'Q3_Financial_Report.pdf' moved to Outbox at 10:02:27 UTC             |
| • [FACT-04] 'OUTLOOK.EXE' process launched at 10:02:33 UTC                        |
+-----------------------------------------------------------------------------------+
| INFERENCES (Derived Multi-Event Correlations)                                     |
| • [INF-01] DOCX and PDF share 0.81 correlation score based on 100% filename base  |
|   similarity, 6s temporal gap, and compatible extension pairing.                  |
+-----------------------------------------------------------------------------------+
| HYPOTHESES (Explanatory Models of Human Activity)                                 |
| • [HYP-01] User drafted a financial report, exported it to PDF, staged the        |
|   artifact, and prepared to dispatch it via mail client.                          |
|   Confidence: 81% (HIGH)                                                          |
|   MANDATORY UNCERTAINTY STATEMENT:                                                |
|   "No direct file conversion daemon or email dispatch packet was captured in logs.|
|   Document transformation is inferred from metadata compatibility."               |
+-----------------------------------------------------------------------------------+
| GAPS & UNKNOWNS (Chain of Custody Discontinuities)                                |
| • [MISS-01] Missing Process Telemetry: No printer spooler or converter was logged.|
| • [MISS-02] Missing Network Transmission: Email application opened, but no        |
|   subsequent socket send or attachment event was observed.                        |
+-----------------------------------------------------------------------------------+
```

---

## 2. Key Architectural Features

- **Epistemic Hygiene**: Hardcoded architectural separation between facts, inferences, hypotheses, and unknowns. The system **never invents evidence** and **never presents an inference as a fact**.
- **Transparent Multi-Factor Correlation**:
  $$S_{\text{composite}} = 0.30 S_{\text{time}} + 0.25 S_{\text{name}} + 0.20 S_{\text{seq}} + 0.15 S_{\text{dir}} + 0.10 S_{\text{ext}} + B_{\text{proc}}$$
- **Unsupervised Anomaly Detection**: `IsolationForest` (scikit-learn) evaluates 10-dimensional session feature vectors to flag atypical velocity or destruction cadences. *(Explicitly notes: Anomaly ≠ Malicious).*
- **Supervised Event-Relation Prediction**: Logistic Regression (interpretable linear baseline with exact feature weights) and Random Forest (non-linear ensemble). Real evaluation metrics computed dynamically on test splits.
- **Multi-Relational Knowledge Graph**: NetworkX directed multi-graph linking Sessions, Directories, Files, Events, and Processes with typed relationship edges (`CREATED`, `MODIFIED`, `POSSIBLY_DERIVED_FROM`, `SAME_SESSION`).
- **Role-Based Access Control (RBAC)**: Backend-enforced authorization across **Investigator**, **Reviewer**, and **Administrator** roles.
- **Safe Directory Monitor (Mode B)**: Watchdog-based collector restricted strictly to user-designated folders. No keystroke logging, credential harvesting, or covert surveillance.
- **Forensic PDF Export**: One-click generation of professional investigation reports using ReportLab.

---

## 3. User Roles & Workflows

### Role 1: Investigator
- Analyzes activity timelines and investigates specific cases.
- Inspects verifiable facts, derived correlations, and relationship graphs.
- Authors collaborative investigation notes.
- Exports formal PDF reports.

### Role 2: Reviewer
- Independent quality gate over reconstructions.
- **Approves** or **Flags** inferences. If flagged, a substantive review critique is strictly required.
- Cannot modify raw evidence or change system configurations.

### Role 3: Administrator
- Governs the system, provisions users, and inspects immutable audit logs.
- Configures live analysis thresholds (Session gap gate, minimum relationship score, anomaly contamination).
- Starts and stops the local safe watchdog folder monitor.
- Resets benchmark scenarios to clean initial states.

---

## 4. Demo Credentials

> **Notice:** These accounts are pre-configured demo credentials intended strictly for development and evaluation. Passwords are encrypted using `bcrypt` hashes.

| Role | Email Address | Password | Permissions |
|---|---|---|---|
| **Investigator** | `investigator@digitalfossil.local` | `investigator123` | Case analysis, graph inspection, notes, PDF export |
| **Reviewer** | `reviewer@digitalfossil.local` | `reviewer123` | Review queue, attestation approval/flagging, PDF export |
| **Admin** | `admin@digitalfossil.local` | `admin123` | Full governance, threshold sliders, watchdog monitor, audit logs |

---

## 5. Technology Stack

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy 2.0, SQLite (WAL mode), Pydantic v2.
- **Machine Learning**: scikit-learn (Isolation Forest, Logistic Regression, Random Forest), NumPy, Pandas.
- **Graph Theory**: NetworkX (DiGraph modeling).
- **Document Generation**: ReportLab (vector PDF compiler).
- **File Monitoring**: Watchdog (safe filesystem event observer).
- **Security & Auth**: bcrypt password hashing, PyJWT bearer token authorization.
- **Frontend**: React 19, TypeScript, Vite, Lucide Icons, Cyber-Forensic Dark Glassmorphism CSS.

---

## 6. Installation & Local Setup

### Prerequisites
- Python 3.11+
- Node.js v18+ and npm
- Git

### Step 1: Clone Repository
```powershell
git clone https://github.com/your-username/digital-fossil.git
cd digital-fossil
```

### Step 2: Backend Setup
```powershell
# Windows PowerShell:
python -m pip install -r backend/requirements.txt email-validator

# Initialize database and seed 6 forensic benchmark scenarios:
python -m backend.app.database.init_db
```

### Step 3: Frontend Setup
```powershell
cd frontend
npm install
npm run build
cd ..
```

---

## 7. Running the Application

### Option A: Running Development Servers

**Terminal 1 (Backend API):**
```powershell
# From project root:
python scripts/run_server.py
# Backend API will be available at http://127.0.0.1:8000
# OpenAPI / Swagger documentation at http://127.0.0.1:8000/docs
```

**Terminal 2 (Frontend Client):**
```powershell
cd frontend
npm run dev
# Frontend will be live at http://localhost:5173
```

### Option B: Docker Compose
```bash
docker-compose up --build
# Frontend at http://localhost:5173, Backend at http://localhost:8000
```

---

## 8. Verification & Automated Testing

The project includes a comprehensive, non-placeholder test suite covering event parsing, normalization resilience, sessionization edge cases, mathematical correlation bounds, epistemic inference separation, scikit-learn training validation, and API RBAC authorization.

Run all 31 automated tests with verbose output:
```powershell
python -m pytest backend/app/tests -v
```

Expected output:
```text
======================= 31 passed in ~6.7s =======================
```

---

## 9. Included Documentation Suite

Comprehensive technical architectural documentation is provided in the [`docs/`](file:///docs/) directory:
- [System Architecture & Dataflow](file:///docs/ARCHITECTURE.md)
- [Machine Learning & Anomaly Methodology](file:///docs/ML.md)
- [Inference Engine & Confidence Scoring](file:///docs/INFERENCE_ENGINE.md)
- [Data Model & Schema Reference](file:///docs/DATA_MODEL.md)
- [Security, Privacy & RBAC Policy](file:///docs/SECURITY.md)
- [5-Minute Judge Demo Script](file:///docs/DEMO_SCRIPT.md)
- [Interviewer Questions & Architectural Defense](file:///docs/INTERVIEW_QUESTIONS.md)

---

## 10. Defensive Research Disclaimer & Ethical Statement

**Digital Fossil** is developed as an explainable activity reconstruction research platform. It is NOT intended as a covert surveillance tool or a substitute for sworn forensic chain-of-custody proceedings. The system collects only safe metadata, enforces defensive privacy constraints, and mandates explicit disclosures of uncertainty.
