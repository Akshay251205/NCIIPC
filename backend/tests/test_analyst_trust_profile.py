from app.services.intelligence import profile_service


def _analyst_record():
    return {
        "analyst_id": "AN001",
        "risk": {
            "score": 65.0,
            "level": "HIGH",
            "severity": "HIGH",
            "confidence": "High",
            "components": {},
            "indicators": ["Fast closure"],
            "signals": [],
            "explanation": "Final supervisory risk is 65.0/100 (HIGH).",
        },
        "behavioral_anomaly": {
            "score": 50.0,
            "severity": "MEDIUM",
            "confidence": "Medium",
            "indicators": [],
        },
        "gaming": {
            "score": 0.0,
            "severity": "LOW",
            "confidence": "Low",
            "indicators": [],
        },
        "investigation_nlp": {
            "average_score": 60.0,
            "high_findings": 1,
            "medium_findings": 0,
            "investigations_analyzed": 1,
            "indicators": ["Short note"],
        },
        "peer_benchmark": {
            "score": 40.0,
            "severity": "MEDIUM",
            "confidence": "Medium",
            "indicators": [],
        },
        "negative_space": {
            "score": 80.0,
            "severity": "HIGH",
            "confidence": "High",
            "indicators": ["No monitoring activity record"],
        },
    }


def test_profile_reuses_canonical_fused_result(monkeypatch):
    monkeypatch.setattr(
        profile_service,
        "get_analyst_metrics",
        lambda: [_analyst_record()],
    )

    profile = profile_service.get_analyst_trust_profile("AN001")

    assert profile["risk"]["score"] == 65.0
    assert profile["negative_space"]["score"] == 80.0
    assert "No monitoring activity record" in profile["evidence"]
    assert profile["recommendations"]


def test_profile_returns_none_for_unknown_analyst(monkeypatch):
    monkeypatch.setattr(
        profile_service,
        "get_analyst_metrics",
        lambda: [],
    )

    assert (
        profile_service.get_analyst_trust_profile("UNKNOWN")
        is None
    )
