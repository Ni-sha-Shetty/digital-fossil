# DIGITAL FOSSIL: Architecture & Technical Defense (Interview Guide)

This document provides deep technical rationales for every design decision, technology choice, and mathematical formulation implemented in Digital Fossil.

---

### Q1: Why Python for the backend?
**Answer:** Python is the industry standard for digital forensics, data science, and applied machine learning. Its ecosystem provides mature, audited libraries for temporal analysis (`pandas`, `numpy`), graph theory (`networkx`), statistical anomaly detection (`scikit-learn`), and high-performance asynchronous networking (`fastapi`, `uvicorn`). Using Python ensures that data structures can transition seamlessly from raw telemetry ingestion into matrix operations and graph traversals without serialization bottlenecks.

---

### Q2: Why Pandas & NumPy?
**Answer:** Digital activity produces high-frequency time-series event streams. NumPy provides vectorized, memory-contiguous array operations for feature vector extraction and distance metrics. Pandas enables rapid temporal aggregation, rolling-window calculations, and group-by sessionization across thousands of timestamps with microsecond precision.

---

### Q3: Why SQLite with SQLAlchemy?
**Answer:** SQLite is embedded, zero-configuration, and fully ACID-compliant. In forensic and defensive research contexts, an investigation package must often be portable and self-contained. SQLite stores all records in a single local `.db` file that can be audited independently. By coupling SQLite with SQLAlchemy 2.0 ORM and Write-Ahead Logging (WAL) mode, we achieve high-concurrency read throughput and clean declarative schema modeling while maintaining the option to point to PostgreSQL in enterprise production without changing code.

---

### Q4: Why FastAPI?
**Answer:** FastAPI was selected over traditional frameworks (such as Flask or Django) for four primary reasons:
1. **Asynchronous Concurrency**: Built on Starlette and ASGI, handling live watchdog telemetry polling and long-running ML queries without thread exhaustion.
2. **Strict Type Safety**: Deep integration with Pydantic v2 ensures that all incoming raw events and outgoing forensic schemas are validated against strict canonical types.
3. **Automated Interactive Documentation**: Generates OpenAPI/Swagger specifications at `/docs` natively.
4. **Clean Dependency Injection**: Perfect for role-based authorization gates (`require_investigator`, `require_reviewer`, `require_admin`).

---

### Q5: Why NetworkX for Graph Representation?
**Answer:** Digital events do not exist in linear isolation—they form multi-relational graphs of containment, lifecycle transitions, and cross-artifact derivations. NetworkX provides an expressive Python data structure (`DiGraph`) to model heterogeneous node entities (Files, Events, Processes, Directories, Sessions) and directed edges (e.g. `CREATED`, `POSSIBLY_DERIVED_FROM`, `SAME_SESSION`). It allows us to compute path reachability, node degrees, and cluster connectivity prior to exporting to JSON for frontend visualization.

---

### Q6: Why Isolation Forest for Anomaly Detection?
**Answer:** Traditional anomaly detection often assumes Gaussian data distributions or requires labeled anomaly data (which is notoriously scarce in forensics). Isolation Forest is an unsupervised tree ensemble that explicitly isolates anomalies rather than profiling normal data points. Because anomalous sessions (e.g. burst-speed deletions, mass renames, or atypical lifecycle intervals) require fewer random partition splits to isolate, they produce shorter tree depths. This yields a fast, scale-invariant anomaly score without making unsupportable assumptions about normal operator behavior.

---

### Q7: Why Logistic Regression alongside Random Forest?
**Answer:** Explainability is paramount in forensics. A black-box neural network cannot easily defend its reasoning under cross-examination. Logistic Regression serves as an interpretable linear baseline whose mathematical coefficients demonstrate exactly how much weight is given to time deltas versus filename matching. Random Forest complements it by capturing non-linear interactions without sacrificing feature importance transparency (via Gini impurity metrics).

---

### Q8: Why use Synthetic Benchmark Datasets?
**Answer:** Real-world incident response datasets often contain proprietary source code, private communications, or sensitive credentials that cannot legally or ethically be bundled into public repositories. Synthetic generation allows us to craft controlled, mathematically reproducible benchmarks representing six distinct forensic conditions (standard document export, image batching, web browsing, velocity anomalies, missing intermediate steps, and contradictory timestamps).

---

### Q9: Why "Evidence Confidence" rather than "Statistical Probability of Truth"?
**Answer:** In digital forensics, claiming that an inferred event has "a 95% probability of having occurred" implies a calibrated frequentist or Bayesian posterior distribution over all human activity—which is mathematically dishonest when operating on partial telemetry. Digital Fossil rejects this pseudo-certainty. We explicitly compute **"Evidence Confidence"**, a bounded metric (0.05 to 0.95) reflecting the convergence of supporting telemetry, penalized by unobserved custody gaps and contradictions.

---

### Q10: Why strictly separate Facts, Inferences, Hypotheses, and Unknowns?
**Answer:** Conflating inference with fact is the leading cause of forensic errors and confirmation bias. If a tool reports *"User converted and emailed report.docx"* when telemetry only recorded a DOCX file creation, a PDF creation 6 seconds later, and an email client launch, the tool has committed an epistemic leap. Digital Fossil enforces strict separation:
- **Fact**: DOCX created; PDF created 6s later; Outlook started.
- **Inference**: DOCX and PDF share high structural correlation (score 0.81).
- **Hypothesis**: The user may have exported the document prior to opening mail.
- **Uncertainty Disclosure**: No conversion daemon or transmission packet was recorded; transformation is inferred.

---

### Q11: Why Role-Based Access Control (RBAC)?
**Answer:** In genuine investigative workflows, the integrity of evidence requires distinct separation of duties:
- **Investigators** explore hypotheses, construct timelines, and author notes.
- **Reviewers** act as independent quality gates, evaluating whether the evidence warrants the conclusions without having the power to alter raw logs.
- **Administrators** govern users, tune statistical thresholds, and monitor audit trails.
Enforcing RBAC in the backend ensures that no single user can arbitrarily modify system parameters or bypass peer review.

---

### Q12: What are the current limitations and future improvements?
**Answer:**
- **Current Limitations**:
  - Operates primarily on filesystem and process startup telemetry; does not inspect deep network socket payloads or volatile kernel memory artifacts.
  - Relies on time synchronization across monitored endpoints (clock skew produces conflicting indicators).
- **Future Improvements**:
  - Integration with Linux eBPF probes and Windows ETW (Event Tracing for Windows) for sub-millisecond process thread tracing.
  - Formal causal DAG inference using Do-calculus.
  - Cryptographic hash-chaining of audit logs on tamper-evident append-only ledgers.
