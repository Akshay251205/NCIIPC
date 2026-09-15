from app.services.intelligence import supervisory_engine


def test_supervisory_analysis_adapts_canonical_fused_risk(monkeypatch):
    """The supervisory API must expose, never recalculate, fused risk."""

    canonical_record = {
        "analyst_id": "AN00001",
        "name": "Canonical Analyst",
        "alerts": {"total": 4},
        "investigations": {"total": 2},
        "risk": {
            "score": 57.15,
            "level": "MEDIUM",
            "severity": "MEDIUM",
            "confidence": "Medium",
            "components": {
                "rule": 30.0,
                "behavioral": 65.16,
                "negative_space": 78.0,
                "peer": 100.0,
            },
            "indicators": ["Low evidence-review rate"],
            "signals": [{"source": "rule", "score": 30.0}],
            "explanation": "Canonical fused explanation.",
        },
    }

    monkeypatch.setattr(
        supervisory_engine,
        "get_analyst_metrics",
        lambda: [canonical_record],
    )

    result = supervisory_engine._run_supervisory_analysis()
    finding = result["findings"][0]

    assert finding["score"] == 57.15
    assert finding["risk_score"] == 57.15
    assert finding["risk_level"] == "MEDIUM"
    assert finding["components"] == canonical_record["risk"]["components"]
    assert result["summary"]["analysts_analyzed"] == 1
