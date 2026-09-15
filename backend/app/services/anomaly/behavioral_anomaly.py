from dataclasses import dataclass, field
from statistics import median
from typing import Any


@dataclass
class BehavioralAnomalyFinding:
    """
    Explainable behavioral anomaly result for one analyst.
    """

    entity_type: str
    entity_id: str
    score: float
    severity: str
    confidence: str
    indicators: list[str] = field(default_factory=list)
    observations: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "score": self.score,
            "severity": self.severity,
            "confidence": self.confidence,
            "indicators": self.indicators,
            "observations": self.observations,
            "metrics": self.metrics,
        }


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _clamp(
    value: float,
    minimum: float = 0.0,
    maximum: float = 100.0,
) -> float:
    return max(minimum, min(value, maximum))


def _round(value: float) -> float:
    return round(value, 2)


def _median_absolute_deviation(
    values: list[float],
    center: float | None = None,
) -> float:
    """
    Calculate MAD.

    `center` can be supplied so the population median is not
    recalculated repeatedly.
    """

    if not values:
        return 0.0

    if center is None:
        center = median(values)

    deviations = [
        abs(value - center)
        for value in values
    ]

    return median(deviations)


def _robust_deviation_from_stats(
    value: float,
    center: float,
    mad: float,
) -> float:
    """
    Calculate robust deviation using precomputed population
    statistics.
    """

    if mad > 0:
        return abs(value - center) / mad

    if center == 0:
        return 0.0 if value == 0 else 1.0

    return abs(value - center) / abs(center)


def _anomaly_contribution(
    robust_deviation: float,
) -> float:

    if robust_deviation < 0.50:
        return 0.0

    if robust_deviation < 1:
        return 40.0

    if robust_deviation < 2:
        return 60.0

    if robust_deviation < 3:
        return 80.0

    return 100.0


def _confidence(
    observation_count: int,
    dimensions_observed: int,
) -> str:

    if observation_count >= 10 and dimensions_observed >= 3:
        return "High"

    if observation_count >= 3 and dimensions_observed >= 2:
        return "Medium"

    return "Low"


