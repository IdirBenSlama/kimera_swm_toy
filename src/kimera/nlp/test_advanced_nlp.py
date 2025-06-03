"""
Advanced test suite for the Kimera NLP pattern extraction module.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from kimera.nlp import (
    extract_patterns,
    extract_comprehensive_patterns,
    PatternExtractor,
    SemanticPatternExtractor,
    PatternVisualizer,
    ensure_spacy_model
)

def test_empty_input():
    """Test all extractors with empty input."""
    assert extract_patterns("") == {"entities": [], "noun_chunks": []}
    extractor = PatternExtractor()
    assert extractor.extract_all_patterns("") == {
        "token_patterns": [],
        "dependency_patterns": [],
        "syntactic_patterns": {
            "noun_phrases": [],
            "verb_phrases": [],
            "prepositional_phrases": []
        },
        "semantic_roles": []
    }

def test_non_english_text():
    """Test with non-English input (should not crash, may return empty or partial results)."""
    text = "これは日本語の文章です��"
    patterns = extract_patterns(text)
    assert isinstance(patterns, dict)
    extractor = PatternExtractor()
    adv = extractor.extract_all_patterns(text)
    assert isinstance(adv, dict)

def test_long_text():
    """Test with a long text input."""
    text = " ".join(["Natural language processing is powerful."] * 1000)
    patterns = extract_patterns(text)
    assert "entities" in patterns and "noun_chunks" in patterns
    extractor = PatternExtractor()
    adv = extractor.extract_all_patterns(text)
    assert "token_patterns" in adv

def test_custom_token_pattern():
    """Test adding and extracting a custom token pattern."""
    extractor = PatternExtractor()
    extractor.add_token_pattern(
        "CUSTOM_PATTERN",
        [{"LOWER": "kimera"}, {"POS": "NOUN"}],
        "Kimera followed by a noun"
    )
    text = "Kimera system is an advanced platform."
    matches = extractor.extract_token_patterns(text)
    assert any(m["pattern"] == "CUSTOM_PATTERN" for m in matches)

def test_dependency_pattern_extraction():
    """Test dependency pattern extraction for SVO."""
    extractor = PatternExtractor()
    text = "The scientist invented a new device."
    dep_matches = extractor.extract_dependency_patterns(text)
    assert isinstance(dep_matches, list)
    # Should find at least one SVO pattern
    assert any(m["pattern"] == "SUBJ_VERB_OBJ" for m in dep_matches)

def test_semantic_extractor_full():
    """Test all semantic extractor features (if model available)."""
    try:
        extractor = SemanticPatternExtractor()
        text = (
            "AI and machine learning are related to data science. "
            "Deep learning is a subset of machine learning."
        )
        # Similarity
        similar = extractor.find_similar_phrases(text, "machine learning")
        assert isinstance(similar, list)
        # Clusters
        clusters = extractor.extract_semantic_clusters(text)
        assert isinstance(clusters, list)
        # Analogies
        analogies = extractor.find_analogies(text, ("man", "king", "woman"))
        assert isinstance(analogies, list)
        # Concept patterns
        concepts = extractor.extract_concept_patterns(text, ["technology", "science"])
        assert isinstance(concepts, dict)
    except (RuntimeError, ValueError):
        pytest.skip("SemanticPatternExtractor requires medium/large spaCy model.")

def test_visualization_outputs(tmp_path):
    """Test visualization HTML and JSON outputs."""
    visualizer = PatternVisualizer()
    extractor = PatternExtractor()
    text = "The AI system analyzed data."
    patterns = extractor.extract_all_patterns(text)
    # Dependency HTML
    dep_html = visualizer.visualize_dependencies(text)
    assert dep_html.strip().startswith("<div")
    # Entity HTML
    ent_html = visualizer.visualize_entities(text)
    assert ent_html.strip().startswith("<div")
    # Report
    report_path = tmp_path / "report.html"
    html = visualizer.generate_pattern_report(text, patterns, str(report_path))
    assert report_path.exists() and html.startswith("<!DOCTYPE html>")
    # JSON export
    json_path = tmp_path / "patterns.json"
    visualizer.export_patterns_json(patterns, str(json_path))
    assert json_path.exists()

def test_error_handling_missing_model(monkeypatch):
    """Test error handling when spaCy model is missing."""
    def fake_load(name):
        raise OSError("Model not found")
    monkeypatch.setattr("spacy.load", fake_load)
    with pytest.raises(RuntimeError):
        ensure_spacy_model("en_core_web_sm")

def test_extract_comprehensive_patterns_semantic(monkeypatch):
    """Test extract_comprehensive_patterns with semantic extraction error."""
    def fake_semantic(*args, **kwargs):
        raise ValueError("No vectors")
    monkeypatch.setattr("kimera.nlp.SemanticPatternExtractor", lambda *a, **k: type("Fake", (), {"extract_all_semantic_patterns": fake_semantic})())
    text = "AI is transforming technology."
    result = extract_comprehensive_patterns(text, include_semantic=True)
    assert "semantic_error" in result

def test_pattern_statistics():
    """Test pattern statistics generation."""
    visualizer = PatternVisualizer()
    extractor = PatternExtractor()
    text = "The AI system analyzed data."
    patterns = extractor.extract_all_patterns(text)
    stats = visualizer.generate_pattern_statistics(patterns)
    assert "total_patterns" in stats and "pattern_types" in stats

if __name__ == "__main__":
    pytest.main([__file__])
