from app.services.analytics.investigation_dna import (
    InvestigationDNA,
    build_investigation_dna,
    calculate_closure_behavior,
    calculate_dna_confidence,
    calculate_evidence_discipline,
    calculate_investigation_depth,
    calculate_investigation_quality,
    calculate_note_quality,
)


# ============================================================================
# Basic DNA
# ============================================================================


def base_features() -> dict:
    """
    Normal analyst feature set used by the tests.
    """

    return {
        "analyst_id": "AN_TEST",

        "total_alerts": 20,

        "closed_alerts": 18,

        "average_closure_time_minutes": 35,

        "evidence_review_rate": 90,

        "investigation_evidence_review_rate": 90,

        "escalation_rate": 40,

        "investigation_escalation_rate": 50,

        "total_investigations": 15,

        "average_queries": 5,

        "average_actions": 3,

        "average_investigation_duration_minutes": 45,

        "short_note_rate": 10,

        "repeated_note_rate": 5,
    }


# ============================================================================
# Evidence
# ============================================================================


def test_evidence_discipline_high():

    score = calculate_evidence_discipline(
        alert_evidence_review_rate=100,
        investigation_evidence_review_rate=100,
        total_alerts=10,
        total_investigations=10,
    )

    assert score == 100


def test_evidence_discipline_low():

    score = calculate_evidence_discipline(
        alert_evidence_review_rate=20,
        investigation_evidence_review_rate=20,
        total_alerts=10,
        total_investigations=10,
    )

    assert score == 20


# ============================================================================
# Investigation depth
# ============================================================================


def test_investigation_depth_full_score():

    score = calculate_investigation_depth(
        average_queries=5,
        average_actions=3,
        average_duration_minutes=45,
        total_investigations=10,
    )

    assert score == 100


def test_investigation_depth_zero_without_investigations():

    score = calculate_investigation_depth(
        average_queries=5,
        average_actions=3,
        average_duration_minutes=45,
        total_investigations=0,
    )

    assert score == 0


# ============================================================================
# Closure behavior
# ============================================================================


def test_fast_closure_has_low_closure_behavior_score():

    score = calculate_closure_behavior(
        average_closure_time_minutes=5,
        closed_alerts=10,
    )

    assert score == 20


def test_normal_closure_has_high_score():

    score = calculate_closure_behavior(
        average_closure_time_minutes=35,
        closed_alerts=10,
    )

    assert score == 100


def test_no_closed_alerts_has_zero_score():

    score = calculate_closure_behavior(
        average_closure_time_minutes=35,
        closed_alerts=0,
    )

    assert score == 0


# ============================================================================
# Note quality
# ============================================================================


def test_note_quality_perfect():

    score = calculate_note_quality(
        short_note_rate=0,
        repeated_note_rate=0,
        total_investigations=10,
    )

    assert score == 100


def test_note_quality_decreases_with_short_notes():

    score = calculate_note_quality(
        short_note_rate=100,
        repeated_note_rate=0,
        total_investigations=10,
    )

    assert score == 40


def test_note_quality_decreases_with_repeated_notes():

    score = calculate_note_quality(
        short_note_rate=0,
        repeated_note_rate=100,
        total_investigations=10,
    )

    assert score == 60


# ============================================================================
# Overall quality
# ============================================================================


def test_investigation_quality_is_capped():

    score = calculate_investigation_quality(
        evidence_discipline_score=100,
        investigation_depth_score=100,
        escalation_discipline_score=100,
        closure_behavior_score=100,
        note_quality_score=100,
    )

    assert score == 100


# ============================================================================
# Confidence
# ============================================================================


def test_dna_confidence_low():

    assert (
        calculate_dna_confidence(1)
        == "Low"
    )


def test_dna_confidence_medium():

    assert (
        calculate_dna_confidence(5)
        == "Medium"
    )


def test_dna_confidence_high():

    assert (
        calculate_dna_confidence(10)
        == "High"
    )


# ============================================================================
# Full DNA
# ============================================================================


def test_build_investigation_dna():

    dna = build_investigation_dna(
        base_features()
    )

    assert isinstance(
        dna,
        InvestigationDNA,
    )

    assert (
        dna.analyst_id
        == "AN_TEST"
    )

    assert (
        dna.evidence_discipline_score
        == 90
    )

    assert (
        dna.investigation_depth_score
        == 100
    )

    assert (
        dna.closure_behavior_score
        == 100
    )

    assert (
        dna.note_quality_score
        == 92
    )

    assert (
        dna.investigation_quality_score
        > 0
    )

    assert (
        dna.confidence
        == "High"
    )


def test_build_dna_contains_metrics():

    dna = build_investigation_dna(
        base_features()
    )

    result = dna.to_dict()

    assert (
        result["analyst_id"]
        == "AN_TEST"
    )

    assert (
        "metrics"
        in result
    )

    assert (
        "indicators"
        in result
    )

    assert (
        "investigation_quality_score"
        in result
    )


def test_dna_handles_missing_values():

    features = {
        "analyst_id": "AN_EMPTY",

        "total_alerts": 0,

        "closed_alerts": 0,

        "total_investigations": 0,
    }

    dna = build_investigation_dna(
        features
    )

    assert (
        dna.analyst_id
        == "AN_EMPTY"
    )

    assert (
        dna.investigation_depth_score
        == 0
    )

    assert (
        dna.note_quality_score
        == 0
    )

    assert (
        dna.investigation_quality_score
        >= 0
    )

    def test_dna_can_be_used_with_analyst_metrics_shape():

        features = {
            "analyst_id": "AN22005",

            "total_alerts": 5,

            "closed_alerts": 5,

            "average_closure_time_minutes": 6,

            "evidence_review_rate": 20,

            "investigation_evidence_review_rate": 30,

            "escalation_rate": 0,

            "investigation_escalation_rate": 0,

            "total_investigations": 5,

            "average_queries": 1,

            "average_actions": 1,

            "average_investigation_duration_minutes": 5,

            "short_note_rate": 70,

            "repeated_note_rate": 60,
        }

        dna = build_investigation_dna(
            features
        )

        assert dna.analyst_id == "AN22005"

        assert (
            dna.investigation_quality_score
            < 60
        )

        assert (
            dna.closure_behavior_score
            == 20
        )

        assert (
            dna.note_quality_score
            == 30
        )

        assert (
            len(dna.indicators)
            > 0
    )