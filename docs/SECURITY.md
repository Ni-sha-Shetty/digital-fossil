# DIGITAL FOSSIL: Security, Privacy & Role Authorization

## 1. Defensive Security Architecture

Digital Fossil is strictly an **educational and explainable activity reconstruction research platform**. It is designed as a local-first, defensive tool.

### Explicit Privacy Guardrails:
1. **No Keystroke Logging**: The system does NOT capture keystrokes.
2. **No Credential Harvesting**: The system NEVER accesses browser credential vaults, password managers, or session cookies.
3. **No Screen or Clipboard Capture**: No video, screenshot, or clipboard contents are gathered.
4. **No Covert Surveillance**: Monitoring is NOT system-wide by default. The live file-monitoring collector can ONLY be activated on an explicitly designated, user-controlled directory.

---

## 2. Safe Watchdog Collector Restrictions

When operating in Mode B (Local Folder Monitoring), the collector enforces strict safeguards:
- **Restricted Path Filtering**: Automatically blocks root drive roots (`C:\`, `/`) and system directories (`Windows`, `System32`, `Program Files`, `AppData/Local/Microsoft`).
- **Safe Metadata Collection Only**: Gathers timestamps, file actions (create, modify, move, delete), file extensions, and file sizes. Does NOT read or transmit file contents.
- **Explicit Operator Confirmation**: The collector displays a permanent banner: *"Monitoring is limited strictly to the selected test directory."*
- **Immediate Termination**: Can be cleanly halted with a single click or API call.

---

## 3. Role-Based Access Control (RBAC)

Digital Fossil enforces role permissions on the backend API layer using FastAPI dependencies:

| Capability | Investigator | Reviewer | Administrator |
|---|:---:|:---:|:---:|
| View Event Timelines & Ledger | YES | YES | YES |
| Inspect Knowledge Graph & Evidence | YES | YES | YES |
| View Facts, Inferences, Hypotheses | YES | YES | YES |
| Add Investigation Notes | YES | YES | YES |
| Export Forensic PDF Report | YES | YES | YES |
| Approve / Flag Inferences | NO | **YES** | YES |
| Modify Raw Telemetry / Events | **FORBIDDEN** | **FORBIDDEN** | **FORBIDDEN** |
| Configure Analysis Thresholds | NO | NO | **YES** |
| Manage Operators & User Accounts | NO | NO | **YES** |
| Control Live Folder Collector | NO | NO | **YES** |
| View System Audit Logs | NO | NO | **YES** |
| Reset Benchmark Datasets | NO | NO | **YES** |

---

## 4. Cryptographic Standards
- **Password Hashing**: Implemented using `bcrypt` with automatic salting (cost factor 12). Plaintext passwords are never persisted.
- **Session Tokens**: Implemented via JSON Web Tokens (JWT) signed with HMAC-SHA256 (`HS256`).
- **Audit Logging**: Sensitive operations (login, review decisions, configuration changes, dataset resets) generate immutable records stored in the `audit_logs` table.