def prepare_population_statistics(
    population_metrics: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """
    Calculate population values, median and MAD ONCE.

    This is the key performance optimization.

    Old behavior:
        every analyst -> every metric -> scan population

    New behavior:
        population -> metric -> calculate statistics once
    """

    supported_metrics = (
        "average_closure_time_minutes",
        "evidence_review_rate",
        "escalation_rate",
        "false_positive_rate",
        "average_queries",
        "average_actions",
        "average_investigation_duration_minutes",
        "short_note_rate",
        "repeated_note_rate",
    )

    statistics: dict[str, dict[str, Any]] = {}

    for metric_name in supported_metrics:

        values = []

        for record in population_metrics:
            value = _safe_float(
                record.get(metric_name)
            )

            if value is not None:
                values.append(value)

        if len(values) < 3:
            continue

        center = median(values)

        mad = _median_absolute_deviation(
            values,
            center=center,
        )

        statistics[metric_name] = {
            "values_count": len(values),
            "median": center,
            "mad": mad,
        }

    return statistics


def detect_behavioral_anomaly(
    *,
    analyst_id: str,
    analyst_metrics: dict[str, Any],
    population_metrics: list[dict[str, Any]] | None = None,
    observation_count: int = 0,
    population_statistics: dict[str, dict[str, Any]] | None = None,
) -> BehavioralAnomalyFinding:
    """
    Detect whether an analyst behaves unusually compared
    with the analyst population.

    Population statistics are prepared once per invocation.
    """

    indicators: list[str] = []
    observations: list[str] = []
    metric_results: dict[str, Any] = {}

    deviations: list[float] = []

    dimensions = [
        (
            "average_closure_time_minutes",
            "Unusual closure-time behavior",
        ),
        (
            "evidence_review_rate",
            "Unusual evidence-review behavior",
        ),
        (
            "escalation_rate",
            "Unusual escalation behavior",
        ),
        (
            "false_positive_rate",
            "Unusual false-positive behavior",
        ),
        (
            "average_queries",
            "Unusual investigation-query behavior",
        ),
        (
            "average_actions",
            "Unusual investigation-action behavior",
        ),
        (
            "average_investigation_duration_minutes",
            "Unusual investigation-duration behavior",
        ),
        (
            "short_note_rate",
            "Unusual short-note behavior",
        ),
        (
            "repeated_note_rate",
            "Unusual repeated-note behavior",
        ),
    ]

    # ----------------------------------------------------------
    # IMPORTANT:
    # Calculate population statistics once.
    # ----------------------------------------------------------

    if population_statistics is None:
        population_statistics = prepare_population_statistics(
            population_metrics or []
        )

    # ----------------------------------------------------------
    # Evaluate this analyst against cached statistics.
    # ----------------------------------------------------------

    for metric_name, indicator_text in dimensions:

        analyst_value = _safe_float(
            analyst_metrics.get(metric_name)
        )

        if analyst_value is None:
            continue

        stats = population_statistics.get(metric_name)

        if stats is None:
            continue

        center = stats["median"]
        mad = stats["mad"]
        population_count = stats["values_count"]

        deviation = _robust_deviation_from_stats(
            analyst_value,
            center,
            mad,
        )

        contribution = _anomaly_contribution(
            deviation
        )

        if contribution > 0:
            deviations.append(contribution)

        metric_results[metric_name] = {
            "analyst_value": _round(analyst_value),
            "population_median": _round(center),
            "population_observations": population_count,
            "robust_deviation": _round(deviation),
            "anomaly_contribution": _round(contribution),
        }

        if deviation >= 0.50:

            indicators.append(
                indicator_text
            )

            direction = (
                "above"
                if analyst_value > center
                else "below"
            )

            observations.append(
                f"{metric_name} is {direction} "
                f"the population median "
                f"({analyst_value:.2f} vs "
                f"{center:.2f})."
            )

    # ----------------------------------------------------------
    # Overall score
    # ----------------------------------------------------------

    if deviations:
        score = sum(deviations) / len(deviations)
    else:
        score = 0.0

    strong_anomalies = sum(
        1
        for contribution in deviations
        if contribution >= 75
    )

    if strong_anomalies >= 3:
        score += 15.0

    elif strong_anomalies >= 2:
        score += 10.0

    score = _clamp(score)

    # ----------------------------------------------------------
    # Severity
    # ----------------------------------------------------------

    if score >= 70:
        severity = "HIGH"

    elif score >= 40:
        severity = "MEDIUM"

    else:
        severity = "LOW"

    # ----------------------------------------------------------
    # Confidence
    # ----------------------------------------------------------

    confidence = _confidence(
        observation_count,
        len(metric_results),
    )

    # ----------------------------------------------------------
    # Observations
    # ----------------------------------------------------------

    if not indicators:

        observations.append(
            "No strong behavioral deviation was detected "
            "across the available analyst metrics."
        )

    else:

        observations.insert(
            0,
            "Behavioral pattern differs materially from "
            "the observed analyst population and warrants "
            "supervisory review."
        )

    return BehavioralAnomalyFinding(
        entity_type="analyst",
        entity_id=str(analyst_id),
        score=_round(score),
        severity=severity,
        confidence=confidence,
        indicators=indicators,
        observations=observations,
        metrics=metric_results,
    )


def calculate_population_metrics(
    analyst_records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Normalize analyst records for anomaly comparison.
    """

    supported_metrics = {
        "average_closure_time_minutes",
        "evidence_review_rate",
        "escalation_rate",
        "false_positive_rate",
        "average_queries",
        "average_actions",
        "average_investigation_duration_minutes",
        "short_note_rate",
        "repeated_note_rate",
    }

    population = []

    for record in analyst_records:

        normalized = {}

        for metric_name in supported_metrics:

            if metric_name in record:
                normalized[metric_name] = record[
                    metric_name
                ]

        performance = record.get(
            "performance",
            {},
        )

        investigations = record.get(
            "investigations",
            {},
        )

        normalized.setdefault(
            "average_closure_time_minutes",
            performance.get(
                "average_closure_time_minutes"
            ),
        )

        normalized.setdefault(
            "evidence_review_rate",
            performance.get(
                "evidence_review_rate"
            ),
        )

        normalized.setdefault(
            "escalation_rate",
            performance.get(
                "escalation_rate"
            ),
        )

        normalized.setdefault(
            "false_positive_rate",
            performance.get(
                "false_positive_rate"
            ),
        )

        normalized.setdefault(
            "average_queries",
            investigations.get(
                "average_queries"
            ),
        )

        normalized.setdefault(
            "average_actions",
            investigations.get(
                "average_actions"
            ),
        )

        normalized.setdefault(
            "average_investigation_duration_minutes",
            investigations.get(
                "average_duration_minutes"
            ),
        )

        population.append(normalized)

    return population
