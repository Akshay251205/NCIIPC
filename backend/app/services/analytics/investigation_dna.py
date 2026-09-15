"""
SAT-SA Investigation DNA.

Investigation DNA creates a behavioral fingerprint for an analyst.

It does NOT determine whether an analyst is malicious.

Instead, it summarizes observable investigation behavior:

    - Evidence discipline
    - Investigation depth
    - Escalation discipline
    - Closure behavior
    - Note quality
    - Overall investigation quality

The output is deterministic, explainable and suitable for later use by:

    Rule Engine
    Behavioral Analytics
    Gaming Detection
    Finding Engine
    Risk Engine
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


# ============================================================================
# 1. HELPER FUNCTIONS
# ============================================================================


def _safe_float(
    value: Any,
    default: float = 0.0,
) -> float:
    """
    Safely convert a value to float.

    If the value is None or invalid, return the default.
    """

    if value is None:
        return default

    try:
        return float(value)

    except (
        TypeError,
        ValueError,
    ):
        return default


def _clamp(
    value: float,
    minimum: float = 0.0,
    maximum: float = 100.0,
) -> float:
    """
    Keep a score inside a safe range.

    Example:

        _clamp(120) -> 100
        _clamp(-10) -> 0
    """

    return max(
        minimum,
        min(
            value,
            maximum,
        ),
    )


def _round_score(
    value: float,
) -> float:
    """
    Round a score to two decimal places
    and keep it between 0 and 100.
    """

    return round(
        _clamp(value),
        2,
    )


def _percentage_to_score(
    percentage: Any,
) -> float:
    """
    Convert a percentage directly into a 0-100 score.

    Example:

        80% -> 80
        25% -> 25
    """

    return _round_score(
        _safe_float(percentage)
    )


# ============================================================================
# 2. INVESTIGATION DNA DATA MODEL
# ============================================================================


@dataclass
class InvestigationDNA:
    """
    Behavioral fingerprint of one analyst.

    All *_score fields use:

        0   = weak observed behavior
        100 = strong observed behavior

    Important:

        This is a QUALITY profile.

        Therefore a high quality_score is GOOD.

        It should not be confused with a risk score,
        where a high score means MORE RISK.
    """

    analyst_id: str

    evidence_discipline_score: float

    investigation_depth_score: float

    escalation_discipline_score: float

    closure_behavior_score: float

    note_quality_score: float

    investigation_quality_score: float

    confidence: str

    observations: int

    indicators: list[str]

    metrics: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the DNA object into a JSON-friendly dictionary.
        """

        return asdict(self)


# ============================================================================
# 3. EVIDENCE DISCIPLINE
# ============================================================================


def calculate_evidence_discipline(
    *,
    alert_evidence_review_rate: float,
    investigation_evidence_review_rate: float,
    total_alerts: int,
    total_investigations: int,
) -> float:
    """
    Calculate Evidence Discipline Score.

    We use both:

        alert evidence-review rate
        investigation evidence-review rate

    If investigations exist, they receive equal importance.

    If there are no investigations, we use the alert rate.

    This score is intentionally transparent.
    """

    alert_score = _percentage_to_score(
        alert_evidence_review_rate
    )

    investigation_score = _percentage_to_score(
        investigation_evidence_review_rate
    )

    if total_investigations > 0:

        score = (
            alert_score * 0.50
            + investigation_score * 0.50
        )

    else:

        score = alert_score

    return _round_score(score)


# ============================================================================
# 4. INVESTIGATION DEPTH
# ============================================================================


