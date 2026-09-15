import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class InvestigationNLPFinding:
    """
    Explainable NLP analysis of an investigation note.

    The result describes note quality and investigation-language
    signals. It does not determine analyst intent or misconduct.
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


def _normalize_text(text: str | None) -> str:
    """
    Normalize investigation text for analysis.
    """

    if text is None:
        return ""

    return " ".join(
        str(text).lower().split()
    )


def _tokenize(text: str) -> list[str]:
    """
    Extract simple word tokens.
    """

    return re.findall(
        r"[a-z0-9_/-]+",
        text.lower(),
    )


def _safe_ratio(
    numerator: int,
    denominator: int,
) -> float:
    """
    Safely calculate a ratio.
    """

    if denominator <= 0:
        return 0.0

    return numerator / denominator


def _clamp(
    value: float,
    minimum: float = 0.0,
    maximum: float = 100.0,
) -> float:
    return max(
        minimum,
        min(value, maximum),
    )


def _round(value: float) -> float:
    return round(value, 2)


# --------------------------------------------------------------
# Security investigation vocabulary
# --------------------------------------------------------------

SECURITY_TERMS = {
    "alert",
    "alerted",
    "authentication",
    "bruteforce",
    "brute-force",
    "credential",
    "credentials",
    "endpoint",
    "firewall",
    "forensic",
    "hash",
    "ioc",
    "ip",
    "malware",
    "phishing",
    "process",
    "ransomware",
    "registry",
    "siem",
    "source",
    "threat",
    "token",
    "url",
    "user",
    "username",
    "virus",
    "vpn",
    "edr",
    "xdr",
    "dns",
    "domain",
    "command",
    "powershell",
    "script",
    "payload",
    "suspicious",
    "compromise",
    "incident",
    "investigation",
    "evidence",
    "logs",
    "log",
}


# --------------------------------------------------------------
# Investigation-action vocabulary
# --------------------------------------------------------------

ACTION_TERMS = {
    "review",
    "reviewed",
    "checked",
    "check",
    "searched",
    "search",
    "queried",
    "query",
    "validated",
    "validate",
    "correlated",
    "correlate",
    "inspected",
    "inspect",
    "analyzed",
    "analyse",
    "analyze",
    "investigated",
    "investigate",
    "confirmed",
    "confirm",
    "blocked",
    "isolated",
    "escalated",
    "escalate",
    "remediated",
    "remediate",
    "contained",
    "contain",
}


# --------------------------------------------------------------
# Evidence vocabulary
# --------------------------------------------------------------

EVIDENCE_TERMS = {
    "evidence",
    "logs",
    "log",
    "event",
    "events",
    "timestamp",
    "timeline",
    "source",
    "sources",
    "ioc",
    "hash",
    "ip",
    "url",
    "process",
    "command",
    "screenshot",
    "artifact",
    "artifacts",
}


# --------------------------------------------------------------
# Generic / weak investigation language
# --------------------------------------------------------------

GENERIC_PHRASES = {
    "checked alert",
    "reviewed alert",
    "looked into it",
    "looks fine",
    "nothing found",
    "no issue",
    "normal activity",
    "false positive",
    "closed alert",
    "resolved",
    "handled",
    "done",
    "ok",
    "okay",
}


def calculate_note_quality(
    note: str | None,
) -> dict[str, Any]:
    """
    Calculate explainable investigation-note quality metrics.

    Higher quality means more investigative detail,
    security context, actions, and evidence references.
    """

    normalized = _normalize_text(note)
    tokens = _tokenize(normalized)

    token_count = len(tokens)

    if token_count == 0:
        return {
            "score": 0.0,
            "token_count": 0,
            "security_term_count": 0,
            "action_term_count": 0,
            "evidence_term_count": 0,
            "generic_phrase_count": 0,
        }

    security_term_count = sum(
        1
        for token in tokens
        if token in SECURITY_TERMS
    )

    action_term_count = sum(
        1
        for token in tokens
        if token in ACTION_TERMS
    )

    evidence_term_count = sum(
        1
        for token in tokens
        if token in EVIDENCE_TERMS
    )

    generic_phrase_count = sum(
        1
        for phrase in GENERIC_PHRASES
        if phrase in normalized
    )

    # ----------------------------------------------------------
    # Detail score
    # ----------------------------------------------------------

    detail_score = min(
        token_count / 40.0,
        1.0,
    ) * 30.0

    # ----------------------------------------------------------
    # Security context
    # ----------------------------------------------------------

    security_score = min(
        security_term_count / 5.0,
        1.0,
    ) * 25.0

    # ----------------------------------------------------------
    # Investigative actions
    # ----------------------------------------------------------

    action_score = min(
        action_term_count / 4.0,
        1.0,
    ) * 25.0

    # ----------------------------------------------------------
    # Evidence references
    # ----------------------------------------------------------

    evidence_score = min(
        evidence_term_count / 3.0,
        1.0,
    ) * 20.0

    score = (
        detail_score
        + security_score
        + action_score
        + evidence_score
    )

    # Generic phrases reduce quality.
    score -= generic_phrase_count * 10.0

    score = _clamp(score)

    return {
        "score": _round(score),
        "token_count": token_count,
        "security_term_count": security_term_count,
        "action_term_count": action_term_count,
        "evidence_term_count": evidence_term_count,
        "generic_phrase_count": generic_phrase_count,
    }


def detect_investigation_nlp(
    *,
    investigation_id: str,
    note: str | None,
    evidence_reviewed: bool | None = None,
) -> InvestigationNLPFinding:
    """
    Analyze a single investigation note.

    The score represents concern about insufficient or
    low-quality investigative documentation.

    Higher score = more concerning note characteristics.
    """

    normalized = _normalize_text(note)

    note_quality = calculate_note_quality(
        normalized
    )

    quality_score = note_quality["score"]

    indicators: list[str] = []
    observations: list[str] = []

    # ----------------------------------------------------------
    # Missing note
    # ----------------------------------------------------------

    if not normalized:

        indicators.append(
            "Missing investigation note"
        )

        observations.append(
            "No investigation narrative was available "
            "for NLP analysis."
        )

    # ----------------------------------------------------------
    # Very short note
    # ----------------------------------------------------------

    elif note_quality["token_count"] < 8:

        indicators.append(
            "Very short investigation note"
        )

        observations.append(
            "The investigation note contains very little "
            "documented investigative detail."
        )

    # ----------------------------------------------------------
    # Generic note
    # ----------------------------------------------------------

    if note_quality["generic_phrase_count"] > 0:

        indicators.append(
            "Generic investigation language"
        )

        observations.append(
            "The note contains generic language with "
            "limited investigation-specific detail."
        )

    # ----------------------------------------------------------
    # Weak security context
    # ----------------------------------------------------------

    if (
        normalized
        and note_quality["security_term_count"] == 0
    ):

        indicators.append(
            "Limited security context"
        )

        observations.append(
            "The note contains few or no recognized "
            "security-investigation terms."
        )

    # ----------------------------------------------------------
    # Weak investigative action documentation
    # ----------------------------------------------------------

    if (
        normalized
        and note_quality["action_term_count"] == 0
    ):

        indicators.append(
            "Limited investigative actions documented"
        )

        observations.append(
            "The note does not clearly describe "
            "investigative actions."
        )

    # ----------------------------------------------------------
    # Weak evidence documentation
    # ----------------------------------------------------------

    if (
        normalized
        and note_quality["evidence_term_count"] == 0
    ):

        indicators.append(
            "Limited evidence references"
        )

        observations.append(
            "The note contains few or no recognized "
            "evidence references."
        )

    # ----------------------------------------------------------
    # Evidence mismatch
    # ----------------------------------------------------------

    if (
        evidence_reviewed is True
        and note_quality["evidence_term_count"] == 0
    ):

        indicators.append(
            "Evidence review not reflected in note"
        )

        observations.append(
            "Evidence was marked as reviewed, but the "
            "investigation note does not clearly describe "
            "supporting evidence."
        )

    # ----------------------------------------------------------
    # Convert quality to concern score
    # ----------------------------------------------------------

    concern_score = 100.0 - quality_score

    # Missing or extremely weak documentation gets stronger
    # concern weighting.
    if not normalized:
        concern_score = 100.0

    elif note_quality["token_count"] < 8:
        concern_score += 10.0

    if len(indicators) >= 3:
        concern_score += 10.0

    concern_score = _clamp(
        concern_score
    )

    # ----------------------------------------------------------
    # Severity
    # ----------------------------------------------------------

    if concern_score >= 70:
        severity = "HIGH"

    elif concern_score >= 40:
        severity = "MEDIUM"

    else:
        severity = "LOW"

    # ----------------------------------------------------------
    # Confidence
    # ----------------------------------------------------------

    if note_quality["token_count"] >= 20:
        confidence = "High"

    elif note_quality["token_count"] >= 8:
        confidence = "Medium"

    else:
        confidence = "Low"

    # ----------------------------------------------------------
    # Normal observation
    # ----------------------------------------------------------

    if not indicators:

        observations.append(
            "The investigation note contains sufficient "
            "detail and recognizable investigative context."
        )

    return InvestigationNLPFinding(
        entity_type="investigation",
        entity_id=str(investigation_id),
        score=_round(concern_score),
        severity=severity,
        confidence=confidence,
        indicators=indicators,
        observations=observations,
        metrics={
            "note_quality_score": quality_score,
            **note_quality,
        },
    )


def analyze_investigation_notes(
    records: list[dict[str, Any]],
) -> list[dict]:
    """
    Analyze multiple investigation records.

    Expected fields:

        investigation_id
        investigation_notes
        evidence_reviewed
    """

    results = []

    for record in records:

        finding = detect_investigation_nlp(
            investigation_id=str(
                record.get(
                    "investigation_id",
                    "",
                )
            ),
            note=record.get(
                "investigation_notes"
            ),
            evidence_reviewed=record.get(
                "evidence_reviewed"
            ),
        )

        results.append(
            finding.to_dict()
        )

    return results