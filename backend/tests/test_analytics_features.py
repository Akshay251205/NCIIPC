from app.services.analytics.feature_builder import (
    build_analyst_feature_record,
    build_analyst_feature_records,
    clamp,
    get_feature_statistics,
    group_features_by_organization,
    percentage,
)


def test_clamp():

    assert clamp(50) == 50

    assert clamp(-10) == 0

    assert clamp(150) == 100


def test_percentage():

    assert percentage(50, 100) == 50.0

    assert percentage(1, 4) == 25.0

    assert percentage(0, 0) == 0.0


def test_build_analyst_feature_record():

    analyst = {
        "analyst_id": "AN001",
        "organization_id": "ORG001",
        "role": "SOC Analyst",
        "team": "Blue Team",
        "shift": "Day",
        "experience_years": 3,

        "alerts": {
            "total": 10,
            "closed": 8,
            "open": 1,
            "investigating": 1,
        },

        "performance": {
            "average_closure_time_minutes": 25.5,
            "minimum_closure_time_minutes": 3,
            "maximum_closure_time_minutes": 100,
            "closure_rate": 80,
            "escalation_rate": 20,
            "false_positive_rate": 10,
            "evidence_review_rate": 90,
        },

        "investigations": {
            "total": 8,
            "coverage_rate": 80,
            "average_duration_minutes": 40,
            "minimum_duration_minutes": 5,
            "maximum_duration_minutes": 90,
            "average_queries": 5,
            "average_actions": 3,
            "evidence_review_rate": 88,
            "escalation_rate": 25,
        },

        "data_quality": {
            "observations": 18,
            "data_confidence": "High",
        },

        "risk": {
            "score": 20,
        },
    }

    result = build_analyst_feature_record(
        analyst
    )

    assert result["analyst_id"] == "AN001"

    assert result["organization_id"] == "ORG001"

    assert result["total_alerts"] == 10

    assert result["closed_alerts"] == 8

    assert result["total_investigations"] == 8

    assert result[
        "average_closure_time_minutes"
    ] == 25.5

    assert result["average_queries"] == 5

    assert result["average_actions"] == 3

    assert result[
        "existing_rule_score"
    ] == 20


def test_build_multiple_analyst_features():

    analysts = [
        {
            "analyst_id": "AN001",
            "organization_id": "ORG001",
            "alerts": {
                "total": 5,
            },
            "investigations": {
                "total": 4,
            },
        },
        {
            "analyst_id": "AN002",
            "organization_id": "ORG002",
            "alerts": {
                "total": 10,
            },
            "investigations": {
                "total": 8,
            },
        },
    ]

    results = build_analyst_feature_records(
        analysts
    )

    assert len(results) == 2

    assert results[0][
        "analyst_id"
    ] == "AN001"

    assert results[1][
        "total_alerts"
    ] == 10


def test_group_features_by_organization():

    features = [
        {
            "analyst_id": "AN001",
            "organization_id": "ORG001",
        },
        {
            "analyst_id": "AN002",
            "organization_id": "ORG001",
        },
        {
            "analyst_id": "AN003",
            "organization_id": "ORG002",
        },
    ]

    grouped = group_features_by_organization(
        features
    )

    assert len(grouped) == 2

    assert len(
        grouped["ORG001"]
    ) == 2

    assert len(
        grouped["ORG002"]
    ) == 1


def test_feature_statistics():

    features = [
        {
            "total_alerts": 10,
            "total_investigations": 8,
        },
        {
            "total_alerts": 20,
            "total_investigations": 12,
        },
    ]

    stats = get_feature_statistics(
        features
    )

    assert stats["analysts"] == 2

    assert stats["total_alerts"] == 30

    assert stats[
        "total_investigations"
    ] == 20

    assert stats[
        "average_alerts_per_analyst"
    ] == 15

    assert stats[
        "average_investigations_per_analyst"
    ] == 10