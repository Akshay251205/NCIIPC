from app.services.analytics.analyst_metrics import (
    get_analyst_metrics,
)


def test_real_analyst_metrics_includes_investigation_nlp():
    results = get_analyst_metrics()

    assert isinstance(results, list)
    assert len(results) > 0

    analyst = results[0]

    assert "analyst_id" in analyst
    assert "investigation_nlp" in analyst

    nlp = analyst["investigation_nlp"]

    assert "average_score" in nlp
    assert "high_findings" in nlp
    assert "medium_findings" in nlp
    assert "indicators" in nlp
    assert "investigations_analyzed" in nlp

    assert isinstance(
        nlp["average_score"],
        (int, float),
    )

    assert 0 <= nlp["average_score"] <= 100

    assert isinstance(
        nlp["high_findings"],
        int,
    )

    assert isinstance(
        nlp["medium_findings"],
        int,
    )

    assert isinstance(
        nlp["indicators"],
        list,
    )

    assert isinstance(
        nlp["investigations_analyzed"],
        int,
    )

    assert nlp["investigations_analyzed"] >= 0