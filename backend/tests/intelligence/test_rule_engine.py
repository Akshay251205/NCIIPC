from app.services.rules.rule_engine import (
    FastClosureRule,
    FindingSignal,
    NoEscalationRule,
    NoEvidenceRule,
    RepeatedNotesRule,
    RuleEngine,
    ShallowInvestigationRule,
    ShortNotesRule,
    VeryShortInvestigationRule,
)


def base_features() -> dict:
    """
    Create a normal analyst record for testing.

    Individual tests modify only the field
    relevant to that test.
    """

    return {
        "analyst_id": "AN_TEST",

        "total_alerts": 10,

        "closed_alerts": 8,

        "average_closure_time_minutes": 30,

        "evidence_review_rate": 90,

        "escalation_rate": 50,

        "total_investigations": 8,

        "average_queries": 5,

        "average_investigation_duration_minutes": 40,

        "short_note_rate": 10,

        "repeated_note_rate": 10,
    }


# ============================================================================
# FindingSignal
# ============================================================================


def test_finding_signal_to_dict():

    signal = FindingSignal(
        rule_id="TEST_RULE",
        category="TEST",
        severity="HIGH",
        score=25,
        entity_type="ANALYST",
        entity_id="AN001",
        title="Test Finding",
        reason="Testing finding generation.",
    )

    result = signal.to_dict()

    assert result["rule_id"] == "TEST_RULE"

    assert result["severity"] == "HIGH"

    assert result["score"] == 25

    assert result["entity_id"] == "AN001"

    assert "evidence" in result


# ============================================================================
# Fast Closure
# ============================================================================


def test_fast_closure_triggers():

    features = base_features()

    features[
        "average_closure_time_minutes"
    ] = 5

    signal = FastClosureRule().evaluate(
        features
    )

    assert signal is not None

    assert signal.rule_id == "FAST_CLOSURE"

    assert signal.score == 30

    assert (
        signal.entity_id
        == "AN_TEST"
    )


def test_fast_closure_does_not_trigger():

    features = base_features()

    features[
        "average_closure_time_minutes"
    ] = 20

    signal = FastClosureRule().evaluate(
        features
    )

    assert signal is None


# ============================================================================
# No Evidence
# ============================================================================


def test_no_evidence_triggers():

    features = base_features()

    features[
        "evidence_review_rate"
    ] = 20

    signal = NoEvidenceRule().evaluate(
        features
    )

    assert signal is not None

    assert signal.rule_id == "NO_EVIDENCE"

    assert signal.score == 20


def test_no_evidence_does_not_trigger():

    features = base_features()

    features[
        "evidence_review_rate"
    ] = 80

    signal = NoEvidenceRule().evaluate(
        features
    )

    assert signal is None


# ============================================================================
# No Escalation
# ============================================================================


def test_no_escalation_triggers():

    features = base_features()

    features[
        "escalation_rate"
    ] = 0

    signal = NoEscalationRule().evaluate(
        features
    )

    assert signal is not None

    assert signal.rule_id == "NO_ESCALATION"


def test_no_escalation_requires_two_alerts():

    features = base_features()

    features[
        "total_alerts"
    ] = 1

    features[
        "escalation_rate"
    ] = 0

    signal = NoEscalationRule().evaluate(
        features
    )

    assert signal is None


# ============================================================================
# Shallow Investigation
# ============================================================================


def test_shallow_investigation_triggers():

    features = base_features()

    features[
        "average_queries"
    ] = 1

    signal = (
        ShallowInvestigationRule()
        .evaluate(features)
    )

    assert signal is not None

    assert (
        signal.rule_id
        == "SHALLOW_INVESTIGATION"
    )


def test_shallow_investigation_does_not_trigger():

    features = base_features()

    features[
        "average_queries"
    ] = 5

    signal = (
        ShallowInvestigationRule()
        .evaluate(features)
    )

    assert signal is None


# ============================================================================
# Short Notes
# ============================================================================


def test_short_notes_triggers():

    features = base_features()

    features[
        "short_note_rate"
    ] = 70

    signal = (
        ShortNotesRule()
        .evaluate(features)
    )

    assert signal is not None

    assert (
        signal.rule_id
        == "SHORT_NOTES"
    )


def test_short_notes_does_not_trigger():

    features = base_features()

    features[
        "short_note_rate"
    ] = 20

    signal = (
        ShortNotesRule()
        .evaluate(features)
    )

    assert signal is None


# ============================================================================
# Repeated Notes
# ============================================================================


