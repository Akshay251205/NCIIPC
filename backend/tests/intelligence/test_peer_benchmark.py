from app.services.peer.peer_benchmark import (
    PeerBenchmarkFinding,
    calculate_peer_benchmark,
)


def test_peer_benchmark_normal_behavior():

    finding = calculate_peer_benchmark(
        analyst_id="AN001",

        analyst_metrics={
            "average_closure_time_minutes": 35,
            "evidence_review_rate": 90,
            "escalation_rate": 40,
            "average_queries": 5,
            "average_actions": 3,
            "average_investigation_duration_minutes": 45,
            "short_note_rate": 10,
            "repeated_note_rate": 5,
        },

        peer_metrics={
            "average_closure_time_minutes": 35,
            "evidence_review_rate": 90,
            "escalation_rate": 40,
            "average_queries": 5,
            "average_actions": 3,
            "average_investigation_duration_minutes": 45,
            "short_note_rate": 10,
            "repeated_note_rate": 5,
        },

        peer_observations=20,
    )

    assert isinstance(
        finding,
        PeerBenchmarkFinding,
    )

    assert finding.score == 0

    assert finding.indicators == []

    assert finding.confidence == "High"


def test_peer_benchmark_detects_large_deviation():

    finding = calculate_peer_benchmark(
        analyst_id="AN002",

        analyst_metrics={
            "average_closure_time_minutes": 5,
            "evidence_review_rate": 20,
            "average_queries": 1,
        },

        peer_metrics={
            "average_closure_time_minutes": 35,
            "evidence_review_rate": 90,
            "average_queries": 5,
        },

        peer_observations=20,
    )

    assert finding.score > 0

    assert len(
        finding.indicators
    ) >= 2


def test_peer_benchmark_confidence():

    finding = calculate_peer_benchmark(
        analyst_id="AN003",

        analyst_metrics={
            "evidence_review_rate": 20,
        },

        peer_metrics={
            "evidence_review_rate": 90,
        },

        peer_observations=5,
    )

    assert finding.confidence == "Medium"


def test_peer_benchmark_score_is_capped():

    finding = calculate_peer_benchmark(
        analyst_id="AN004",

        analyst_metrics={
            "average_closure_time_minutes": 1,
            "evidence_review_rate": 1,
            "escalation_rate": 1,
            "average_queries": 1,
            "average_actions": 1,
            "average_investigation_duration_minutes": 1,
            "short_note_rate": 100,
            "repeated_note_rate": 100,
        },

        peer_metrics={
            "average_closure_time_minutes": 100,
            "evidence_review_rate": 100,
            "escalation_rate": 100,
            "average_queries": 100,
            "average_actions": 100,
            "average_investigation_duration_minutes": 100,
            "short_note_rate": 1,
            "repeated_note_rate": 1,
        },

        peer_observations=50,
    )

    assert 0 <= finding.score <= 100


def test_peer_benchmark_to_dict():

    finding = calculate_peer_benchmark(
        analyst_id="AN005",

        analyst_metrics={
            "evidence_review_rate": 20,
        },

        peer_metrics={
            "evidence_review_rate": 90,
        },

        peer_observations=10,
    )

    result = finding.to_dict()

    assert result["entity_type"] == "ANALYST"

    assert result["entity_id"] == "AN005"

    assert "score" in result

    assert "severity" in result

    assert "indicators" in result

    assert "observations" in result

    assert "metrics" in result

    assert "confidence" in result