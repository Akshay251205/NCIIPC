from app.services.analytics.analyst_metrics import (
    get_analyst_metrics,
)


def test_real_analyst_metrics_includes_peer_benchmark():

    results = get_analyst_metrics()

    assert isinstance(results, list)
    assert len(results) > 0

    analyst = results[0]

    assert "analyst_id" in analyst

    assert "peer_benchmark" in analyst

    peer = analyst["peer_benchmark"]

    assert "score" in peer
    assert "severity" in peer
    assert "confidence" in peer
    assert "indicators" in peer
    assert "observations" in peer
    assert "metrics" in peer

    assert isinstance(
        peer["score"],
        (int, float),
    )

    assert 0 <= peer["score"] <= 100

    assert isinstance(
        peer["indicators"],
        list,
    )

    assert isinstance(
        peer["observations"],
        list,
    )

    assert isinstance(
        peer["metrics"],
        dict,
    )