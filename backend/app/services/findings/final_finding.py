from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class FinalSupervisoryFinding:
    """
    Stable Team 2 intelligence contract.

    This object is intentionally independent from FastAPI,
    SQLAlchemy, and frontend-specific models.
    """

    entity_type: str
    entity_id: str

    risk_score: float
    risk_level: str
    risk_severity: str
    confidence: str

    primary_indicators: list[str] = field(
        default_factory=list
    )

    explanation: str = ""

    intelligence: dict[str, Any] = field(
        default_factory=dict
    )

    evidence: dict[str, Any] = field(
        default_factory=dict
    )

    supervisory_actions: list[str] = field(
        default_factory=list
    )

    status: str = "complete"

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "risk_score": self.risk_score,
            "risk_level": self.risk_level,
            "risk_severity": self.risk_severity,
            "confidence": self.confidence,
            "primary_indicators": self.primary_indicators,
            "explanation": self.explanation,
            "intelligence": self.intelligence,
            "evidence": self.evidence,
            "supervisory_actions": self.supervisory_actions,
            "status": self.status,
        }


def _safe_float(
    value: Any,
    default: float = 0.0,
) -> float:
    try:
        if value is None:
            return default

        return float(value)

    except (TypeError, ValueError):
        return default


def _clamp(
    value: float,
    minimum: float = 0.0,
    maximum: float = 100.0,
) -> float:
    return max(
        minimum,
        min(maximum, value),
    )


def _round(value: float) -> float:
    return round(
        _clamp(value),
        2,
    )


def _unique_strings(
    values: list[Any],
) -> list[str]:
    result: list[str] = []

    for value in values:
        if not value:
            continue

        value = str(value)

        if value not in result:
            result.append(value)

    return result


def _risk_actions(
    *,
    risk_level: str,
    indicators: list[str],
) -> list[str]:
    """
    Generate supervisory actions from the final risk level.

    These are recommendations, not automated enforcement actions.
    """

    level = str(
        risk_level or "LOW"
    ).upper()

    if level == "CRITICAL":
        actions = [
            "Immediate supervisory review",
            "Validate investigation evidence and analyst activity",
            "Review affected alerts and investigations",
        ]

    elif level == "HIGH":
        actions = [
            "Prioritized supervisory review",
            "Validate investigation depth and evidence handling",
            "Review supporting alerts and investigations",
        ]

    elif level == "MEDIUM":
        actions = [
            "Monitor analyst behavior for recurring patterns",
            "Review supporting intelligence indicators",
        ]

    else:
        actions = [
            "Continue routine supervisory monitoring",
        ]

    if indicators:
        actions.append(
            "Review the identified intelligence indicators"
        )

    return _unique_strings(actions)


def _extract_risk(
    analyst_result: dict[str, Any],
) -> dict[str, Any]:
    risk = analyst_result.get(
        "risk",
        {},
    )

    if not isinstance(
        risk,
        dict,
    ):
        return {}

    return risk


def _extract_layer(
    analyst_result: dict[str, Any],
    name: str,
) -> dict[str, Any]:
    value = analyst_result.get(
        name,
        {},
    )

    if not isinstance(
        value,
        dict,
    ):
        return {}

    return value


def _extract_indicators(
    layer: dict[str, Any],
) -> list[str]:
    indicators = layer.get(
        "indicators",
        [],
    )

    if not isinstance(
        indicators,
        list,
    ):
        return []

    return [
        str(indicator)
        for indicator in indicators
        if indicator
    ]