def calculate_investigation_depth(
    *,
    average_queries: float,
    average_actions: float,
    average_duration_minutes: float | None,
    total_investigations: int,
) -> float:
    """
    Calculate Investigation Depth Score.

    We combine:

        Query activity
        Action activity
        Investigation duration

    Transparent v1 reference points:

        5 queries      = full query-depth score
        3 actions      = full action-depth score
        45 minutes     = full duration-depth score

    These are not hard requirements.

    They simply prevent a large number from making
    the score exceed 100.
    """

    if total_investigations <= 0:
        return 0.0

    # --------------------------------------------------------------
    # Query depth
    # --------------------------------------------------------------

    query_score = _clamp(
        (
            _safe_float(
                average_queries
            )
            / 5.0
        )
        * 100
    )

    # --------------------------------------------------------------
    # Action depth
    # --------------------------------------------------------------

    action_score = _clamp(
        (
            _safe_float(
                average_actions
            )
            / 3.0
        )
        * 100
    )

    # --------------------------------------------------------------
    # Duration depth
    # --------------------------------------------------------------

    duration = _safe_float(
        average_duration_minutes
    )

    duration_score = _clamp(
        (
            duration
            / 45.0
        )
        * 100
    )

    # --------------------------------------------------------------
    # Final depth score
    # --------------------------------------------------------------

    score = (
        query_score * 0.40
        + action_score * 0.30
        + duration_score * 0.30
    )

    return _round_score(score)


# ============================================================================
# 5. ESCALATION DISCIPLINE
# ============================================================================


def calculate_escalation_discipline(
    *,
    alert_escalation_rate: float,
    investigation_escalation_rate: float,
    total_alerts: int,
    total_investigations: int,
) -> float:
    """
    Calculate Escalation Discipline Score.

    IMPORTANT:

    Escalation is context-dependent.

    A low escalation rate does NOT automatically mean
    poor analyst behavior.

    Therefore this score is deliberately conservative.

    We use the observed escalation rate as a behavioral
    signal rather than declaring low escalation "bad".
    """

    alert_rate = _safe_float(
        alert_escalation_rate
    )

    investigation_rate = _safe_float(
        investigation_escalation_rate
    )

    if (
        total_alerts > 0
        and total_investigations > 0
    ):

        score = (
            alert_rate * 0.50
            + investigation_rate * 0.50
        )

    elif total_alerts > 0:

        score = alert_rate

    elif total_investigations > 0:

        score = investigation_rate

    else:

        score = 0.0

    return _round_score(score)


# ============================================================================
# 6. CLOSURE BEHAVIOR
# ============================================================================


def calculate_closure_behavior(
    *,
    average_closure_time_minutes: float | None,
    closed_alerts: int,
) -> float:
    """
    Calculate Closure Behavior Score.

    We want to avoid treating extremely fast closure
    as excellent behavior.

    Transparent v1 interpretation:

        < 10 min
            suspiciously fast -> low score

        10-20 min
            fast but potentially reasonable -> medium score

        20-120 min
            broad acceptable operating range -> high score

        > 120 min
            potentially slow -> reduced score

    This is a behavioral baseline, not proof of poor performance.
    """

    if closed_alerts <= 0:
        return 0.0

    if average_closure_time_minutes is None:
        return 0.0

    closure_time = _safe_float(
        average_closure_time_minutes
    )

    if closure_time < 10:

        score = 20.0

    elif closure_time < 20:

        score = 70.0

    elif closure_time <= 120:

        score = 100.0

    else:

        score = 70.0

    return _round_score(score)


# ============================================================================
# 7. NOTE QUALITY
# ============================================================================


def calculate_note_quality(
    *,
    short_note_rate: float,
    repeated_note_rate: float,
    total_investigations: int,
) -> float:
    """
    Calculate Note Quality Score.

    We penalize:

        short notes
        repeated notes

    Short and repeated notes are behavioral signals,
    not proof of misconduct.
    """

    if total_investigations <= 0:
        return 0.0

    short_rate = _clamp(
        _safe_float(
            short_note_rate
        )
    )

    repeated_rate = _clamp(
        _safe_float(
            repeated_note_rate
        )
    )

    # --------------------------------------------------------------
    # Start from perfect quality.
    # --------------------------------------------------------------

    score = 100.0

    # Short notes have a 60% contribution.
    score -= (
        short_rate * 0.60
    )

    # Repeated notes have a 40% contribution.
    score -= (
        repeated_rate * 0.40
    )

    return _round_score(score)


