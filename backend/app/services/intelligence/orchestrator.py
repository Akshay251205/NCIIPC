from __future__ import annotations

from typing import Any


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def _clamp(
    value: float,
    minimum: float = 0.0,
    maximum: float = 100.0,
) -> float:
    return max(minimum, min(maximum, value))


def _round(value: float) -> float:
    return round(_clamp(value), 2)


def _deduplicate(values: list[str]) -> list[str]:
    result: list[str] = []

    for value in values:
        if value and value not in result:
            result.append(value)

    return result


def _extract_score(
    finding: dict[str, Any] | None,
    default: float = 0.0,
) -> float:
    if not finding:
        return default

    return _clamp(
        _safe_float(
            finding.get("score"),
            default,
        )
    )


def _extract_indicators(
    finding: dict[str, Any] | None,
) -> list[str]:
    if not finding:
        return []

    indicators = finding.get("indicators", [])

    if not isinstance(indicators, list):
        return []

    return [
        str(indicator)
        for indicator in indicators
        if indicator
    ]


def build_intelligence_context(
    analyst_result: dict[str, Any],
) -> dict[str, Any]:
    """
    Extract the normalized intelligence inputs for one analyst.

    This function does not calculate risk itself. It prepares the
    outputs produced by the individual Team 2 intelligence engines
    for orchestration and downstream risk fusion.
    """

    dna = analyst_result.get(
        "investigation_dna",
        {},
    )

    gaming = analyst_result.get(
        "gaming",
        {},
    )

    peer = analyst_result.get(
        "peer_benchmark",
        {},
    )

    anomaly = analyst_result.get(
        "behavioral_anomaly",
        {},
    )

    nlp = analyst_result.get(
        "investigation_nlp",
        {},
    )

    negative_space = analyst_result.get(
        "negative_space",
        None,
    )

    risk = analyst_result.get(
        "risk",
        {},
    )

    context = {
        "analyst_id": analyst_result.get(
            "analyst_id"
        ),
        "dna": {
            "quality_score": _clamp(
                _safe_float(
                    dna.get(
                        "investigation_quality_score"
                    )
                )
            ),
            "confidence": dna.get(
                "confidence",
                "Low",
            ),
            "indicators": _extract_indicators(
                dna
            ),
        },
        "gaming": {
            "score": _extract_score(gaming),
            "severity": gaming.get(
                "severity",
                "LOW",
            ),
            "confidence": gaming.get(
                "confidence",
                "Low",
            ),
            "indicators": _extract_indicators(
                gaming
            ),
        },
        "peer": {
            "score": _extract_score(peer),
            "severity": peer.get(
                "severity",
                "LOW",
            ),
            "confidence": peer.get(
                "confidence",
                "Low",
            ),
            "indicators": _extract_indicators(
                peer
            ),
        },
        "behavioral_anomaly": {
            "score": _extract_score(anomaly),
            "severity": anomaly.get(
                "severity",
                "LOW",
            ),
            "confidence": anomaly.get(
                "confidence",
                "Low",
            ),
            "indicators": _extract_indicators(
                anomaly
            ),
        },
        "nlp": {
            "score": _clamp(
                _safe_float(
                    nlp.get(
                        "average_score",
                        nlp.get("score", 0.0),
                    )
                )
            ),
            "high_findings": _safe_int(
                nlp.get("high_findings")
            ),
            "medium_findings": _safe_int(
                nlp.get("medium_findings")
            ),
            "investigations_analyzed": _safe_int(
                nlp.get("investigations_analyzed")
            ),
            "indicators": _extract_indicators(
                nlp
            ),
        },
        "negative_space": (
            {
                "score": _extract_score(
                    negative_space
                ),
                "severity": negative_space.get(
                    "severity",
                    "LOW",
                ),
                "confidence": negative_space.get(
                    "confidence",
                    "Low",
                ),
                "indicators": _extract_indicators(
                    negative_space
                ),
            }
            if isinstance(
                negative_space,
                dict,
            )
            else None
        ),
        "existing_risk": risk,
    }

    return context


def collect_intelligence_indicators(
    context: dict[str, Any],
) -> list[str]:
    """
    Collect and deduplicate indicators from all
    available intelligence layers.
    """

    indicators: list[str] = []

    layers = [
        context.get("dna"),
        context.get("gaming"),
        context.get("peer"),
        context.get("behavioral_anomaly"),
        context.get("nlp"),
        context.get("negative_space"),
    ]

    for layer in layers:
        if not isinstance(layer, dict):
            continue

        indicators.extend(
            _extract_indicators(layer)
        )

    return _deduplicate(indicators)


def calculate_intelligence_summary(
    context: dict[str, Any],
) -> dict[str, Any]:
    """
    Produce a compact supervisory summary from all
    available intelligence components.

    This is intentionally descriptive rather than a
    replacement for the Risk Fusion engine.
    """

    dna = context.get("dna", {})
    gaming = context.get("gaming", {})
    peer = context.get("peer", {})
    anomaly = context.get(
        "behavioral_anomaly",
        {},
    )
    nlp = context.get("nlp", {})
    negative_space = context.get(
        "negative_space"
    )

    concern_scores = [
        _extract_score(gaming),
        _extract_score(peer),
        _extract_score(anomaly),
        _extract_score(nlp),
    ]

    if isinstance(
        negative_space,
        dict,
    ):
        concern_scores.append(
            _extract_score(
                negative_space
            )
        )

    active_scores = [
        score
        for score in concern_scores
        if score > 0
    ]

    average_concern = (
        sum(active_scores) / len(active_scores)
        if active_scores
        else 0.0
    )

    highest_concern = (
        max(concern_scores)
        if concern_scores
        else 0.0
    )

    high_signal_count = sum(
        1
        for score in concern_scores
        if score >= 70
    )

    medium_signal_count = sum(
        1
        for score in concern_scores
        if score >= 40
    )

    return {
        "average_concern_score": _round(
            average_concern
        ),
        "highest_concern_score": _round(
            highest_concern
        ),
        "high_signal_count": high_signal_count,
        "medium_or_higher_signal_count": (
            medium_signal_count
        ),
        "investigation_quality_score": _round(
            _safe_float(
                dna.get("quality_score")
            )
        ),
        "indicators": (
            collect_intelligence_indicators(
                context
            )
        ),
    }


def orchestrate_analyst_intelligence(
    analyst_result: dict[str, Any],
) -> dict[str, Any]:
    """
    Orchestrate all available Team 2 intelligence
    outputs for one analyst.

    The orchestrator does not silently invent missing
    intelligence. Missing components remain unavailable.
    """

    context = build_intelligence_context(
        analyst_result
    )

    summary = calculate_intelligence_summary(
        context
    )

    available_layers = [
        "rules",
        "investigation_dna",
        "gaming",
        "peer_benchmark",
        "behavioral_anomaly",
        "investigation_nlp",
    ]

    if context.get(
        "negative_space"
    ) is not None:
        available_layers.append(
            "negative_space"
        )

    return {
        "entity_type": "analyst",
        "entity_id": str(
            context.get(
                "analyst_id",
                "",
            )
        ),
        "status": "complete",
        "available_layers": available_layers,
        "context": context,
        "summary": summary,
    }


def orchestrate_all_analysts(
    analyst_results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Run the intelligence orchestrator across
    all analyst results.
    """

    if not isinstance(
        analyst_results,
        list,
    ):
        return []

    return [
        orchestrate_analyst_intelligence(
            analyst_result
        )
        for analyst_result in analyst_results
        if isinstance(
            analyst_result,
            dict,
        )
    ]