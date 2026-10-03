# DIGITAL FOSSIL: Data Model & Database Architecture

## 1. Database Engine & Persistence

Digital Fossil utilizes **SQLite** with Write-Ahead Logging (WAL) enabled through **SQLAlchemy 2.0**. SQLite provides zero-configuration local deployment, deterministic ACID transactions, and portability for research and forensic review.

---

## 2. Relational Schema Architecture

```
 +--------------------+       +--------------------+
 |       users        |       |    system_configs  |
 +--------------------+       +--------------------+
 | id (PK)            |       | id (PK)            |
 | email (Unique)     |       | session_thresh_sec |
 | hashed_password    |       | min_rel_score      |
 | role               |       | anomaly_threshold  |
 | full_name          |       | updated_at         |
 | is_active          |       | updated_by         |
 +--------------------+       +--------------------+

          |
          | (Attribution & Audit)
          v
 +--------------------+       +--------------------+
 |     audit_logs     |       |       events       |
 +--------------------+       +--------------------+
 | id (PK)            |       | id (PK)            |
 | timestamp          |       | event_id (Unique)  |
 | user_email         |       | timestamp          |
 | role               |       | event_type         |
 | action             |       | path               |
 | target             |       | file_name          |
 | metadata_json      |       | extension          |
 +--------------------+       | directory          |
                              | file_size          |
                              | source             |
                              | process_name       |
                              | session_id (FK)    |
                              | extra_metadata     |
                              +--------------------+
                                        |
                                        | (Belongs to)
                                        v
 +--------------------+       +--------------------+
 |   investigations   |       |      sessions      |
 +--------------------+       +--------------------+
 | id (PK)            |       | id (PK)            |
 | investigation_id   |<----->| session_id (Unique)|
 | session_id         |       | start_time         |
 | title              |       | end_time           |
 | status             |       | duration_seconds   |
 | reviewer_verdict   |       | event_count        |
 | reviewer_comment   |       | involved_files     |
 | reviewed_by        |       | involved_dirs      |
 | reviewed_at        |       | detected_processes |
 | overall_confidence |       | anomaly_score      |
 | confidence_label   |       | is_anomaly         |
 | summary            |       | confidence_score   |
 +--------------------+       | scenario_tag       |
          |                   +--------------------+
          v
 +--------------------+
 | investigation_notes|
 +--------------------+
 | id (PK)            |
 | investigation_id   |
 | author_email       |
 | author_role        |
 | content            |
 | created_at         |
 +--------------------+
```

---

## 3. Canonical Event Data Model

| Field | Type | Description |
|---|---|---|
| `event_id` | String(64) | Deterministic SHA-256 hash or system UUID prefixed with `EVT-` |
| `timestamp` | DateTime | Canonical UTC timestamp normalized across ISO, epoch, or locale formats |
| `event_type` | String(50) | Standardized enum: `FILE_CREATED`, `FILE_MODIFIED`, `FILE_MOVED`, `FILE_RENAMED`, `FILE_DELETED`, `FILE_ACCESSED`, `PROCESS_STARTED`, `PROCESS_STOPPED` |
| `path` | String(1024)| Full absolute path with normalized forward slashes |
| `file_name` | String(255) | Base file name including extension |
| `extension` | String(50) | Lowercase extension without leading dot (or `none`) |
| `directory` | String(1024)| Parent folder path |
| `file_size` | BigInteger | Byte length of the artifact |
| `process_name` | String(100)| Originating process image (e.g. `WINWORD.EXE`, `explorer.exe`) |
| `source` | String(50) | Origin identifier (`synthetic_demo`, `watchdog_live`, `manual_import`) |
| `session_id` | String(64) | Foreign key pointing to the bounded session cluster |
| `extra_metadata` | Text | JSON-serialized dictionary for auxiliary telemetry |
