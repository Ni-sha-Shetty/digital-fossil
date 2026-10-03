import logging
from sqlalchemy.orm import Session
from app.database.connection import engine, Base, SessionLocal
from app.models.user import User
from app.models.config import SystemConfig
from app.models.audit import AuditLog
from app.models.event import Event
from app.models.session import Session as SessionModel
from app.models.investigation import Investigation, InvestigationNote
from app.auth.security import hash_password
from app.services.demo_service import get_demo_scenarios_data
from app.services.pipeline_service import process_raw_events_pipeline

logger = logging.getLogger("digital_fossil.init_db")

DEMO_USERS = [
    {
        "email": "investigator@digitalfossil.local",
        "password": "investigator123",
        "full_name": "Senior Investigator Alex Vance",
        "role": "investigator"
    },
    {
        "email": "reviewer@digitalfossil.local",
        "password": "reviewer123",
        "full_name": "Quality Reviewer Morgan Reed",
        "role": "reviewer"
    },
    {
        "email": "admin@digitalfossil.local",
        "password": "admin123",
        "full_name": "System Administrator Jordan Croft",
        "role": "admin"
    }
]

def init_database():
    """Initializes tables, seeds demo accounts, thresholds, and synthetic scenarios."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # 1. Seed Demo Users
        for u_data in DEMO_USERS:
            existing = db.query(User).filter(User.email == u_data["email"]).first()
            if not existing:
                user = User(
                    email=u_data["email"],
                    hashed_password=hash_password(u_data["password"]),
                    full_name=u_data["full_name"],
                    role=u_data["role"],
                    is_active=True
                )
                db.add(user)
                logger.info(f"Seeded user: {u_data['email']} ({u_data['role']})")
        db.commit()

        # 2. Seed Default Config
        existing_cfg = db.query(SystemConfig).first()
        if not existing_cfg:
            cfg = SystemConfig(
                session_threshold_sec=120,
                min_relationship_score=0.35,
                anomaly_threshold=0.10,
                updated_by="system_init"
            )
            db.add(cfg)
            db.commit()
            logger.info("Seeded system config default thresholds.")

        # 3. Seed Demo Scenarios if no investigations exist
        inv_count = db.query(Investigation).count()
        if inv_count == 0:
            logger.info("Seeding 6 realistic demo scenarios...")
            scenarios = get_demo_scenarios_data()
            for sc in scenarios:
                process_raw_events_pipeline(
                    raw_records=sc["events"],
                    db=db,
                    scenario_tag=sc["scenario_tag"]
                )

            # Add sample notes and review comment to the primary scenario for immediate demonstration
            primary_inv = db.query(Investigation).filter(Investigation.investigation_id == "INV-20261003-001").first()
            if primary_inv:
                primary_inv.reviewer_verdict = "approved"
                primary_inv.reviewer_comment = (
                    "Observed temporal succession and filename identity strongly correlate the docx creation "
                    "with PDF export. However, caveat noted that direct file converter process was not captured in logs."
                )
                primary_inv.reviewed_by = "reviewer@digitalfossil.local"
                
                note = InvestigationNote(
                    investigation_id="INV-20261003-001",
                    author_email="investigator@digitalfossil.local",
                    author_role="investigator",
                    content="Cross-referenced timestamp with external firewall outbox logs. The 6-second delta strongly indicates local programmatic save-as/export."
                )
                db.add(note)
                db.commit()

            # Record initial audit entry
            init_audit = AuditLog(
                user_email="system@digitalfossil.local",
                role="system",
                action="DATABASE_INITIALIZED",
                target="sqlite://digital_fossil.db",
                metadata_json='{"status": "ready", "scenarios_seeded": 6}'
            )
            db.add(init_audit)
            db.commit()
            logger.info("Database initialized with demo users, thresholds, scenarios, and initial notes.")
    finally:
        db.close()

def reset_demo_database():
    """Clears and re-seeds all events, sessions, investigations, and notes while keeping users."""
    db = SessionLocal()
    try:
        db.query(InvestigationNote).delete()
        db.query(Investigation).delete()
        db.query(SessionModel).delete()
        db.query(Event).delete()
        db.commit()

        scenarios = get_demo_scenarios_data()
        for sc in scenarios:
            process_raw_events_pipeline(
                raw_records=sc["events"],
                db=db,
                scenario_tag=sc["scenario_tag"]
            )
        
        primary_inv = db.query(Investigation).filter(Investigation.investigation_id == "INV-20261003-001").first()
        if primary_inv:
            primary_inv.reviewer_verdict = "approved"
            primary_inv.reviewer_comment = "Corroborated by timestamp sequence and filename similarity."
            primary_inv.reviewed_by = "reviewer@digitalfossil.local"
            note = InvestigationNote(
                investigation_id="INV-20261003-001",
                author_email="investigator@digitalfossil.local",
                author_role="investigator",
                content="Initial automated analysis verified."
            )
            db.add(note)
            db.commit()

        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to reset demo database: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_database()