# ============================================================================
# 8. OVERALL INVESTIGATION QUALITY
# ============================================================================


def calculate_investigation_quality(
    *,
    evidence_discipline_score: float,
    investigation_depth_score: float,
    escalation_discipline_score: float,
    closure_behavior_score: float,
    note_quality_score: float,
) -> float:
    """
    Calculate the overall Investigation Quality Score.

    v1 weights:

        Evidence discipline      30%
        Investigation depth      25%
        Escalation discipline    15%
        Closure behavior         10%
        Note quality             20%

    Total:

        30 + 25 + 15 + 10 + 20 = 100%
    """

    score = (
        evidence_discipline_score * 0.30
        + investigation_depth_score * 0.25
        + escalation_discipline_score * 0.15
        + closure_behavior_score * 0.10
        + note_quality_score * 0.20
    )

    return _round_score(score)


# ============================================================================
# 9. CONFIDENCE
# ============================================================================


def calculate_dna_confidence(
    observations: int,
) -> str:
    """
    Determine how much observed activity supports
    the DNA profile.

        0-2 observations  -> Low
        3-9 observations  -> Medium
        10+ observations  -> High
    """

    if observations >= 10:
        return "High"

    if observations >= 3:
        return "Medium"

    return "Low"


# ============================================================================
# 10. BEHAVIORAL INDICATORS
# ============================================================================


def generate_dna_indicators(
    *,
    evidence_discipline_score: float,
    investigation_depth_score: float,
    escalation_discipline_score: float,
    closure_behavior_score: float,
    note_quality_score: float,
) -> list[str]:
    """
    Generate human-readable indicators explaining
    the DNA profile.

    These indicators are intentionally descriptive.
    """

    indicators: list[str] = []

    # --------------------------------------------------------------
    # Evidence
    # --------------------------------------------------------------

    if evidence_discipline_score < 50:

        indicators.append(
            "Low evidence discipline"
        )

    elif evidence_discipline_score >= 80:

        indicators.append(
            "Strong evidence discipline"
        )

    # --------------------------------------------------------------
    # Investigation depth
    # --------------------------------------------------------------

    if investigation_depth_score < 40:

        indicators.append(
            "Shallow investigation depth"
        )

    elif investigation_depth_score >= 80:

        indicators.append(
            "Strong investigation depth"
        )

    # --------------------------------------------------------------
    # Escalation
    # --------------------------------------------------------------

    if (
        escalation_discipline_score > 0
        and escalation_discipline_score < 10
    ):

        indicators.append(
            "Low observed escalation activity"
        )

    elif escalation_discipline_score >= 70:

        indicators.append(
            "High observed escalation activity"
        )

    # --------------------------------------------------------------
    # Closure
    # --------------------------------------------------------------

    if closure_behavior_score < 50:

        indicators.append(
            "Potentially unusual closure behavior"
        )

    elif closure_behavior_score >= 90:

        indicators.append(
            "Stable closure behavior"
        )

    # --------------------------------------------------------------
    # Notes
    # --------------------------------------------------------------

    if note_quality_score < 50:

        indicators.append(
            "Low investigation note quality"
        )

    elif note_quality_score >= 80:

        indicators.append(
            "Strong investigation note quality"
        )

    # --------------------------------------------------------------
    # Default
    # --------------------------------------------------------------

    if not indicators:

        indicators.append(
            "No strong Investigation DNA deviation observed"
        )

    return indicators


# ============================================================================
# 11. BUILD INVESTIGATION DNA
# ============================================================================


