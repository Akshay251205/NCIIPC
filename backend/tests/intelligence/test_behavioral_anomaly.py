from app.services.anomaly.behavioral_anomaly import (
    calculate_population_metrics,
    detect_behavioral_anomaly,
)


def _normal_metrics():
    return {
        "average_closure_time_minutes": 40.0,
        "evidence_review_rate": 75.0,
        "escalation_rate": 35.0,
        "false_positive_rate": 15.0,
        "average_queries": 4.0,
        "average_actions": 3.0,
        "average_investigation_duration_minutes": 40.0,
        "short_note_rate": 20.0,
        "repeated_note_rate": 10.0,
    }


def test_normal_behavior_has_low_anomaly_score():
    population = [
        _normal_metrics()
        for _ in range(10)
    ]

    finding = detect_behavioral_anomaly(
        analyst_id="AN001",
        analyst_metrics=_normal_metrics(),
        population_metrics=population,
        observation_count=10,
    )

    assert finding.score <= 40
    assert finding.severity == "LOW"


def test_unusual_closure_time_is_detected():
    population = [
        _normal_metrics()
        for _ in range(10)
    ]

    analyst = _normal_metrics()
    analyst[
        "average_closure_time_minutes"
    ] = 200.0

    finding = detect_behavioral_anomaly(
        analyst_id="AN002",
        analyst_metrics=analyst,
        population_metrics=population,
        observation_count=10,
    )

    assert finding.score > 0
    assert (
        "Unusual closure-time behavior"
        in finding.indicators
    )


def test_multiple_anomalies_increase_score():
    population = [
        _normal_metrics()
        for _ in range(10)
    ]

    analyst = _normal_metrics()

    analyst[
        "average_closure_time_minutes"
    ] = 200.0

    analyst[
        "evidence_review_rate"
    ] = 5.0

    analyst[
        "average_queries"
    ] = 0.1

    finding = detect_behavioral_anomaly(
        analyst_id="AN003",
        analyst_metrics=analyst,
        population_metrics=population,
        observation_count=10,
    )

    assert finding.score >= 40
    assert len(finding.indicators) >= 2


def test_low_confidence_with_few_observations():
    population = [
        _normal_metrics()
        for _ in range(3)
    ]

    finding = detect_behavioral_anomaly(
        analyst_id="AN004",
        analyst_metrics=_normal_metrics(),
        population_metrics=population,
        observation_count=1,
    )

    assert finding.confidence == "Low"


def test_high_confidence_with_sufficient_observations():
    population = [
        _normal_metrics()
        for _ in range(20)
    ]

    analyst = _normal_metrics()
    analyst[
        "average_closure_time_minutes"
    ] = 200.0

    finding = detect_behavioral_anomaly(
        analyst_id="AN005",
        analyst_metrics=analyst,
        population_metrics=population,
        observation_count=20,
    )

    assert finding.confidence == "High"


def test_to_dict_contains_expected_fields():
    population = [
        _normal_metrics()
        for _ in range(10)
    ]

    finding = detect_behavioral_anomaly(
        analyst_id="AN006",
        analyst_metrics=_normal_metrics(),
        population_metrics=population,
        observation_count=10,
    )

    result = finding.to_dict()

    assert result["entity_type"] == "analyst"
    assert result["entity_id"] == "AN006"
    assert "score" in result
    assert "severity" in result
    assert "confidence" in result
    assert "indicators" in result
    assert "observations" in result
    assert "metrics" in result


def test_calculate_population_metrics_supports_nested_sat_sa_output():
    records = [
        {
            "performance": {
                "average_closure_time_minutes": 30.0,
                "evidence_review_rate": 80.0,
                "escalation_rate": 40.0,
                "false_positive_rate": 10.0,
            },
            "investigations": {
                "average_queries": 5.0,
                "average_actions": 3.0,
                "average_duration_minutes": 45.0,
            },
        }
    ]

    population = calculate_population_metrics(
        records
    )

    assert len(population) == 1

    assert (
        population[0][
            "average_closure_time_minutes"
        ]
        == 30.0
    )

    assert (
        population[0]["evidence_review_rate"]
        == 80.0
    )

    assert (
        population[0]["average_queries"]
        == 5.0
    )

    assert (
        population[0]["average_actions"]
        == 3.0
    )

    assert (
        population[0][
            "average_investigation_duration_minutes"
        ]
        == 45.0
    )