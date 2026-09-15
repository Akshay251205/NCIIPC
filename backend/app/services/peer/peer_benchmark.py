from dataclasses import dataclass, field


# ============================================================
# Peer Benchmark Finding
# ============================================================


@dataclass
class PeerBenchmarkFinding:
    """
    Represents an analyst's deviation from a peer baseline.

    A high score means the analyst is behaving differently
    from the selected peer baseline.
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


def _percentage_deviation(
    analyst_value,
    peer_value,
):

    analyst_value = _safe_float(
        analyst_value
    )

    peer_value = _safe_float(
        peer_value
    )

    if peer_value == 0:

        if analyst_value == 0:
            return 0.0

        return 100.0

    return abs(
        (
            analyst_value
            - peer_value
        )
        / peer_value
    ) * 100


def _severity(score):

    if score >= 70:
        return "HIGH"

    if score >= 40:
        return "MEDIUM"

    return "LOW"


def _confidence(
    observations,
):

    observations = max(
        int(observations or 0),
        0,
    )

    if observations >= 10:
        return "High"

    if observations >= 3:
        return "Medium"

    return "Low"


# ============================================================
# Core Peer Benchmark
# ============================================================


def calculate_peer_benchmark(
    *,
    analyst_id: str,

    analyst_metrics: dict,

    peer_metrics: dict,

    peer_observations: int = 0,
) -> PeerBenchmarkFinding:

    indicators = []

    observations = []

    deviations = {}

    # ========================================================
    # Metrics compared against peers
    # ========================================================

    metric_definitions = [
        (
            "average_closure_time_minutes",
            "Closure-time deviation",
        ),
        (
            "evidence_review_rate",
            "Evidence-review deviation",
        ),
        (
            "escalation_rate",
            "Escalation-rate deviation",
        ),
        (
            "average_queries",
            "Investigation-query deviation",
        ),
        (
            "average_actions",
            "Investigation-action deviation",
        ),
        (
            "average_investigation_duration_minutes",
            "Investigation-duration deviation",
        ),
        (
            "short_note_rate",
            "Short-note deviation",
        ),
        (
            "repeated_note_rate",
            "Repeated-note deviation",
        ),
    ]

    for metric_name, label in metric_definitions:

        if metric_name not in analyst_metrics:
            continue

        if metric_name not in peer_metrics:
            continue

        analyst_value = analyst_metrics.get(
            metric_name
        )

        peer_value = peer_metrics.get(
            metric_name
        )

        if (
            analyst_value is None
            or peer_value is None
        ):
            continue

        deviation = _percentage_deviation(
            analyst_value,
            peer_value,
        )

        deviations[metric_name] = round(
            deviation,
            2,
        )

        # ----------------------------------------------------
        # Significant peer deviation
        # ----------------------------------------------------

        if deviation >= 50:

            indicators.append(label)

            observations.append(
                f"{metric_name} differs from "
                f"the peer baseline by "
                f"{round(deviation, 2)}%."
            )

    # ========================================================
    # Convert deviations into score
    # ========================================================

    if deviations:

        average_deviation = (
            sum(deviations.values())
            / len(deviations)
        )

        score = _clamp(
            average_deviation
        )

    else:

        score = 0.0

    # ========================================================
    # Multiple deviations bonus
    # ========================================================

    if len(indicators) >= 3:

        score += 15

    elif len(indicators) >= 2:

        score += 10

    score = round(
        _clamp(score),
        2,
    )

    return PeerBenchmarkFinding(
        entity_type="ANALYST",
        entity_id=str(analyst_id),
        score=score,
        severity=_severity(score),
        indicators=indicators,
        observations=observations,
        metrics={
            "analyst_metrics": analyst_metrics,
            "peer_metrics": peer_metrics,
            "deviations": deviations,
            "average_deviation": round(
                (
                    sum(deviations.values())
                    / len(deviations)
                )
                if deviations
                else 0.0,
                2,
            ),
            "peer_observations": (
                peer_observations
            ),
        },
        confidence=_confidence(
            peer_observations
        ),
    )


# ============================================================
# Simple batch helper
# ============================================================


def calculate_peer_benchmarks(
    records: list[dict],
) -> list[dict]:

    results = []

    for record in records:

        analyst_id = record.get(
            "analyst_id"
        )

        if not analyst_id:
            continue

        finding = calculate_peer_benchmark(
            analyst_id=analyst_id,
            analyst_metrics=record.get(
                "analyst_metrics",
                {},
            ),
            peer_metrics=record.get(
                "peer_metrics",
                {},
            ),
            peer_observations=record.get(
                "peer_observations",
                0,
            ),
        )

        results.append(
            finding.to_dict()
        )

    return results