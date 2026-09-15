"""Canonical analyst trust-profile service.

This service is intentionally a thin composition layer. It reuses the bulk
analytics pipeline, Risk Fusion output, and final-finding builder instead of
maintaining a second scoring implementation.
"""

from __future__ import annotations

from typing import Any

from app.services.analytics.analyst_metrics import get_analyst_metrics
from app.services.findings.final_finding import build_final_finding_dict


def get_analyst_trust_profile(
    analyst_id: str,
) -> dict[str, Any] | None:
    """Return one deterministic, explainable analyst trust profile.

    The canonical analytics pipeline uses bulk loading and population
    statistics. Filtering happens only after that one complete computation,
    avoiding an analyst-specific database query path.
    """

    requested_id = str(analyst_id)

    analyst = next(
        (
            record
            for record in get_analyst_metrics()
            if str(record.get("analyst_id")) == requested_id
        ),
        None,
    )

    if analyst is None:
        return None

    finding = build_final_finding_dict(analyst)

    return {
        "analyst_id": requested_id,
        "risk": analyst["risk"],
        "behavioral_anomaly": analyst["behavioral_anomaly"],
        "gaming": analyst["gaming"],
        "investigation_nlp": analyst["investigation_nlp"],
        "peer_benchmark": analyst["peer_benchmark"],
        "negative_space": analyst.get("negative_space"),
        "evidence": finding["primary_indicators"],
        "evidence_context": finding["evidence"],
        "recommendations": finding["supervisory_actions"],
        "explanation": finding["explanation"],
    }
