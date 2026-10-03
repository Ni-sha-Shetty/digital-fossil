import json
import logging
from typing import Dict, Any, List
from app.config import settings

logger = logging.getLogger("digital_fossil.explanation")

def build_evidence_package(
    observed_facts: List[Any],
    inferences: List[Any],
    hypotheses: List[Any],
    missing_evidence: List[Any],
    conflicting_evidence: List[Any],
    confidence: float
) -> Dict[str, Any]:
    """
    Constructs a strictly sanitized, structured evidence package.
    No uncontrolled raw blobs or credentials.
    """
    return {
        "observed_facts": [
            {"id": f.id, "event_id": f.event_id, "statement": f.statement, "timestamp": str(f.timestamp)}
            for f in observed_facts[:15]
        ],
        "inferences": [
            {"id": inf.id, "statement": inf.statement, "score": inf.correlation_score, "evidence_ids": inf.supporting_evidence_ids}
            for inf in inferences[:10]
        ],
        "hypotheses": [
            {
                "id": h.id,
                "text": h.hypothesis_text,
                "confidence": h.confidence,
                "uncertainty": h.uncertainty_statement,
                "supporting_evidence": h.supporting_evidence_ids,
                "contradicting_evidence": h.contradicting_evidence_ids
            }
            for h in hypotheses
        ],
        "missing_information": [
            {"id": m.id, "description": m.description, "significance": m.significance}
            for m in missing_evidence
        ],
        "conflicting_information": [
            {"id": c.id, "description": c.description, "type": c.conflict_type}
            for c in conflicting_evidence
        ],
        "overall_confidence": confidence
    }

def generate_deterministic_explanation(evidence_package: Dict[str, Any]) -> str:
    """
    Generates a rigorous, human-readable forensic explanation strictly based on verified evidence
    and cautious inference. Used when no LLM API key is present or on API timeout.
    """
    facts = evidence_package.get("observed_facts", [])
    infs = evidence_package.get("inferences", [])
    hyps = evidence_package.get("hypotheses", [])
    missing = evidence_package.get("missing_information", [])
    conflicts = evidence_package.get("conflicting_information", [])
    confidence = evidence_package.get("overall_confidence", 0.5)

    paragraphs = []
    
    # 1. Executive Summary
    conf_pct = int(confidence * 100)
    paragraphs.append(
        f"**Activity Reconstruction Summary (Evidence Confidence: {conf_pct}%)**\n"
        f"The system recorded {len(facts)} directly observed filesystem/process facts and derived "
        f"{len(infs)} correlated relationship(s)."
    )

    # 2. Key Hypothesis
    if hyps:
        primary = hyps[0]
        paragraphs.append(
            f"**Primary Hypothesis ({primary.get('id', 'HYP-01')}):**\n"
            f"{primary.get('text')}\n\n"
            f"*Supporting Evidence:* {', '.join(primary.get('supporting_evidence', [])) or 'Observed session cluster'}.\n"
            f"*Key Uncertainty:* {primary.get('uncertainty')}"
        )

    # 3. Inferred Relationships
    if infs:
        inf_lines = [f"• **{inf['id']}:** {inf['statement']}" for inf in infs[:4]]
        paragraphs.append("**Correlated Inferences:**\n" + "\n".join(inf_lines))

    # 4. Unknowns & Critical Missing Evidence
    if missing:
        miss_lines = [f"• **{m['id']}:** {m['description']} ({m['significance']})" for m in missing]
        paragraphs.append("**Identified Missing Evidence (Gaps in Chain of Custody):**\n" + "\n".join(miss_lines))

    # 5. Conflicting Data
    if conflicts:
        conf_lines = [f"• **{c['id']}:** {c['description']}" for c in conflicts]
        paragraphs.append("**Conflicting Indicators:**\n" + "\n".join(conf_lines))

    paragraphs.append(
        "_Note: This explanation distinguishes confirmed event logs from derived possibilities. "
        "No unrecorded intermediate actions are claimed as fact._"
    )

    return "\n\n".join(paragraphs)

def generate_explainable_narrative(evidence_package: Dict[str, Any]) -> str:
    """
    Dispatches to optional LLM if an API key is configured; otherwise uses deterministic engine.
    """
    api_key = settings.LLM_API_KEY
    if not api_key:
        return generate_deterministic_explanation(evidence_package)

    try:
        # If an API key is available, call via httpx with strict instructions
        import httpx
        system_prompt = (
            "You are an expert digital forensics assistant. Analyze the structured evidence package below.\n"
            "STRICT RULES:\n"
            "1. NEVER invent events, filenames, timestamps, or processes not in the package.\n"
            "2. Distinguish OBSERVED FACTS from INFERRED RELATIONSHIPS and HYPOTHESES.\n"
            "3. State UNKNOWNS and MISSING EVIDENCE explicitly.\n"
            "4. Use cautious forensic terminology ('evidence suggests', 'may indicate', 'insufficient evidence to prove').\n"
            "5. Cite evidence IDs (e.g. FACT-001, INF-001, MISS-001).\n"
            "6. Keep output concise (under 250 words)."
        )
        # Attempt Gemini or OpenAI standard endpoint
        if settings.LLM_PROVIDER.lower() == "gemini" or "AIza" in api_key:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            payload = {
                "contents": [{
                    "parts": [{"text": f"{system_prompt}\n\nEvidence Package:\n{json.dumps(evidence_package, indent=2)}"}]
                }]
            }
            with httpx.Client(timeout=10.0) as client:
                resp = client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text")
                        if text:
                            return text
        logger.warning("LLM API call did not succeed, falling back to deterministic explanation.")
    except Exception as e:
        logger.warning(f"Error querying external LLM: {e}. Falling back to deterministic explanation.")

    return generate_deterministic_explanation(evidence_package)
