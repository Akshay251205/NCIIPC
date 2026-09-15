from __future__ import annotations

from dataclasses import dataclass, field


# ==============================================================
# Configuration
# ==============================================================

RULE_WEIGHT = 0.40
AI_WEIGHT = 0.30
NEGATIVE_SPACE_WEIGHT = 0.20
PEER_WEIGHT = 0.10


# ==============================================================
# Data structure
# ==============================================================


@dataclass
class RiskFusionFinding:
    entity_type: str
    entity_id: str

    score: float
    level: str
    severity: str
    confidence: str

    components: dict[str, float] = field(default_factory=dict)

    indicators: list[str] = field(default_factory=list)

    signals: list[dict] = field(default_factory=list)

    explanation: str = ""


# ==============================================================
# Helpers
# ==============================================================


def _safe_float(value, default: float = 0.0) -> float:
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
    return max(minimum, min(maximum, value))


def _round(value: float) -> float:
    return round(_clamp(value), 2)


# ==============================================================
# Risk levels
# ==============================================================


def risk_level(score: float) -> str:
    """
    Convert a 0-100 risk score into a supervisory level.
    """

    score = _safe_float(score)

    if score >= 80:
        return "CRITICAL"

    if score >= 60:
        return "HIGH"

    if score >= 40:
        return "MEDIUM"

    return "LOW"


# ==============================================================
# Severity
# ==============================================================


def risk_severity(score: float) -> str:
    """
    Severity follows the same broad supervisory thresholds
    as the risk level.
    """

    return risk_level(score)


# ==============================================================
# Confidence
# ==============================================================


def calculate_risk_confidence(
    *,
    observations: int = 0,
    component_count: int = 0,
    component_confidences: list[str] | None = None,
) -> str:
    """
    Determine confidence using both data volume and
    supporting intelligence components.
    """

    observations = max(int(observations or 0), 0)

    confidences = component_confidences or []

    high_components = sum(
        1
        for confidence in confidences
        if str(confidence).lower() == "high"
    )

    medium_components = sum(
        1
        for confidence in confidences
        if str(confidence).lower() == "medium"
    )

    if observations >= 10 and (
        high_components >= 2
        or component_count >= 4
    ):
        return "High"

    if observations >= 3 and (
        high_components >= 1
        or medium_components >= 1
        or component_count >= 2
    ):
        return "Medium"

    return "Low"


# ==============================================================
# AI / Behavioral fusion
# ==============================================================


def calculate_ai_risk(
    *,
    behavioral_anomaly_score: float | None = None,
    gaming_score: float | None = None,
    nlp_score: float | None = None,
    investigation_dna_quality: float | None = None,
) -> tuple[float, dict[str, float]]:
    """
    Combine AI-derived supervisory signals.

    Internal AI weighting:

        45% behavioral anomaly
        30% gaming
        15% NLP concern
        10% inverse Investigation DNA quality

    Investigation DNA is a QUALITY score where higher is better,
    so it is inverted before being used as a risk signal.

    A value of None means that an AI signal is unavailable. An explicit
    value of 0 is still valid evidence and therefore activates the AI layer.
    """

    anomaly = _clamp(
        _safe_float(behavioral_anomaly_score)
    )

    gaming = _clamp(
        _safe_float(gaming_score)
    )

    nlp = _clamp(
        _safe_float(nlp_score)
    )

    if investigation_dna_quality is None:
        dna_risk = None
    else:
        dna_risk = _clamp(
            100.0 - _safe_float(
                investigation_dna_quality
            )
        )

    components = {
        "behavioral_anomaly": _round(anomaly),
        "gaming": _round(gaming),
        "nlp": _round(nlp),
    }

    weighted_values = [
        (anomaly, 0.45),
        (gaming, 0.30),
        (nlp, 0.15),
    ]

    if dna_risk is not None:
        weighted_values.append(
            (dna_risk, 0.10)
        )
        components["investigation_dna_risk"] = _round(
            dna_risk
        )

    total_weight = sum(
        weight
        for _, weight in weighted_values
    )

    if total_weight <= 0:
        return 0.0, components

    score = sum(
        value * weight
        for value, weight in weighted_values
    ) / total_weight

    return _round(score), components


