from app.services.analytics.analyst_metrics import (
    get_analyst_metrics,
)


def test_real_analyst_metrics_contains_fused_risk():
    results = get_analyst_metrics()

    assert isinstance(results, list)
    assert len(results) > 0

    analyst = results[0]

    assert "analyst_id" in analyst
    assert "risk" in analyst

    risk = analyst["risk"]

    assert "score" in risk
    assert "level" in risk
    assert "severity" in risk
    assert "confidence" in risk
    assert "components" in risk
    assert "indicators" in risk
    assert "signals" in risk
    assert "explanation" in risk

    assert isinstance(
        risk["score"],
        (int, float),
    )

    assert 0 <= risk["score"] <= 100

    assert risk["level"] in {
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL",
    }

    assert isinstance(
        risk["components"],
        dict,
    )

    components = risk["components"]

    assert "rule" in components
    assert "behavioral" in components
    assert "negative_space" in components
    assert "peer" in components

    assert isinstance(
        risk["indicators"],
        list,
    )

    assert isinstance(
        risk["signals"],
        list,
    )

    assert isinstance(
        risk["explanation"],
        str,
    )

    assert risk["explanation"]