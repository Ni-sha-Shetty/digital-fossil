import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

def get_demo_scenarios_data() -> List[Dict[str, Any]]:
    """
    Returns 6 realistic synthetic digital activity scenarios.
    Demonstrates both successful workflows, incomplete evidence, and conflicting artifacts.
    """
    base_time = datetime.utcnow().replace(microsecond=0) - timedelta(hours=2)

    scenarios = [
        # Scenario 1: Document Workflow
        {
            "session_id": "SES-20261003-001",
            "scenario_tag": "document_workflow",
            "title": "Quarterly Financial Report Preparation & Distribution Workflow",
            "summary": "Creation of Q3_Financial_Report.docx, subsequent generation of PDF artifact, relocation to staging, and launch of email client.",
            "events": [
                {
                    "timestamp": (base_time + timedelta(seconds=10)).isoformat(),
                    "event_type": "FILE_CREATED",
                    "path": "C:/Users/Analyst/Documents/Projects/Q3_Financial_Report.docx",
                    "file_name": "Q3_Financial_Report.docx",
                    "extension": "docx",
                    "directory": "C:/Users/Analyst/Documents/Projects",
                    "file_size": 48200,
                    "process_name": "WINWORD.EXE",
                    "source": "synthetic_demo"
                },
                {
                    "timestamp": (base_time + timedelta(seconds=18)).isoformat(),
                    "event_type": "FILE_MODIFIED",
                    "path": "C:/Users/Analyst/Documents/Projects/Q3_Financial_Report.docx",
                    "file_name": "Q3_Financial_Report.docx",
                    "extension": "docx",
                    "directory": "C:/Users/Analyst/Documents/Projects",
                    "file_size": 52140,
                    "process_name": "WINWORD.EXE",
                    "source": "synthetic_demo"
                },
                {
                    "timestamp": (base_time + timedelta(seconds=24)).isoformat(),
                    "event_type": "FILE_CREATED",
                    "path": "C:/Users/Analyst/Documents/Projects/Q3_Financial_Report.pdf",
                    "file_name": "Q3_Financial_Report.pdf",
                    "extension": "pdf",
                    "directory": "C:/Users/Analyst/Documents/Projects",
                    "file_size": 114200,
                    "process_name": "WINWORD.EXE",
                    "source": "synthetic_demo"
                },
                {
                    "timestamp": (base_time + timedelta(seconds=27)).isoformat(),
                    "event_type": "FILE_MOVED",
                    "path": "C:/Users/Analyst/Documents/Outbox/Q3_Financial_Report.pdf",
                    "file_name": "Q3_Financial_Report.pdf",
                    "extension": "pdf",
                    "directory": "C:/Users/Analyst/Documents/Outbox",
                    "file_size": 114200,
                    "process_name": "explorer.exe",
                    "source": "synthetic_demo"
                },
                {
                    "timestamp": (base_time + timedelta(seconds=33)).isoformat(),
                    "event_type": "PROCESS_STARTED",
                    "path": "C:/Program Files/Microsoft Office/root/Office16/OUTLOOK.EXE",
                    "file_name": "OUTLOOK.EXE",
                    "extension": "exe",
                    "directory": "C:/Program Files/Microsoft Office/root/Office16",
                    "file_size": 2489000,
                    "process_name": "OUTLOOK.EXE",
                    "source": "synthetic_demo"
                }
            ]
        },

        # Scenario 2: Image Organization & Compression
        {
            "session_id": "SES-20261003-002",
            "scenario_tag": "image_workflow",
            "title": "Field Asset Photography Curation & Batch Archival",
            "summary": "Import of raw camera photos, sequential renaming into event IDs, staging into folders, and archive packaging.",
            "events": [
                {
                    "timestamp": (base_time + timedelta(minutes=10, seconds=5)).isoformat(),
                    "event_type": "FILE_CREATED",
                    "path": "C:/Users/FieldTech/Pictures/Import/IMG_8801.JPG",
                    "file_name": "IMG_8801.JPG",
                    "extension": "jpg",
                    "directory": "C:/Users/FieldTech/Pictures/Import",
                    "file_size": 4200100,
                    "process_name": "photoloader.exe",
                    "source": "synthetic_demo"
                },
                {
                    "timestamp": (base_time + timedelta(minutes=10, seconds=8)).isoformat(),
                    "event_type": "FILE_CREATED",
                    "path": "C:/Users/FieldTech/Pictures/Import/IMG_8802.JPG",
                    "file_name": "IMG_8802.JPG",
                    "extension": "jpg",
                    "directory": "C:/Users/FieldTech/Pictures/Import",
                    "file_size": 4350800,
                    "process_name": "photoloader.exe",
                    "source": "synthetic_demo"
                },
                {
                    "timestamp": (base_time + timedelta(minutes=10, seconds=15)).isoformat(),
                    "event_type": "FILE_RENAMED",
                    "path": "C:/Users/FieldTech/Pictures/SiteAudit_UnitA.JPG",
                    "file_name": "SiteAudit_UnitA.JPG",
                    "extension": "jpg",
                    "directory": "C:/Users/FieldTech/Pictures",
                    "file_size": 4200100,
                    "process_name": "explorer.exe",
                    "source": "synthetic_demo"
                },
                {
                    "timestamp": (base_time + timedelta(minutes=10, seconds=18)).isoformat(),
                    "event_type": "FILE_RENAMED",
                    "path": "C:/Users/FieldTech/Pictures/SiteAudit_UnitB.JPG",
                    "file_name": "SiteAudit_UnitB.JPG",
                    "extension": "jpg",
                    "directory": "C:/Users/FieldTech/Pictures",
                    "file_size": 4350800,
                    "process_name": "explorer.exe",
                    "source": "synthetic_demo"
                },
                {
                    "timestamp": (base_time + timedelta(minutes=10, seconds=28)).isoformat(),
                    "event_type": "FILE_CREATED",
                    "path": "C:/Users/FieldTech/Pictures/SiteAudit_Archive.zip",
                    "file_name": "SiteAudit_Archive.zip",
                    "extension": "zip",
                    "directory": "C:/Users/FieldTech/Pictures",
                    "file_size": 7900000,
                    "process_name": "7zFM.exe",
                    "source": "synthetic_demo"
                }
            ]
        },

        # Scenario 3: Normal Browsing Activity
        {
            "session_id": "SES-20261003-003",
            "scenario_tag": "normal_browsing",
            "title": "Routine Web Browsing & Local Reference Access",
            "summary": "Browser process launch, standard browser cache updates, and opening a local user manual.",
            "events": [
                {
                    "timestamp": (base_time + timedelta(minutes=20, seconds=1)).isoformat(),
                    "event_type": "PROCESS_STARTED",
                    "path": "C:/Program Files/Google/Chrome/Application/chrome.exe",
                    "file_name": "chrome.exe",
                    "extension": "exe",
                    "directory": "C:/Program Files/Google/Chrome/Application",
                    "file_size": 3100000,
                    "process_name": "chrome.exe",
                    "source": "synthetic_demo"
                },
                {
                    "timestamp": (base_time + timedelta(minutes=20, seconds=6)).isoformat(),
                    "event_type": "FILE_MODIFIED",
                    "path": "C:/Users/Staff/AppData/Local/Google/Chrome/User Data/Default/History",
                    "file_name": "History",
                    "extension": "none",
                    "directory": "C:/Users/Staff/AppData/Local/Google/Chrome/User Data/Default",
                    "file_size": 250000,
                    "process_name": "chrome.exe",
                    "source": "synthetic_demo"
                },
                {
                    "timestamp": (base_time + timedelta(minutes=20, seconds=14)).isoformat(),
                    "event_type": "FILE_ACCESSED",
                    "path": "C:/Users/Staff/Downloads/UserGuide_v2.pdf",
                    "file_name": "UserGuide_v2.pdf",
                    "extension": "pdf",
                    "directory": "C:/Users/Staff/Downloads",
                    "file_size": 890000,
                    "process_name": "AcroRd32.exe",
                    "source": "synthetic_demo"
                }
            ]
        },

        # Scenario 4: Unusual File Activity (Statistical Anomaly)
        {
            "session_id": "SES-20261003-004",
            "scenario_tag": "unusual_activity",
            "title": "Atypical High-Frequency Renaming & Rapid File Deletions",
            "summary": "Burst of 14 rapid file modifications, renaming operations, and multiple deletions within 15 seconds.",
            "events": [
                {
                    "timestamp": (base_time + timedelta(minutes=30, seconds=i)).isoformat(),
                    "event_type": "FILE_RENAMED" if i % 2 == 0 else "FILE_DELETED",
                    "path": f"C:/SharedData/Confidential/record_{i:02d}." + ("locked" if i % 2 == 0 else "bak"),
                    "file_name": f"record_{i:02d}." + ("locked" if i % 2 == 0 else "bak"),
                    "extension": "locked" if i % 2 == 0 else "bak",
                    "directory": "C:/SharedData/Confidential",
                    "file_size": 15000 * (i + 1),
                    "process_name": "powershell.exe",
                    "source": "synthetic_demo"
                }
                for i in range(14)
            ]
        },

        # Scenario 5: Incomplete Evidence (Missing Critical Conversion Link)
        {
            "session_id": "SES-20261003-005",
            "scenario_tag": "incomplete_evidence",
            "title": "Incomplete Audit Trail: Unlinked Source and Destination Artifacts",
            "summary": "Initial draft created in one directory, while a target PDF appears 4 minutes later in an external directory without intermediate staging.",
            "events": [
                {
                    "timestamp": (base_time + timedelta(minutes=45, seconds=0)).isoformat(),
                    "event_type": "FILE_CREATED",
                    "path": "C:/Users/Contractor/Documents/Contracts/VendorAgreement.docx",
                    "file_name": "VendorAgreement.docx",
                    "extension": "docx",
                    "directory": "C:/Users/Contractor/Documents/Contracts",
                    "file_size": 65000,
                    "process_name": "WINWORD.EXE",
                    "source": "synthetic_demo"
                },
                {
                    "timestamp": (base_time + timedelta(minutes=45, seconds=50)).isoformat(),
                    "event_type": "FILE_MODIFIED",
                    "path": "C:/Users/Contractor/Documents/Contracts/VendorAgreement.docx",
                    "file_name": "VendorAgreement.docx",
                    "extension": "docx",
                    "directory": "C:/Users/Contractor/Documents/Contracts",
                    "file_size": 68000,
                    "process_name": "WINWORD.EXE",
                    "source": "synthetic_demo"
                },
                {
                    "timestamp": (base_time + timedelta(minutes=46, seconds=45)).isoformat(),
                    "event_type": "FILE_CREATED",
                    "path": "D:/ExternalBackup/VendorAgreement_Signed.pdf",
                    "file_name": "VendorAgreement_Signed.pdf",
                    "extension": "pdf",
                    "directory": "D:/ExternalBackup",
                    "file_size": 182000,
                    "process_name": None,
                    "source": "synthetic_demo"
                }
            ]
        },

        # Scenario 6: Conflicting Evidence (Timestamp Inversion & Contradictory Actions)
        {
            "session_id": "SES-20261003-006",
            "scenario_tag": "conflicting_evidence",
            "title": "Conflicting Forensic Evidence: Post-Deletion Modification Discrepancy",
            "summary": "System logs show file deletion followed shortly by modification on the deleted path, indicating clock skew or log anomaly.",
            "events": [
                {
                    "timestamp": (base_time + timedelta(minutes=60, seconds=10)).isoformat(),
                    "event_type": "FILE_CREATED",
                    "path": "C:/DataStore/SensitiveClientData.xlsx",
                    "file_name": "SensitiveClientData.xlsx",
                    "extension": "xlsx",
                    "directory": "C:/DataStore",
                    "file_size": 1400000,
                    "process_name": "EXCEL.EXE",
                    "source": "synthetic_demo"
                },
                {
                    "timestamp": (base_time + timedelta(minutes=60, seconds=20)).isoformat(),
                    "event_type": "FILE_DELETED",
                    "path": "C:/DataStore/SensitiveClientData.xlsx",
                    "file_name": "SensitiveClientData.xlsx",
                    "extension": "xlsx",
                    "directory": "C:/DataStore",
                    "file_size": 0,
                    "process_name": "cmd.exe",
                    "source": "synthetic_demo"
                },
                {
                    "timestamp": (base_time + timedelta(minutes=60, seconds=25)).isoformat(),
                    "event_type": "FILE_MODIFIED",
                    "path": "C:/DataStore/SensitiveClientData.xlsx",
                    "file_name": "SensitiveClientData.xlsx",
                    "extension": "xlsx",
                    "directory": "C:/DataStore",
                    "file_size": 1420000,
                    "process_name": "EXCEL.EXE",
                    "source": "synthetic_demo"
                }
            ]
        }
    ]

    return scenarios