# ==============================================================
# Main fusion
# ==============================================================


def calculate_risk_fusion(
    *,
    analyst_id: str,
    rule_score: float = 0.0,
    behavioral_anomaly_score: float | None = None,
    gaming_score: float | None = None,
    nlp_score: float | None = None,
    investigation_dna_quality: float | None = None,
    negative_space_score: float | None = None,
    peer_score: float | None = None,
    observations: int = 0,
    component_confidences: list[str] | None = None,
    rule_indicators: list[str] | None = None,
    behavioral_indicators: list[str] | None = None,
    gaming_indicators: list[str] | None = None,
    nlp_indicators: list[str] | None = None,
    negative_space_indicators: list[str] | None = None,
    peer_indicators: list[str] | None = None,
) -> RiskFusionFinding:
    """
    Calculate the final supervisory risk score.

    Primary weights:

        Rule             40%
        AI / Behavioral  30%
        Negative Space   20%
        Peer             10%

    If a component is genuinely unavailable, the remaining
    available components are renormalized rather than
    artificially lowering the analyst's risk score.
    """

    rule_score = _clamp(
        _safe_float(rule_score)
    )

    negative_space_available = (
        negative_space_score is not None
    )

    peer_available = (
        peer_score is not None
    )

    negative_space = (
        _clamp(
            _safe_float(
                negative_space_score
            )
        )
        if negative_space_available
        else 0.0
    )

    peer = (
        _clamp(
            _safe_float(peer_score)
        )
        if peer_available
        else 0.0
    )

    ai_score, ai_components = calculate_ai_risk(
        behavioral_anomaly_score=(
            behavioral_anomaly_score
        ),
        gaming_score=gaming_score,
        nlp_score=nlp_score,
        investigation_dna_quality=(
            investigation_dna_quality
        ),
    )

    # ----------------------------------------------------------
    # Top-level weighted components
    # ----------------------------------------------------------

    # Determine whether the AI/behavioral layer has
    # meaningful evidence available.
    #
    # The first three AI inputs default to 0.0 for convenience, so
    # availability is based on whether any AI source was explicitly
    # supplied by the caller. The DNA value already uses None to mean
    # unavailable.
    ai_available = any(
        value is not None
        for value in (
            behavioral_anomaly_score,
            gaming_score,
            nlp_score,
            investigation_dna_quality,
        )
    )

    available_components = [
        (
            "rule",
            rule_score,
            RULE_WEIGHT,
            True,
        ),
        (
            "behavioral",
            ai_score,
            AI_WEIGHT,
            ai_available,
        ),
        (
            "negative_space",
            negative_space,
            NEGATIVE_SPACE_WEIGHT,
            negative_space_available,
        ),
        (
            "peer",
            peer,
            PEER_WEIGHT,
            peer_available,
        ),
    ]

    active_weight = sum(
        weight
        for _, _, weight, available
        in available_components
        if available
    )

    if active_weight <= 0:
        final_score = 0.0

    else:
        final_score = sum(
            score * weight
            for _, score, weight, available
            in available_components
            if available
        ) / active_weight

    final_score = _round(final_score)

    # ----------------------------------------------------------
    # Component output
    # ----------------------------------------------------------

    components = {
        "rule": _round(rule_score),
        "behavioral": _round(ai_score),
        "negative_space": (
            _round(negative_space)
            if negative_space_available
            else None
        ),
        "peer": (
            _round(peer)
            if peer_available
            else None
        ),
    }

    # ----------------------------------------------------------
    # Indicators
    # ----------------------------------------------------------

    indicators: list[str] = []

    indicator_sources = [
        rule_indicators or [],
        behavioral_indicators or [],
        gaming_indicators or [],
        nlp_indicators or [],
        negative_space_indicators or [],
        peer_indicators or [],
    ]

    for source in indicator_sources:
        for indicator in source:
            if indicator and indicator not in indicators:
                indicators.append(indicator)

    # ----------------------------------------------------------
    # Signals
    # ----------------------------------------------------------

    signals = [
        {
            "source": "rule",
            "score": _round(rule_score),
            "weight": RULE_WEIGHT,
        },
    ]

    if ai_available:
        signals.append(
            {
                "source": "behavioral",
                "score": _round(ai_score),
                "weight": AI_WEIGHT,
                "details": ai_components,
            }
        )

    if negative_space_available:
        signals.append(
            {
                "source": "negative_space",
                "score": _round(
                    negative_space
                ),
                "weight": NEGATIVE_SPACE_WEIGHT,
            }
        )

    if peer_available:
        signals.append(
            {
                "source": "peer",
                "score": _round(peer),
                "weight": PEER_WEIGHT,
            }
        )

    # ----------------------------------------------------------
    # Explanation
    # ----------------------------------------------------------

    level = risk_level(final_score)

    explanation_parts = [
        (
            f"Final supervisory risk is "
            f"{final_score}/100 ({level})."
        )
    ]

    if rule_score >= 40:
        explanation_parts.append(
            "Deterministic rules identified "
            "concerning analyst behavior."
        )

    if ai_score >= 40:
        explanation_parts.append(
            "Behavioral and AI-derived signals "
            "indicate elevated concern."
        )

    if negative_space_available and negative_space >= 40:
        explanation_parts.append(
            "Negative-space intelligence indicates "
            "a monitoring or visibility gap."
        )

    if peer_available and peer >= 40:
        explanation_parts.append(
            "Peer comparison shows meaningful "
            "deviation from the benchmark."
        )

    explanation = " ".join(
        explanation_parts
    )

    # ----------------------------------------------------------
    # Confidence
    # ----------------------------------------------------------

    component_count = 1  # rule is always available

    if ai_available:
        component_count += 1

    if negative_space_available:
        component_count += 1

    if peer_available:
        component_count += 1

    confidence = calculate_risk_confidence(
        observations=observations,
        component_count=component_count,
        component_confidences=(
            component_confidences
            or []
        ),
    )

    return RiskFusionFinding(
        entity_type="analyst",
        entity_id=str(analyst_id),
        score=final_score,
        level=level,
        severity=risk_severity(
            final_score
        ),
        confidence=confidence,
        components=components,
        indicators=indicators,
        signals=signals,
        explanation=explanation,
    )


