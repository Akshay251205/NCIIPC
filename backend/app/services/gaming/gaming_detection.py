from dataclasses import dataclass, field


# ============================================================
# Gaming Detection
# ============================================================


@dataclass
class GamingFinding:
    """
    Represents a behavioral pattern that may be
    consistent with potential metric-gaming behavior.

    This is a supervisory signal, not an accusation.
    """

    entity_type: str
    entity_id: str

    score: float

    severity: str

    indicators: list[str] = field(default_factory=list)

    observations: list[str] = field(default_factory=list)

    metrics: dict = field(default_factory=dict)

    confidence: str = "Low"

    def to_dict(self) -> dict:
        return {
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "score": self.score,
            "severity": self.severity,
            "indicators": self.indicators,
            "observations": self.observations,
            "metrics": self.metrics,
            "confidence": self.confidence,
        }


# ============================================================
# Helpers
# ============================================================


def _safe_float(value, default=0.0):

    try:

        if value is None:
            return default

        return float(value)

    except (TypeError, ValueError):

        return default


def _clamp(
    value,
    minimum=0.0,
    maximum=100.0,
):

    return max(
        minimum,
        min(
            maximum,
            value,
        ),
    )


def _severity(score: float) -> str:

    if score >= 70:
        return "HIGH"

    if score >= 40:
        return "MEDIUM"

    return "LOW"


def _confidence(
    total_alerts: int,
    total_investigations: int,
) -> str:

    observations = (
        max(total_alerts, 0)
        + max(total_investigations, 0)
    )

    if observations >= 10:
        return "High"

    if observations >= 3:
        return "Medium"

    return "Low"


# ============================================================
# Core Gaming Detector
# ============================================================


def detect_gaming_behavior(
    *,
    analyst_id: str,

    total_alerts: int = 0,
    closed_alerts: int = 0,

    average_closure_time_minutes=None,

    evidence_review_rate: float = 0.0,

    investigation_evidence_review_rate: float = 0.0,

    total_investigations: int = 0,

    average_queries: float = 0.0,

    average_actions: float = 0.0,

    average_investigation_duration_minutes=None,

    short_note_rate: float = 0.0,

    repeated_note_rate: float = 0.0,
) -> GamingFinding:

    total_alerts = max(
        int(total_alerts or 0),
        0,
    )

    closed_alerts = max(
        int(closed_alerts or 0),
        0,
    )

    total_investigations = max(
        int(total_investigations or 0),
        0,
    )

    average_closure_time_minutes = _safe_float(
        average_closure_time_minutes,
        None,
    )

    average_investigation_duration_minutes = _safe_float(
        average_investigation_duration_minutes,
        None,
    )

    evidence_review_rate = _clamp(
        _safe_float(
            evidence_review_rate
        )
    )

    investigation_evidence_review_rate = _clamp(
        _safe_float(
            investigation_evidence_review_rate
        )
    )

    average_queries = max(
        _safe_float(average_queries),
        0.0,
    )

    average_actions = max(
        _safe_float(average_actions),
        0.0,
    )

    short_note_rate = _clamp(
        _safe_float(short_note_rate)
    )

    repeated_note_rate = _clamp(
        _safe_float(repeated_note_rate)
    )

    score = 0.0

    indicators = []

    observations = []

    # ========================================================
    # Signal 1: Suspiciously fast closure
    # ========================================================

    if (
        closed_alerts > 0
        and average_closure_time_minutes is not None
        and average_closure_time_minutes < 10
    ):

        score += 30

        indicators.append(
            "Suspiciously fast alert closure"
        )

        observations.append(
            "Closed alerts show an unusually short "
            "average closure time."
        )

    # ========================================================
    # Signal 2: Low evidence review
    # ========================================================

    if (
        total_alerts > 0
        and evidence_review_rate < 50
    ):

        score += 20

        indicators.append(
            "Low evidence-review behavior"
        )

        observations.append(
            "A substantial portion of alerts were "
            "closed without recorded evidence review."
        )

    # ========================================================
    # Signal 3: Low investigation evidence review
    # ========================================================

    if (
        total_investigations > 0
        and investigation_evidence_review_rate < 50
    ):

        score += 15

        indicators.append(
            "Low investigation evidence review"
        )

        observations.append(
            "Investigations show limited recorded "
            "evidence-review activity."
        )

    # ========================================================
    # Signal 4: Shallow investigation activity
    # ========================================================

    if (
        total_investigations > 0
        and average_queries < 2
    ):

        score += 15

        indicators.append(
            "Shallow investigation activity"
        )

        observations.append(
            "Investigations contain very few "
            "recorded queries on average."
        )

    if (
        total_investigations > 0
        and average_actions < 2
    ):

        score += 10

        indicators.append(
            "Low investigation action count"
        )

        observations.append(
            "Investigations contain few recorded "
            "actions on average."
        )

    # ========================================================
    # Signal 5: Very short investigations
    # ========================================================

    if (
        total_investigations > 0
        and average_investigation_duration_minutes
        is not None
        and average_investigation_duration_minutes < 10
    ):

        score += 15

        indicators.append(
            "Very short investigations"
        )

        observations.append(
            "Investigation duration is unusually short."
        )

    # ========================================================
    # Signal 6: Short investigation notes
    # ========================================================

    if (
        total_investigations > 0
        and short_note_rate >= 70
    ):

        score += 10

        indicators.append(
            "High short-note rate"
        )

        observations.append(
            "Most investigation notes are unusually short."
        )

    # ========================================================
    # Signal 7: Repeated investigation notes
    # ========================================================

    if (
        total_investigations > 0
        and repeated_note_rate >= 50
    ):

        score += 15

        indicators.append(
            "High repeated-note rate"
        )

        observations.append(
            "Investigation notes contain a high level "
            "of repeated content."
        )

    # ========================================================
    # Combined behavioral pattern
    # ========================================================

    strong_signals = 0

    if (
        closed_alerts > 0
        and average_closure_time_minutes is not None
        and average_closure_time_minutes < 10
    ):
        strong_signals += 1

    if (
        total_investigations > 0
        and average_queries < 2
    ):
        strong_signals += 1

    if (
        total_investigations > 0
        and short_note_rate >= 70
    ):
        strong_signals += 1

    if (
        total_investigations > 0
        and repeated_note_rate >= 50
    ):
        strong_signals += 1

    if strong_signals >= 2:

        score += 10

        indicators.append(
            "Pattern consistent with potential "
            "metric-gaming behavior"
        )

        observations.append(
            "Multiple behavioral signals occur together "
            "and warrant supervisory review."
        )

    score = round(
        _clamp(score),
        2,
    )

    return GamingFinding(
        entity_type="ANALYST",
        entity_id=str(analyst_id),
        score=score,
        severity=_severity(score),
        indicators=indicators,
        observations=observations,
        metrics={
            "total_alerts": total_alerts,
            "closed_alerts": closed_alerts,
            "average_closure_time_minutes":
                average_closure_time_minutes,
            "evidence_review_rate":
                evidence_review_rate,
            "investigation_evidence_review_rate":
                investigation_evidence_review_rate,
            "total_investigations":
                total_investigations,
            "average_queries":
                average_queries,
            "average_actions":
                average_actions,
            "average_investigation_duration_minutes":
                average_investigation_duration_minutes,
            "short_note_rate":
                short_note_rate,
            "repeated_note_rate":
                repeated_note_rate,
            "strong_signals":
                strong_signals,
        },
        confidence=_confidence(
            total_alerts,
            total_investigations,
        ),
    )