#!/usr/bin/env python
"""
DIGITAL FOSSIL - Standalone Demo Dataset Generator
Generates reproducible synthetic forensic datasets across 6 core scenarios:
1. Document Workflow (docx -> pdf -> staging -> email client)
2. Image Organization & Archival (batch camera import -> rename -> zip)
3. Normal Browsing (browser launch -> cache -> local manual read)
4. Unusual Activity (atypical high-frequency modifications & mass deletion)
5. Incomplete Evidence (unobserved staging gap / missing intermediate tool)
6. Conflicting Evidence (lifecycle inversion / post-delete modification)
"""
import sys
import os
from pathlib import Path

# Add backend to sys.path
backend_path = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.database.init_db import reset_demo_database, init_database

def main():
    print("=" * 70)
    print("DIGITAL FOSSIL: Synthetic Activity Reconstruction Data Generator")
    print("=" * 70)
    print("Resetting database and seeding benchmark scenarios...")
    init_database()
    success = reset_demo_database()
    if success:
        print("[SUCCESS] All 6 forensic scenarios generated and persisted.")
        print("Scenarios available:")
        print("  1. SES-20261003-001: Document Preparation & Outbox Workflow")
        print("  2. SES-20261003-002: Batch Media Curation & Archival")
        print("  3. SES-20261003-003: Routine Web Reference & Cache Access")
        print("  4. SES-20261003-004: Elevated Velocity Deletion & Rename Anomaly")
        print("  5. SES-20261003-005: Audit Discontinuity (Incomplete Evidence)")
        print("  6. SES-20261003-006: Lifecycle Inversion (Conflicting Evidence)")
    else:
        print("[ERROR] Failed to seed demo datasets.")
        sys.exit(1)

if __name__ == "__main__":
    main()
