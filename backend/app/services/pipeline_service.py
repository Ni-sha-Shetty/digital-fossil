import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.event import Event
from app.models.session import Session as SessionModel
from app.models.investigation import Investigation, InvestigationNote
from app.models.config import SystemConfig
from app.engine.normalizer import normalize_raw_event
from app.engine.sessionizer import sessionize_events
from app.engine.feature_extractor import extract_session_features
from app.engine.inference_engine import reconstruct_session_activity
from app.engine.explanation import build_evidence_package, generate_explainable_narrative
from app.graph.builder import build_investigation_graph
from app.ml.anomaly_detector import anomaly_detector
from app.ml.related_classifier import related_classifier
from app.schemas.event import EventNormalized
from app.schemas.investigation import InvestigationDetail, NoteResponse

logger = logging.getLogger("digital_fossil.pipeline")

def get_current_thresholds(db: Session) -> tuple[int, float, float]:
    cfg = db.query(SystemConfig).first()
    if cfg:
        return cfg.session_threshold_sec, cfg.min_relationship_score, cfg.anomaly_threshold
    return 120, 0.35, 0.10

def process_raw_events_pipeline(
    raw_records: List[Dict[str, Any]],
    db: Session,
    scenario_tag: str = "general"
) -> Dict[str, Any]:
    """
    Executes the complete Digital Fossil analysis pipeline:
    RAW EVENTS -> NORMALIZATION -> VALIDATION -> SESSIONIZATION -> FEATURE EXTRACTION
    -> GRAPH -> ANOMALY DETECTION -> INFERENCE -> CONFIDENCE -> EXPLANATION -> PERSISTENCE
    """
    session_th_sec, min_rel_score, _ = get_current_thresholds(db)

    # 1. Normalization & Validation
    normalized_events: List[EventNormalized] = []
    seen_ids = set()

    for r in raw_records:
        norm = normalize_raw_event(r)
        if norm and norm.event_id not in seen_ids:
            seen_ids.add(norm.event_id)
            normalized_events.append(norm)

    if not normalized_events:
        return {"sessions_created": 0, "events_processed": 0}

    # 2. Sessionization
    session_groups = sessionize_events(normalized_events, threshold_seconds=session_th_sec)

    created_inv_ids = []

    for group in session_groups:
        tag = scenario_tag if scenario_tag != "general" else group.scenario_tag

        # 3. Feature extraction & Anomaly detection
        feat_vector = extract_session_features(group.events)
        anomaly_res = anomaly_detector.evaluate_session(feat_vector)

        # 4. Inference Engine & Confidence Scoring
        reconstruction = reconstruct_session_activity(
            group.events,
            scenario_tag=tag,
            ml_pairwise_predictor=related_classifier.predict_pair
        )

        # 5. Persist Session Model
        ses_model = db.query(SessionModel).filter(SessionModel.session_id == group.session_id).first()
        if not ses_model:
            ses_model = SessionModel(
                session_id=group.session_id,
                start_time=group.start_time,
                end_time=group.end_time,
                duration_seconds=group.duration_seconds,
                event_count=group.event_count,
                involved_files=json.dumps(group.involved_files),
                involved_directories=json.dumps(group.involved_directories),
                detected_processes=json.dumps(group.detected_processes),
                anomaly_score=anomaly_res["anomaly_score"],
                is_anomaly=anomaly_res["is_anomaly"],
                confidence_score=reconstruction.overall_confidence,
                scenario_tag=tag,
                status="analyzed"
            )
            db.add(ses_model)
        else:
            ses_model.duration_seconds = group.duration_seconds
            ses_model.event_count = group.event_count
            ses_model.anomaly_score = anomaly_res["anomaly_score"]
            ses_model.is_anomaly = anomaly_res["is_anomaly"]
            ses_model.confidence_score = reconstruction.overall_confidence

        db.flush()

        # 6. Persist Events
        for evt in group.events:
            evt.session_id = group.session_id
            existing_event = db.query(Event).filter(Event.event_id == evt.event_id).first()
            if not existing_event:
                db_event = Event(
                    event_id=evt.event_id,
                    timestamp=evt.timestamp,
                    event_type=evt.event_type,
                    path=evt.path,
                    file_name=evt.file_name,
                    extension=evt.extension,
                    directory=evt.directory,
                    file_size=evt.file_size,
                    source=evt.source,
                    process_name=evt.process_name,
                    session_id=group.session_id,
                    extra_metadata=json.dumps(evt.extra_metadata)
                )
                db.add(db_event)

        # 7. Generate Investigation Record
        inv_id = f"INV-{group.session_id.replace('SES-', '')}"
        existing_inv = db.query(Investigation).filter(Investigation.investigation_id == inv_id).first()

        title_map = {
            "document_workflow": "Document Preparation & Outbox Relocation Investigation",
            "image_workflow": "Media Curation & Archival Session Analysis",
            "normal_browsing": "Routine Local Reference & Cache Verification",
            "unusual_activity": "Elevated Event Velocity & Modification Anomaly Investigation",
            "incomplete_evidence": "Audit Trail Discontinuity & Missing Staging Investigation",
            "conflicting_evidence": "Timestamp Contradiction & Lifecycle Inversion Review"
        }
        title = title_map.get(tag, f"Activity Reconstruction: {group.session_id}")

        evidence_pkg = build_evidence_package(
            observed_facts=reconstruction.observed_facts,
            inferences=reconstruction.inferences,
            hypotheses=reconstruction.hypotheses,
            missing_evidence=reconstruction.missing_evidence,
            conflicting_evidence=reconstruction.conflicting_evidence,
            confidence=reconstruction.overall_confidence
        )

        ai_summary = generate_explainable_narrative(evidence_pkg)

        if not existing_inv:
            inv = Investigation(
                investigation_id=inv_id,
                session_id=group.session_id,
                title=title,
                status="open",
                overall_confidence=reconstruction.overall_confidence,
                confidence_label=reconstruction.confidence_label,
                observed_facts_count=len(reconstruction.observed_facts),
                inferences_count=len(reconstruction.inferences),
                hypotheses_count=len(reconstruction.hypotheses),
                unknowns_count=len(reconstruction.missing_evidence) + len(reconstruction.conflicting_evidence),
                summary=ai_summary
            )
            db.add(inv)
        else:
            existing_inv.overall_confidence = reconstruction.overall_confidence
            existing_inv.confidence_label = reconstruction.confidence_label
            existing_inv.observed_facts_count = len(reconstruction.observed_facts)
            existing_inv.inferences_count = len(reconstruction.inferences)
            existing_inv.hypotheses_count = len(reconstruction.hypotheses)
            existing_inv.unknowns_count = len(reconstruction.missing_evidence) + len(reconstruction.conflicting_evidence)
            existing_inv.summary = ai_summary

        created_inv_ids.append(inv_id)

    db.commit()
    logger.info(f"Pipeline processed {len(normalized_events)} events across {len(session_groups)} sessions.")
    return {
        "sessions_created": len(session_groups),
        "events_processed": len(normalized_events),
        "investigation_ids": created_inv_ids
    }