def build_investigation_dna(
    features: dict[str, Any],
) -> InvestigationDNA:
    """
    Build an Investigation DNA profile from analyst metrics.

    Expected feature names:

        analyst_id

        total_alerts
        closed_alerts

        evidence_review_rate
        escalation_rate

        total_investigations

        average_queries
        average_actions

        average_investigation_duration_minutes

        investigation_evidence_review_rate
        investigation_escalation_rate

        short_note_rate
        repeated_note_rate

        average_closure_time_minutes
    """

    # ==============================================================
    # Basic identity
    # ==============================================================

    analyst_id = str(
        features.get(
            "analyst_id",
            "UNKNOWN",
        )
    )

    # ==============================================================
    # Basic counts
    # ==============================================================

    total_alerts = int(
        _safe_float(
            features.get(
                "total_alerts",
                0,
            )
        )
    )

    closed_alerts = int(
        _safe_float(
            features.get(
                "closed_alerts",
                0,
            )
        )
    )

    total_investigations = int(
        _safe_float(
            features.get(
                "total_investigations",
                0,
            )
        )
    )

    # ==============================================================
    # Evidence discipline
    # ==============================================================

    evidence_discipline_score = (
        calculate_evidence_discipline(
            alert_evidence_review_rate=_safe_float(
                features.get(
                    "evidence_review_rate",
                    0,
                )
            ),
            investigation_evidence_review_rate=_safe_float(
                features.get(
                    "investigation_evidence_review_rate",
                    0,
                )
            ),
            total_alerts=total_alerts,
            total_investigations=total_investigations,
        )
    )

    # ==============================================================
    # Investigation depth
    # ==============================================================

    investigation_depth_score = (
        calculate_investigation_depth(
            average_queries=_safe_float(
                features.get(
                    "average_queries",
                    0,
                )
            ),
            average_actions=_safe_float(
                features.get(
                    "average_actions",
                    0,
                )
            ),
            average_duration_minutes=features.get(
                "average_investigation_duration_minutes"
            ),
            total_investigations=total_investigations,
        )
    )

    # ==============================================================
    # Escalation discipline
    # ==============================================================

    escalation_discipline_score = (
        calculate_escalation_discipline(
            alert_escalation_rate=_safe_float(
                features.get(
                    "escalation_rate",
                    0,
                )
            ),
            investigation_escalation_rate=_safe_float(
                features.get(
                    "investigation_escalation_rate",
                    0,
                )
            ),
            total_alerts=total_alerts,
            total_investigations=total_investigations,
        )
    )

    # ==============================================================
    # Closure behavior
    # ==============================================================

    closure_behavior_score = (
        calculate_closure_behavior(
            average_closure_time_minutes=features.get(
                "average_closure_time_minutes"
            ),
            closed_alerts=closed_alerts,
        )
    )

    # ==============================================================
    # Note quality
    # ==============================================================

    note_quality_score = (
        calculate_note_quality(
            short_note_rate=_safe_float(
                features.get(
                    "short_note_rate",
                    0,
                )
            ),
            repeated_note_rate=_safe_float(
                features.get(
                    "repeated_note_rate",
                    0,
                )
            ),
            total_investigations=total_investigations,
        )
    )

    # ==============================================================
    # Overall quality
    # ==============================================================

    investigation_quality_score = (
        calculate_investigation_quality(
            evidence_discipline_score=(
                evidence_discipline_score
            ),
            investigation_depth_score=(
                investigation_depth_score
            ),
            escalation_discipline_score=(
                escalation_discipline_score
            ),
            closure_behavior_score=(
                closure_behavior_score
            ),
            note_quality_score=(
                note_quality_score
            ),
        )
    )

    # ==============================================================
    # Observations
    # ==============================================================

    observations = (
        total_alerts
        + total_investigations
    )

    confidence = calculate_dna_confidence(
        observations
    )

    # ==============================================================
    # Indicators
    # ==============================================================

    indicators = generate_dna_indicators(
        evidence_discipline_score=(
            evidence_discipline_score
        ),
        investigation_depth_score=(
            investigation_depth_score
        ),
        escalation_discipline_score=(
            escalation_discipline_score
        ),
        closure_behavior_score=(
            closure_behavior_score
        ),
        note_quality_score=(
            note_quality_score
        ),
    )

    # ==============================================================
    # Raw behavioral metrics
    # ==============================================================

    metrics = {
        "total_alerts": total_alerts,

        "closed_alerts": closed_alerts,

        "total_investigations": (
            total_investigations
        ),

        "average_closure_time_minutes": (
            features.get(
                "average_closure_time_minutes"
            )
        ),

        "evidence_review_rate": (
            features.get(
                "evidence_review_rate",
                0,
            )
        ),

        "investigation_evidence_review_rate": (
            features.get(
                "investigation_evidence_review_rate",
                0,
            )
        ),

        "escalation_rate": (
            features.get(
                "escalation_rate",
                0,
            )
        ),

        "investigation_escalation_rate": (
            features.get(
                "investigation_escalation_rate",
                0,
            )
        ),

        "average_queries": (
            features.get(
                "average_queries",
                0,
            )
        ),

        "average_actions": (
            features.get(
                "average_actions",
                0,
            )
        ),

        "average_investigation_duration_minutes": (
            features.get(
                "average_investigation_duration_minutes"
            )
        ),

        "short_note_rate": (
            features.get(
                "short_note_rate",
                0,
            )
        ),

        "repeated_note_rate": (
            features.get(
                "repeated_note_rate",
                0,
            )
        ),
    }

    # ==============================================================
    # Return DNA
    # ==============================================================

    return InvestigationDNA(
        analyst_id=analyst_id,

        evidence_discipline_score=(
            evidence_discipline_score
        ),

        investigation_depth_score=(
            investigation_depth_score
        ),

        escalation_discipline_score=(
            escalation_discipline_score
        ),

        closure_behavior_score=(
            closure_behavior_score
        ),

        note_quality_score=(
            note_quality_score
        ),

        investigation_quality_score=(
            investigation_quality_score
        ),

        confidence=confidence,

        observations=observations,

        indicators=indicators,

        metrics=metrics,
    )