def test_repeated_notes_triggers():

    features = base_features()

    features[
        "repeated_note_rate"
    ] = 70

    signal = (
        RepeatedNotesRule()
        .evaluate(features)
    )

    assert signal is not None

    assert (
        signal.rule_id
        == "REPEATED_NOTES"
    )


def test_repeated_notes_does_not_trigger():

    features = base_features()

    features[
        "repeated_note_rate"
    ] = 20

    signal = (
        RepeatedNotesRule()
        .evaluate(features)
    )

    assert signal is None


# ============================================================================
# Very Short Investigations
# ============================================================================


def test_very_short_investigation_triggers():

    features = base_features()

    features[
        "average_investigation_duration_minutes"
    ] = 5

    signal = (
        VeryShortInvestigationRule()
        .evaluate(features)
    )

    assert signal is not None

    assert (
        signal.rule_id
        == "VERY_SHORT_INVESTIGATION"
    )


def test_very_short_investigation_does_not_trigger():

    features = base_features()

    features[
        "average_investigation_duration_minutes"
    ] = 30

    signal = (
        VeryShortInvestigationRule()
        .evaluate(features)
    )

    assert signal is None


# ============================================================================
# Rule Engine
# ============================================================================


def test_rule_engine_returns_multiple_signals():

    features = base_features()

    features[
        "average_closure_time_minutes"
    ] = 5

    features[
        "evidence_review_rate"
    ] = 20

    features[
        "escalation_rate"
    ] = 0

    features[
        "average_queries"
    ] = 1

    features[
        "average_investigation_duration_minutes"
    ] = 5

    features[
        "short_note_rate"
    ] = 70

    features[
        "repeated_note_rate"
    ] = 70

    engine = RuleEngine()

    signals = engine.evaluate(
        features
    )

    rule_ids = {
        signal.rule_id
        for signal in signals
    }

    assert "FAST_CLOSURE" in rule_ids

    assert "NO_EVIDENCE" in rule_ids

    assert "NO_ESCALATION" in rule_ids

    assert (
        "SHALLOW_INVESTIGATION"
        in rule_ids
    )

    assert (
        "SHORT_NOTES"
        in rule_ids
    )

    assert (
        "REPEATED_NOTES"
        in rule_ids
    )

    assert (
        "VERY_SHORT_INVESTIGATION"
        in rule_ids
    )


def test_rule_engine_score_is_capped_at_100():

    features = base_features()

    features[
        "average_closure_time_minutes"
    ] = 5

    features[
        "evidence_review_rate"
    ] = 20

    features[
        "escalation_rate"
    ] = 0

    features[
        "average_queries"
    ] = 1

    features[
        "average_investigation_duration_minutes"
    ] = 5

    features[
        "short_note_rate"
    ] = 80

    features[
        "repeated_note_rate"
    ] = 80

    engine = RuleEngine()

    signals = engine.evaluate(
        features
    )

    score = engine.calculate_score(
        signals
    )

    assert score == 100


def test_rule_engine_no_findings_for_normal_analyst():

    features = base_features()

    engine = RuleEngine()

    signals = engine.evaluate(
        features
    )

    assert signals == []


def test_rule_engine_summary():

    features = base_features()

    features[
        "average_closure_time_minutes"
    ] = 5

    engine = RuleEngine()

    result = engine.summary(
        features
    )

    assert result["score"] == 30

    assert (
        "FAST_CLOSURE"
        in result["triggered_rules"]
    )

    assert (
        "Suspiciously Fast Alert Closure"
        in result["indicators"]
    )


def test_rule_engine_evaluate_many():

    analyst_one = base_features()

    analyst_one[
        "analyst_id"
    ] = "AN001"

    analyst_one[
        "average_closure_time_minutes"
    ] = 5

    analyst_two = base_features()

    analyst_two[
        "analyst_id"
    ] = "AN002"

    analyst_two[
        "evidence_review_rate"
    ] = 20

    engine = RuleEngine()

    signals = engine.evaluate_many(
        [
            analyst_one,
            analyst_two,
        ]
    )

    assert len(signals) == 2

    ids = {
        signal.entity_id
        for signal in signals
    }

    assert "AN001" in ids

    assert "AN002" in ids


def test_rule_engine_logs_and_isolates_rule_failure(caplog):
    class BrokenRule:
        rule_id = "BROKEN_RULE"

        def evaluate(self, features):
            raise RuntimeError("intentional test failure")

    caplog.set_level("ERROR")
    result = RuleEngine(rules=[BrokenRule()]).evaluate(base_features())

    assert result == []
    assert "Rule execution failed" in caplog.text
    assert caplog.records[0].rule == "BROKEN_RULE"
    assert caplog.records[0].analyst_id == "AN_TEST"
