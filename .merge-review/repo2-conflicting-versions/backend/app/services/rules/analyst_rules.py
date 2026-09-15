"""
Backward-compatible analyst rule evaluation.

The actual rule implementations live in:

    rule_engine.py

This wrapper keeps the existing SAT-SA analytics code working.
"""

from typing import Any

from app.services.rules.rule_engine import RuleEngine


def evaluate_analyst_behavior(
    *,
    total_alerts: int,
    closed_alerts: int,
    avg_closure_time: float | None,
    evidence_review_rate: float,
    escalation_rate: float,
    total_investigations: int,
    avg_queries: float,
    avg_investigation_time: float | None,

    # New optional intelligence fields.
    short_note_rate: float = 0.0,
    repeated_note_rate: float = 0.0,
    analyst_id: str = "UNKNOWN",
) -> dict[str, Any]:
    """
    Evaluate analyst behavior using the SAT-SA Rule Engine.

    Existing callers can continue using the original arguments.

    New callers can additionally provide:
        short_note_rate
        repeated_note_rate
        analyst_id
    """

    features = {
        "analyst_id": analyst_id,

        "total_alerts": total_alerts,

        "closed_alerts": closed_alerts,

        "average_closure_time_minutes": (
            avg_closure_time
        ),

        "evidence_review_rate": (
            evidence_review_rate
        ),

        "escalation_rate": (
            escalation_rate
        ),

        "total_investigations": (
            total_investigations
        ),

        "average_queries": (
            avg_queries
        ),

        "average_investigation_duration_minutes": (
            avg_investigation_time
        ),

        "short_note_rate": (
            short_note_rate
        ),

        "repeated_note_rate": (
            repeated_note_rate
        ),
    }

    engine = RuleEngine()

    result = engine.summary(
        features
    )

    # --------------------------------------------------------------
    # Preserve the old return format.
    #
    # analyst_metrics.py already expects:
    #
    #     score
    #     level
    #     confidence
    #     indicators
    # --------------------------------------------------------------

    score = result["score"]

    if score >= 70:
        level = "High"

    elif score >= 40:
        level = "Medium"

    else:
        level = "Low"

    return {
        "score": score,

        "level": level,

        "severity": result["severity"],

        "confidence": result["confidence"],

        "indicators": result["indicators"],

        "triggered_rules": result[
            "triggered_rules"
        ],

        "signals": result[
            "signals"
        ],
    }