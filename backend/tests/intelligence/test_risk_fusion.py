from app.services.risk.risk_fusion import (
    calculate_ai_risk,
    calculate_risk_fusion,
    risk_level,
)


def test_risk_level_thresholds():
    assert risk_level(0) == "LOW"
    assert risk_level(39.99) == "LOW"
    assert risk_level(40) == "MEDIUM"
    assert risk_level(59.99) == "MEDIUM"
    assert risk_level(60) == "HIGH"
    assert risk_level(79.99) == "HIGH"
    assert risk_level(80) == "CRITICAL"


def test_rule_only_fusion():
    result = calculate_risk_fusion(
        analyst_id="AN001",
        rule_score=100,
    )

    assert result.score == 100
    assert result.level == "CRITICAL"
    assert result.components["rule"] == 100


def test_full_weighted_fusion():
    result = calculate_risk_fusion(
        analyst_id="AN001",
        rule_score=80,
        behavioral_anomaly_score=60,
        gaming_score=50,
        nlp_score=40,
        investigation_dna_quality=20,
        negative_space_score=70,
        peer_score=50,
        observations=20,
        component_confidences=[
            "High",
            "High",
            "Medium",
            "High",
        ],
    )

    assert 0 <= result.score <= 100

    assert result.components["rule"] == 80
    assert result.components["negative_space"] == 70
    assert result.components["peer"] == 50

    assert result.level in {
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL",
    }


def test_missing_optional_components_are_renormalized():
    result = calculate_risk_fusion(
        analyst_id="AN001",
        rule_score=80,
        behavioral_anomaly_score=60,
        negative_space_score=None,
        peer_score=None,
    )

    assert result.score > 0
    assert result.components["negative_space"] is None
    assert result.components["peer"] is None


def test_zero_scores_produce_low_risk():
    result = calculate_risk_fusion(
        analyst_id="AN001",
        rule_score=0,
        behavioral_anomaly_score=0,
        gaming_score=0,
        nlp_score=0,
        investigation_dna_quality=100,
        negative_space_score=0,
        peer_score=0,
    )

    assert result.score == 0
    assert result.level == "LOW"


def test_high_behavioral_signals_raise_ai_risk():
    score, components = calculate_ai_risk(
        behavioral_anomaly_score=100,
        gaming_score=100,
        nlp_score=100,
        investigation_dna_quality=0,
    )

    assert score == 100
    assert components["behavioral_anomaly"] == 100
    assert components["gaming"] == 100
    assert components["nlp"] == 100
    assert components["investigation_dna_risk"] == 100


def test_dna_quality_is_inverted_for_risk():
    score, components = calculate_ai_risk(
        behavioral_anomaly_score=0,
        gaming_score=0,
        nlp_score=0,
        investigation_dna_quality=100,
    )

    assert score == 0
    assert components["investigation_dna_risk"] == 0


def test_indicators_are_deduplicated():
    result = calculate_risk_fusion(
        analyst_id="AN001",
        rule_score=60,
        rule_indicators=[
            "Fast closure",
            "Low evidence review",
        ],
        gaming_indicators=[
            "Fast closure",
            "Low evidence review",
            "Short investigation",
        ],
    )

    assert result.indicators.count(
        "Fast closure"
    ) == 1

    assert result.indicators.count(
        "Low evidence review"
    ) == 1

    assert "Short investigation" in result.indicators


def test_explanation_contains_final_risk():
    result = calculate_risk_fusion(
        analyst_id="AN001",
        rule_score=80,
        behavioral_anomaly_score=70,
        gaming_score=60,
        nlp_score=50,
        negative_space_score=80,
        peer_score=70,
    )

    assert "Final supervisory risk" in result.explanation
    assert result.explanation


def test_signal_sources_are_present():
    result = calculate_risk_fusion(
        analyst_id="AN001",
        rule_score=50,
        behavioral_anomaly_score=50,
        negative_space_score=50,
        peer_score=50,
    )

    sources = [
        signal["source"]
        for signal in result.signals
    ]

    assert "rule" in sources
    assert "behavioral" in sources
    assert "negative_space" in sources
    assert "peer" in sources


def test_negative_space_flows_into_risk_fusion():
    result = calculate_risk_fusion(
        analyst_id="AN001",
        rule_score=0,
        negative_space_score=80,
        negative_space_indicators=[
            "No monitoring activity record",
        ],
    )

    assert result.components["negative_space"] == 80
    assert "No monitoring activity record" in result.indicators
    assert any(
        signal["source"] == "negative_space"
        for signal in result.signals
    )