def get_investigation_detail(investigation_id: str, db: Session) -> Optional[InvestigationDetail]:
    inv = db.query(Investigation).filter(Investigation.investigation_id == investigation_id).first()
    if not inv:
        return None

    session = db.query(SessionModel).filter(SessionModel.session_id == inv.session_id).first()
    db_events = db.query(Event).filter(Event.session_id == inv.session_id).order_by(Event.timestamp.asc()).all()

    # Convert to EventNormalized
    norm_events = [
        EventNormalized(
            event_id=e.event_id,
            timestamp=e.timestamp,
            event_type=e.event_type,
            path=e.path,
            file_name=e.file_name,
            extension=e.extension,
            directory=e.directory,
            file_size=e.file_size,
            source=e.source,
            process_name=e.process_name,
            session_id=e.session_id,
            extra_metadata=json.loads(e.extra_metadata or "{}")
        )
        for e in db_events
    ]

    tag = session.scenario_tag if session else "general"
    reconstruction = reconstruct_session_activity(
        norm_events,
        scenario_tag=tag,
        ml_pairwise_predictor=related_classifier.predict_pair
    )

    _, min_rel_score, _ = get_current_thresholds(db)
    graph_data = build_investigation_graph(
        session_id=inv.session_id,
        events=norm_events,
        min_relationship_score=min_rel_score
    )

    # Fetch notes
    notes = db.query(InvestigationNote).filter(InvestigationNote.investigation_id == investigation_id).order_by(InvestigationNote.created_at.asc()).all()

    return InvestigationDetail(
        id=inv.id,
        investigation_id=inv.investigation_id,
        session_id=inv.session_id,
        title=inv.title,
        status=inv.status,
        reviewer_verdict=inv.reviewer_verdict,
        reviewer_comment=inv.reviewer_comment,
        reviewed_by=inv.reviewed_by,
        reviewed_at=inv.reviewed_at,
        overall_confidence=inv.overall_confidence,
        confidence_label=inv.confidence_label,
        observed_facts_count=inv.observed_facts_count,
        inferences_count=inv.inferences_count,
        hypotheses_count=inv.hypotheses_count,
        unknowns_count=inv.unknowns_count,
        summary=inv.summary,
        created_at=inv.created_at,
        updated_at=inv.updated_at,
        session_start=session.start_time if session else inv.created_at,
        session_end=session.end_time if session else inv.created_at,
        session_duration=session.duration_seconds if session else 0.0,
        is_anomaly=session.is_anomaly if session else False,
        anomaly_score=session.anomaly_score if session else 0.0,
        observed_facts=reconstruction.observed_facts,
        inferences=reconstruction.inferences,
        hypotheses=reconstruction.hypotheses,
        missing_evidence=reconstruction.missing_evidence,
        conflicting_evidence=reconstruction.conflicting_evidence,
        ai_explanation=inv.summary,
        graph=graph_data,
        notes=[NoteResponse.from_orm(n) for n in notes]
    )
