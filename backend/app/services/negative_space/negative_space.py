from dataclasses import dataclass, field


# ============================================================
# Negative Space Detection
# ============================================================


@dataclass
class NegativeSpaceFinding:
    """
    Represents an absence-of-expected-activity finding.
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


def _clamp(value, minimum=0.0, maximum=100.0):
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
    *,
    has_asset_data: bool,
    has_activity_data: bool,
) -> str:

    if has_asset_data and has_activity_data:
        return "High"

    if has_asset_data or has_activity_data:
        return "Medium"

    return "Low"


# ============================================================
# Core detector
# ============================================================


def detect_negative_space(
    *,
    asset_id: str,
    asset_status: str | None = None,
    asset_criticality: str | None = None,
    has_activity_record: bool = False,
    event_count: int | float | None = None,
    log_sources_active: int | float | None = None,
) -> NegativeSpaceFinding:

    event_count = max(
        _safe_float(event_count),
        0.0,
    )

    log_sources_active = max(
        _safe_float(log_sources_active),
        0.0,
    )

    indicators = []
    observations = []

    score = 0.0

    # --------------------------------------------------------
    # Signal 1: No activity record
    # --------------------------------------------------------

    if not has_activity_record:

        score += 60

        indicators.append(
            "No monitoring activity record"
        )

        observations.append(
            "Asset exists but no corresponding "
            "activity record was observed."
        )

    # --------------------------------------------------------
    # Signal 2: Silent activity record
    # --------------------------------------------------------

    if has_activity_record and event_count <= 0:

        score += 30

        indicators.append(
            "Silent asset activity"
        )

        observations.append(
            "Asset has an activity record but "
            "no events were observed."
        )

    # --------------------------------------------------------
    # Signal 3: No active log sources
    # --------------------------------------------------------

    if has_activity_record and log_sources_active <= 0:

        score += 25

        indicators.append(
            "No active log sources"
        )

        observations.append(
            "No active log sources were observed "
            "for the asset."
        )

    # --------------------------------------------------------
    # Signal 4: Inactive asset
    # --------------------------------------------------------

    if asset_status:

        normalized_status = str(
            asset_status
        ).strip().lower()

        if normalized_status == "inactive":

            score += 20

            indicators.append(
                "Asset marked inactive"
            )

            observations.append(
                "Asset is currently marked inactive."
            )

    # --------------------------------------------------------
    # Criticality modifier
    # --------------------------------------------------------

    criticality = str(
        asset_criticality or ""
    ).strip().lower()

    if criticality == "critical":

        score *= 1.30

    elif criticality == "high":

        score *= 1.15

    score = round(
        _clamp(score),
        2,
    )

    return NegativeSpaceFinding(
        entity_type="ASSET",
        entity_id=str(asset_id),
        score=score,
        severity=_severity(score),
        indicators=indicators,
        observations=observations,
        metrics={
            "event_count": event_count,
            "log_sources_active": log_sources_active,
            "has_activity_record": has_activity_record,
            "asset_status": asset_status,
            "asset_criticality": asset_criticality,
        },
        confidence=_confidence(
            has_asset_data=bool(asset_status or asset_criticality),
            has_activity_data=has_activity_record,
        ),
    )


# ============================================================
# Batch detection
# ============================================================


def detect_negative_space_batch(
    assets: list[dict],
) -> list[dict]:

    findings = []

    for asset in assets:

        asset_id = asset.get("asset_id")

        if not asset_id:
            continue

        finding = detect_negative_space(
            asset_id=asset_id,
            asset_status=asset.get(
                "asset_status"
            ),
            asset_criticality=asset.get(
                "asset_criticality"
            ),
            has_activity_record=bool(
                asset.get(
                    "has_activity_record",
                    False,
                )
            ),
            event_count=asset.get(
                "event_count",
                0,
            ),
            log_sources_active=asset.get(
                "log_sources_active",
                0,
            ),
        )

        # Only return meaningful
        # negative-space findings.

        if finding.score > 0:

            findings.append(
                finding.to_dict()
            )

    return findings