# ============================================================================
# 12. CONVENIENCE FUNCTION
# ============================================================================


def get_investigation_dna(
    features: dict[str, Any],
) -> dict[str, Any]:
    """
    Build DNA and immediately return a dictionary.

    This is convenient for analytics code.
    """

    dna = build_investigation_dna(
        features
    )

    return dna.to_dict()


# ============================================================================
# 13. CLI DEMO
# ============================================================================


if __name__ == "__main__":

    demo_features = {
        "analyst_id": "AN-DEMO",

        "total_alerts": 20,

        "closed_alerts": 18,

        "average_closure_time_minutes": 35,

        "evidence_review_rate": 90,

        "investigation_evidence_review_rate": 90,

        "escalation_rate": 40,

        "investigation_escalation_rate": 50,

        "total_investigations": 15,

        "average_queries": 5,

        "average_actions": 3,

        "average_investigation_duration_minutes": 45,

        "short_note_rate": 10,

        "repeated_note_rate": 5,
    }

    dna = build_investigation_dna(
        demo_features
    )

    print()
    print("SAT-SA INVESTIGATION DNA")
    print("=" * 70)

    print(
        f"Analyst: {dna.analyst_id}"
    )

    print(
        f"Evidence Discipline: "
        f"{dna.evidence_discipline_score}/100"
    )

    print(
        f"Investigation Depth: "
        f"{dna.investigation_depth_score}/100"
    )

    print(
        f"Escalation Discipline: "
        f"{dna.escalation_discipline_score}/100"
    )

    print(
        f"Closure Behavior: "
        f"{dna.closure_behavior_score}/100"
    )

    print(
        f"Note Quality: "
        f"{dna.note_quality_score}/100"
    )

    print(
        f"Investigation Quality: "
        f"{dna.investigation_quality_score}/100"
    )

    print(
        f"Confidence: "
        f"{dna.confidence}"
    )

    print()
    print("Indicators:")
    print("-" * 70)

    for indicator in dna.indicators:

        print(
            f"- {indicator}"
        )