# DIGITAL FOSSIL: 5-Minute Evaluation & Demo Script

## Objective
Demonstrate Digital Fossil to judges and interviewers within 5 minutes, highlighting the core value proposition: **"Don't just show what happened. Reconstruct what likely happened — and prove why."**

---

## ⏱️ Minute 0:00 – 1:00 | The Problem & One-Click Login

1. **Open the Application**: Navigate to `http://localhost:5173`.
2. **Explain the Pitch**:
   > *"Most event monitoring tools dump thousands of raw logs on an analyst—files created, modified, renamed. Individually, these logs don't explain operator behavior. Digital Fossil reconstructs these events into coherent activity sessions while strictly separating confirmed facts from probabilistic inferences and hypotheses."*
3. **Show Demo Credentials**:
   - Point out the 3 pre-configured demo roles:
     - **Investigator**: `investigator@digitalfossil.local` / `investigator123`
     - **Reviewer**: `reviewer@digitalfossil.local` / `reviewer123`
     - **Admin**: `admin@digitalfossil.local` / `admin123`
   - Click the **"Investigator" (Alex Vance)** 1-click button to authenticate immediately.

---

## ⏱️ Minute 1:00 – 2:30 | Investigator Journey: Epistemic Separation & Graph

1. **Load Document Benchmark**:
   - Click **"Load Document Workflow Benchmark"** (`INV-20261003-001`).
2. **Show Epistemic Separation (The Core Innovation)**:
   - Walk through the 4 distinct tiers:
     - **OBSERVED FACTS (Green)**: Point to `Q3_Financial_Report.docx` created, modified, `Q3_Financial_Report.pdf` created 6s later, moved to `Outbox`, and `OUTLOOK.EXE` launched. These are 100% verifiable facts.
     - **INFERENCES (Cyan)**: Point to the correlation score (0.81) between docx and pdf based on filename identity and temporal proximity.
     - **HYPOTHESES (Purple)**: Point to the formulated explanation (*"User prepared a financial report, exported it to PDF, staged it, and launched an email client"*).
     - **MANDATORY UNCERTAINTY STATEMENT (Red callout)**: Highlight the disclosure: *"No direct conversion process or email dispatch packet was recorded in evidence. Transformation is an inference based on metadata compatibility."*
     - **UNKNOWNS & MISSING EVIDENCE (Amber)**: Show the explicit gaps identified: *"Missing Converter Process"* and *"Missing Email Transmission Packet"*.
3. **Show Multi-Relational Knowledge Graph**:
   - Switch to the **"Relationship Graph"** tab.
   - Click on the `file:Q3_Financial_Report.pdf` node to open the **Entity Inspector Drawer**.
   - Show the directed edge labeled `POSSIBLY_DERIVED_FROM (0.81)`.
4. **Show Interactive Timeline**:
   - Switch to the **"Interactive Timeline"** tab.
   - Show the sequential time deltas: `+8s`, `+6s`, `+3s`, `+6s`.
5. **Export Forensic PDF Report**:
   - Click **"Export Forensic Report"**. Show the generated PDF downloaded with tables, confidence gauges, and reviewer sign-off blocks.

---

## ⏱️ Minute 2:30 – 3:45 | Reviewer Journey: Independent Quality Gate

1. **Switch Role to Reviewer**:
   - In the top navigation bar, click the **"SWITCH ROLE: REVIEWER"** shortcut.
   - The UI immediately updates with the **Reviewer Quality Gate** badge (`[REVIEWER]`).
2. **Review Queue**:
   - Open the **Review Queue** tab.
   - Select case `INV-20261003-001`.
3. **Quality Gate Attestation**:
   - Reviewers CANNOT modify raw evidence or alter system thresholds.
   - Enter a review critique in the **Reviewer Remarks** box:
     > *"Corroborated by timestamp succession and naming identity. Verified caveat that no printer spooler or converter tool was captured."*
   - Click **"Approve Reconstruction"** or **"Flag Inference as Uncertain"**.
   - Show the instant status update to **`VERDICT: APPROVED`** and audit logging.

---

## ⏱️ Minute 3:45 – 5:00 | Admin Journey & Machine Learning Explainability

1. **Switch Role to Admin**:
   - Click **"SWITCH ROLE: ADMIN"** in the top bar.
2. **Dynamic Analysis Thresholds**:
   - Point out the **Sessionization Gap Threshold** slider (default: 120s / 2 min).
   - Adjust the slider to 180s and click **"Save Configuration & Log Audit"**.
   - Show the immediate audit log entry recorded in the **System Audit Log** table below.
3. **Safe Watchdog Collector**:
   - Show the **Explicit Test Directory Monitor**.
   - Point out the mandatory defensive privacy notice (*"Strictly limited to user test folders; no surveillance or credential harvesting"*).
4. **ML Explainability Dashboard**:
   - Click the **"ML Models"** tab in the navigation bar.
   - Show genuine scikit-learn metrics: Accuracy, Precision, Recall, F1-Score, and the 2x2 Confusion Matrix for both Logistic Regression and Random Forest.
   - Demonstrate the **Interactive Pairwise Prediction Sandbox**: adjust time difference and filename similarity sliders and click **"Compute Real-Time Pairwise Inference"**.
5. **Conclusion**:
   - Summarize the key takeaway: *"Digital Fossil turns raw digital debris into trustworthy, evidence-backed reconstructions while always proving why and stating what remains uncertain."*