# ==============================================================
# Convenience dictionary interface
# ==============================================================


def fuse_analyst_risk(
    *,
    analyst_id: str,
    rule_score: float,
    behavioral_anomaly_score: float = 0.0,
    gaming_score: float = 0.0,
    nlp_score: float = 0.0,
    investigation_dna_quality: float | None = None,
    negative_space_score: float | None = None,
    peer_score: float | None = None,
    observations: int = 0,
    component_confidences: list[str] | None = None,
    rule_indicators: list[str] | None = None,
    behavioral_indicators: list[str] | None = None,
    gaming_indicators: list[str] | None = None,
    nlp_indicators: list[str] | None = None,
    negative_space_indicators: list[str] | None = None,
    peer_indicators: list[str] | None = None,
) -> dict:
    """
    Dictionary-oriented wrapper used by analyst_metrics.py.
    """

    finding = calculate_risk_fusion(
        analyst_id=analyst_id,
        rule_score=rule_score,
        behavioral_anomaly_score=(
            behavioral_anomaly_score
        ),
        gaming_score=gaming_score,
        nlp_score=nlp_score,
        investigation_dna_quality=(
            investigation_dna_quality
        ),
        negative_space_score=(
            negative_space_score
        ),
        peer_score=peer_score,
        observations=observations,
        component_confidences=(
            component_confidences
        ),
        rule_indicators=rule_indicators,
        behavioral_indicators=(
            behavioral_indicators
        ),
        gaming_indicators=(
            gaming_indicators
        ),
        nlp_indicators=nlp_indicators,
        negative_space_indicators=(
            negative_space_indicators
        ),
        peer_indicators=peer_indicators,
    )

    return {
        "score": finding.score,
        "level": finding.level,
        "severity": finding.severity,
        "confidence": finding.confidence,
        "components": finding.components,
        "indicators": finding.indicators,
        "signals": finding.signals,
        "explanation": finding.explanation,
    }