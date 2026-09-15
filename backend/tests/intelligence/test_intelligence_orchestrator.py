from app.services.intelligence import (
    build_intelligence_context,
    calculate_intelligence_summary,
    collect_intelligence_indicators,
    orchestrate_all_analysts,
    orchestrate_analyst_intelligence,
)


def sample_analyst():
    return {
        "analyst_id": "AN001",
        "investigation_dna": {
            "investigation_quality_score": 75,
            "confidence": "High",
            "indicators": [
                "Strong evidence discipline",
            ],
        },
        "gaming": {
            "score": 60,
            "severity": "MEDIUM",
            "confidence": "High",
            "indicators": [
                "Suspiciously fast closure",
            ],
        },
        "peer_benchmark": {
            "score": 50,
            "severity": "MEDIUM",
            "confidence": "Medium",
            "indicators": [
                "High closure-time deviation",
            ],
        },
        "behavioral_anomaly": {
            "score": 80,
            "severity": "HIGH",
            "confidence": "High",
            "indicators": [
                "Unusual closure behavior",
            ],
        },
        "investigation_nlp": {
            "average_score": 40,
            "high_findings": 1,
            "medium_findings": 2,
            "investigations_analyzed": 4,
            "indicators": [
                "Generic investigation language",
            ],
        },
        "negative_space": {
            "score": 70,
            "severity": "HIGH",
            "confidence": "Medium",
            "indicators": [
                "Monitoring visibility gap",
            ],
        },
        "risk": {
            "score": 72,
            "level": "HIGH",
        },
    }


def test_build_intelligence_context():
    context = build_intelligence_context(
        sample_analyst()
    )

    assert context["analyst_id"] == "AN001"

    assert (
        context["dna"]["quality_score"]
        == 75
    )

    assert (
        context["gaming"]["score"]
        == 60
    )

    assert (
        context["peer"]["score"]
        == 50
    )

    assert (
        context["behavioral_anomaly"]["score"]
        == 80
    )

    assert (
        context["nlp"]["score"]
        == 40
    )

    assert (
        context["negative_space"]["score"]
        == 70
    )


def test_missing_optional_layers_remain_unavailable():
    analyst = {
        "analyst_id": "AN002",
        "investigation_dna": {},
        "gaming": {},
        "peer_benchmark": {},
        "behavioral_anomaly": {},
        "investigation_nlp": {},
    }

    context = build_intelligence_context(
        analyst
    )

    assert (
        context["negative_space"]
        is None
    )


def test_collect_intelligence_indicators_deduplicates():
    context = {
        "dna": {
            "indicators": [
                "Fast closure",
                "Low evidence review",
            ]
        },
        "gaming": {
            "indicators": [
                "Fast closure",
                "Short investigation",
            ]
        },
        "peer": {
            "indicators": [
                "Peer deviation",
            ]
        },
        "behavioral_anomaly": {
            "indicators": [
                "Fast closure",
            ]
        },
        "nlp": {
            "indicators": [
                "Generic language",
            ]
        },
        "negative_space": None,
    }

    indicators = (
        collect_intelligence_indicators(
            context
        )
    )

    assert indicators.count(
        "Fast closure"
    ) == 1

    assert (
        "Low evidence review"
        in indicators
    )

    assert (
        "Short investigation"
        in indicators
    )

    assert (
        "Peer deviation"
        in indicators
    )

    assert (
        "Generic language"
        in indicators
    )


def test_calculate_intelligence_summary():
    context = build_intelligence_context(
        sample_analyst()
    )

    summary = (
        calculate_intelligence_summary(
            context
        )
    )

    assert (
        0
        <= summary[
            "average_concern_score"
        ]
        <= 100
    )

    assert (
        summary[
            "highest_concern_score"
        ]
        == 80
    )

    assert (
        summary[
            "high_signal_count"
        ]
        >= 1
    )

    assert (
        summary[
            "investigation_quality_score"
        ]
        == 75
    )

    assert isinstance(
        summary["indicators"],
        list,
    )


def test_orchestrate_analyst_intelligence():
    result = (
        orchestrate_analyst_intelligence(
            sample_analyst()
        )
    )

    assert (
        result["entity_type"]
        == "analyst"
    )

    assert (
        result["entity_id"]
        == "AN001"
    )

    assert (
        result["status"]
        == "complete"
    )

    assert (
        "rules"
        in result["available_layers"]
    )

    assert (
        "investigation_dna"
        in result["available_layers"]
    )

    assert (
        "gaming"
        in result["available_layers"]
    )

    assert (
        "peer_benchmark"
        in result["available_layers"]
    )

    assert (
        "behavioral_anomaly"
        in result["available_layers"]
    )

    assert (
        "investigation_nlp"
        in result["available_layers"]
    )

    assert (
        "negative_space"
        in result["available_layers"]
    )

    assert (
        "context"
        in result
    )

    assert (
        "summary"
        in result
    )


def test_orchestrate_all_analysts():
    analysts = [
        sample_analyst(),
        {
            "analyst_id": "AN002",
        },
    ]

    results = (
        orchestrate_all_analysts(
            analysts
        )
    )

    assert len(results) == 2
    assert (
        results[0]["entity_id"]
        == "AN001"
    )
    assert (
        results[1]["entity_id"]
        == "AN002"
    )


def test_orchestrate_all_analysts_handles_invalid_input():
    assert (
        orchestrate_all_analysts(None)
        == []
    )

    assert (
        orchestrate_all_analysts("invalid")
        == []
    )