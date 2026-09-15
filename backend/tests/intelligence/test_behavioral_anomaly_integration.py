from app.services.analytics.analyst_metrics import (
    get_analyst_metrics,
)


def test_real_analyst_metrics_includes_behavioral_anomaly():
    results = get_analyst_metrics()

    assert isinstance(results, list)
    assert len(results) > 0

    analyst = results[0]

    assert "analyst_id" in analyst
    assert "behavioral_anomaly" in analyst

    anomaly = analyst["behavioral_anomaly"]

    assert "score" in anomaly
    assert "severity" in anomaly
    assert "confidence" in anomaly
    assert "indicators" in anomaly
    assert "observations" in anomaly
    assert "metrics" in anomaly

    assert isinstance(
        anomaly["score"],
        (int, float),
    )

    assert 0 <= anomaly["score"] <= 100

    assert anomaly["severity"] in {
        "LOW",
        "MEDIUM",
        "HIGH",
    }

    assert anomaly["confidence"] in {
        "Low",
        "Medium",
        "High",
    }

    assert isinstance(
        anomaly["indicators"],
        list,
    )

    assert isinstance(
        anomaly["observations"],
        list,
    )

    assert isinstance(
        anomaly["metrics"],
        dict,
    )