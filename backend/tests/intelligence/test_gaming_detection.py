from app.services.gaming.gaming_detection import (
    GamingFinding,
    detect_gaming_behavior,
)


def test_fast_closure_is_detected():

    finding = detect_gaming_behavior(
        analyst_id="AN001",
        total_alerts=10,
        closed_alerts=10,
        average_closure_time_minutes=5,
    )

    assert isinstance(
        finding,
        GamingFinding,
    )

    assert finding.score > 0

    assert (
        "Suspiciously fast alert closure"
        in finding.indicators
    )


def test_low_evidence_review_is_detected():

    finding = detect_gaming_behavior(
        analyst_id="AN002",
        total_alerts=10,
        closed_alerts=8,
        evidence_review_rate=20,
    )

    assert (
        "Low evidence-review behavior"
        in finding.indicators
    )


def test_shallow_investigation_is_detected():

    finding = detect_gaming_behavior(
        analyst_id="AN003",
        total_alerts=10,
        total_investigations=10,
        average_queries=1,
        average_actions=1,
    )

    assert (
        "Shallow investigation activity"
        in finding.indicators
    )

    assert (
        "Low investigation action count"
        in finding.indicators
    )


def test_repeated_notes_are_detected():

    finding = detect_gaming_behavior(
        analyst_id="AN004",
        total_alerts=10,
        total_investigations=10,
        repeated_note_rate=80,
    )

    assert (
        "High repeated-note rate"
        in finding.indicators
    )


def test_combined_gaming_pattern():

    finding = detect_gaming_behavior(
        analyst_id="AN005",
        total_alerts=20,
        closed_alerts=20,
        average_closure_time_minutes=5,
        evidence_review_rate=20,
        total_investigations=20,
        average_queries=1,
        average_actions=1,
        average_investigation_duration_minutes=5,
        short_note_rate=80,
        repeated_note_rate=70,
    )

    assert finding.score >= 70

    assert (
        "Pattern consistent with potential "
        "metric-gaming behavior"
        in finding.indicators
    )

    assert finding.severity == "HIGH"


def test_normal_behavior_has_low_score():

    finding = detect_gaming_behavior(
        analyst_id="AN006",
        total_alerts=20,
        closed_alerts=15,
        average_closure_time_minutes=35,
        evidence_review_rate=90,
        investigation_evidence_review_rate=90,
        total_investigations=15,
        average_queries=5,
        average_actions=3,
        average_investigation_duration_minutes=45,
        short_note_rate=10,
        repeated_note_rate=5,
    )

    assert finding.score == 0

    assert finding.indicators == []