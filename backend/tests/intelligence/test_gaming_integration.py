from app.services.analytics.analyst_metrics import (
    get_analyst_metrics,
)


def test_real_analyst_metrics_includes_gaming_detection():

    results = get_analyst_metrics()

    assert isinstance(results, list)
    assert len(results) > 0

    analyst = results[0]

    # Existing analytics
    assert "analyst_id" in analyst
    assert "alerts" in analyst
    assert "investigations" in analyst
    assert "risk" in analyst

    # Gaming detection
    assert "gaming" in analyst

    gaming = analyst["gaming"]

    assert "score" in gaming
    assert "severity" in gaming
    assert "confidence" in gaming
    assert "indicators" in gaming
    assert "observations" in gaming
    assert "metrics" in gaming

    # Score must be valid
    assert isinstance(
        gaming["score"],
        (int, float),
    )

    assert 0 <= gaming["score"] <= 100

    # These should be collections
    assert isinstance(
        gaming["indicators"],
        list,
    )

    assert isinstance(
        gaming["observations"],
        list,
    )

    assert isinstance(
        gaming["metrics"],
        dict,
    )