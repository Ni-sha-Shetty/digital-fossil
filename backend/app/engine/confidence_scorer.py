from typing import Dict, Any, List

def calculate_evidence_confidence(
    correlation_score: float,
    ml_probability: float = 0.5,
    missing_evidence_count: int = 0,
    conflicting_evidence_count: int = 0,
    has_process_link: bool = False,
    time_gap_seconds: float = 0.0
) -> Dict[str, Any]:
    """
    Computes an unpretentious, transparent 'Evidence Confidence' score.
    Does NOT claim absolute statistical certainty.
    Formula:
    Base = (0.65 * Correlation) + (0.35 * ML_Probability)
    Penalties: -0.12 per missing evidence, -0.20 per conflicting evidence, -0.10 if time gap > 90s.
    Bonuses: +0.05 if shared process detected.
    Bounded within [0.05, 0.95].
    """
    w_corr = 0.65
    w_ml = 0.35

    base_score = (w_corr * correlation_score) + (w_ml * ml_probability)
    
    missing_penalty = missing_evidence_count * 0.12
    conflict_penalty = conflicting_evidence_count * 0.20
    time_penalty = 0.10 if time_gap_seconds > 90.0 else 0.0
    
    total_penalties = missing_penalty + conflict_penalty + time_penalty
    total_bonus = 0.05 if has_process_link else 0.0

    raw_confidence = base_score + total_bonus - total_penalties
    
    # Cap confidence: never claim 1.0 (100%) because digital activity reconstruction has inherent uncertainty
    confidence = round(max(0.05, min(0.95, raw_confidence)), 4)

    if confidence >= 0.75:
        label = "HIGH"
        guidance = "Strong evidence convergence across temporal, naming, and structural features."
    elif confidence >= 0.45:
        label = "MEDIUM"
        guidance = "Moderate correlation; suggestive patterns observed but key intermediate steps are unrecorded."
    else:
        label = "LOW"
        guidance = "Weak or conflicting evidence; relationship is speculative or substantially incomplete."

    breakdown = {
        "score": confidence,
        "label": label,
        "guidance": guidance,
        "formula": "Confidence = (0.65 * Correlation) + (0.35 * ML_Prob) + Bonuses - Penalties [bounded (0.05, 0.95)]",
        "components": {
            "correlation_contribution": round(w_corr * correlation_score, 4),
            "ml_contribution": round(w_ml * ml_probability, 4),
            "missing_evidence_penalty": -round(missing_penalty, 4),
            "conflicting_evidence_penalty": -round(conflict_penalty, 4),
            "time_gap_penalty": -round(time_penalty, 4),
            "process_bonus": round(total_bonus, 4)
        }
    }
    return breakdown