def build_final_finding(
    analyst_result: dict[str, Any],
) -> FinalSupervisoryFinding:
    """
    Convert one complete analyst intelligence result
    into the stable final supervisory finding contract.
    """

    analyst_id = str(
        analyst_result.get(
            "analyst_id",
            "",
        )
    )

    risk = _extract_risk(
        analyst_result
    )

    dna = _extract_layer(
        analyst_result,
        "investigation_dna",
    )

    gaming = _extract_layer(
        analyst_result,
        "gaming",
    )

    peer = _extract_layer(
        analyst_result,
        "peer_benchmark",
    )

    anomaly = _extract_layer(
        analyst_result,
        "behavioral_anomaly",
    )

    nlp = _extract_layer(
        analyst_result,
        "investigation_nlp",
    )

    negative_space = analyst_result.get(
        "negative_space"
    )

    if not isinstance(
        negative_space,
        dict,
    ):
        negative_space = {}

    indicators: list[str] = []

    for layer in [
        risk,
        dna,
        gaming,
        peer,
        anomaly,
        nlp,
        negative_space,
    ]:
        indicators.extend(
            _extract_indicators(layer)
        )

    indicators = _unique_strings(
        indicators
    )

    risk_score = _round(
        _safe_float(
            risk.get("score")
        )
    )

    risk_level = str(
        risk.get(
            "level",
            "LOW",
        )
    ).upper()

    risk_severity = str(
        risk.get(
            "severity",
            risk_level,
        )
    ).upper()

    confidence = str(
        risk.get(
            "confidence",
            "Low",
        )
    )

    explanation = str(
        risk.get(
            "explanation",
            (
                "No detailed risk explanation "
                "was provided."
            ),
        )
    )

    intelligence = {
        "investigation_dna": {
            "quality_score": _round(
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
            "score": _round(
                _safe_float(
                    gaming.get("score")
                )
            ),
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
        "peer_benchmark": {
            "score": _round(
                _safe_float(
                    peer.get("score")
                )
            ),
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
            "score": _round(
                _safe_float(
                    anomaly.get("score")
                )
            ),
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
        "investigation_nlp": {
            "average_score": _round(
                _safe_float(
                    nlp.get("average_score")
                )
            ),
            "high_findings": int(
                _safe_float(
                    nlp.get(
                        "high_findings"
                    )
                )
            ),
            "medium_findings": int(
                _safe_float(
                    nlp.get(
                        "medium_findings"
                    )
                )
            ),
            "investigations_analyzed": int(
                _safe_float(
                    nlp.get(
                        "investigations_analyzed"
                    )
                )
            ),
            "indicators": _extract_indicators(
                nlp
            ),
        },
        "negative_space": (
            {
                "score": _round(
                    _safe_float(
                        negative_space.get(
                            "score"
                        )
                    )
                ),
                "severity": negative_space.get(
                    "severity",
                    "LOW",
                ),
                "confidence": negative_space.get(
                    "confidence",
                    "Low",
                ),
                "indicators": (
                    _extract_indicators(
                        negative_space
                    )
                ),
            }
            if negative_space
            else None
        ),
    }

    evidence = {
        "data_quality": analyst_result.get(
            "data_quality",
            {},
        ),
        "alerts": analyst_result.get(
            "alerts",
            {},
        ),
        "investigations": analyst_result.get(
            "investigations",
            {},
        ),
        "performance": analyst_result.get(
            "performance",
            {},
        ),
        "risk_components": risk.get(
            "components",
            {},
        ),
        "risk_signals": risk.get(
            "signals",
            [],
        ),
    }

    supervisory_actions = _risk_actions(
        risk_level=risk_level,
        indicators=indicators,
    )

    return FinalSupervisoryFinding(
        entity_type="analyst",
        entity_id=analyst_id,
        risk_score=risk_score,
        risk_level=risk_level,
        risk_severity=risk_severity,
        confidence=confidence,
        primary_indicators=indicators,
        explanation=explanation,
        intelligence=intelligence,
        evidence=evidence,
        supervisory_actions=supervisory_actions,
        status="complete",
    )


def build_final_findings(
    analyst_results: list[dict[str, Any]],
) -> list[FinalSupervisoryFinding]:
    """
    Build final findings for all analyst results.
    """

    if not isinstance(
        analyst_results,
        list,
    ):
        return []

    findings: list[
        FinalSupervisoryFinding
    ] = []

    for analyst_result in analyst_results:
        if not isinstance(
            analyst_result,
            dict,
        ):
            continue

        findings.append(
            build_final_finding(
                analyst_result
            )
        )

    return findings


def build_final_finding_dict(
    analyst_result: dict[str, Any],
) -> dict[str, Any]:
    """
    Dictionary interface for API/service consumers.
    """

    return build_final_finding(
        analyst_result
    ).to_dict()


def build_final_finding_dicts(
    analyst_results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Dictionary interface for multiple analysts.
    """

    return [
        finding.to_dict()
        for finding in build_final_findings(
            analyst_results
        )
    ]