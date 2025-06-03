"""
Test script for the enhanced NLP pattern extraction module.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from kimera.nlp import (
    extract_patterns,
    extract_comprehensive_patterns,
    PatternExtractor,
    SemanticPatternExtractor,
    PatternVisualizer
)


def test_basic_extraction():
    """Test basic pattern extraction."""
    print("Testing basic pattern extraction...")
    
    text = "Microsoft acquired GitHub for $7.5 billion in 2018."
    patterns = extract_patterns(text)
    
    assert "entities" in patterns
    assert "noun_chunks" in patterns
    assert len(patterns["entities"]) > 0
    
    print("✓ Basic extraction test passed")
    return patterns


def test_pattern_extractor():
    """Test PatternExtractor class."""
    print("\nTesting PatternExtractor...")
    
    extractor = PatternExtractor()
    text = "The developer wrote clean code for the project."
    
    # Test token patterns
    token_patterns = extractor.extract_token_patterns(text)
    print(f"  Found {len(token_patterns)} token patterns")
    
    # Test syntactic patterns
    syntactic = extractor.extract_syntactic_patterns(text)
    assert "noun_phrases" in syntactic
    assert "verb_phrases" in syntactic
    
    print("✓ PatternExtractor test passed")
    return syntactic


def test_comprehensive_extraction():
    """Test comprehensive pattern extraction."""
    print("\nTesting comprehensive extraction...")
    
    text = (
        "Google's AI research team published groundbreaking papers. "
        "The team developed new algorithms for natural language understanding."
    )
    
    patterns = extract_comprehensive_patterns(text, include_semantic=False)
    
    assert "basic" in patterns
    assert "advanced" in patterns
    assert "entities" in patterns["basic"]
    
    print("✓ Comprehensive extraction test passed")
    return patterns


def test_visualizer():
    """Test PatternVisualizer class."""
    print("\nTesting PatternVisualizer...")
    
    visualizer = PatternVisualizer()
    text = "The data scientist analyzed complex patterns."
    
    # Test dependency visualization
    dep_html = visualizer.visualize_dependencies(text)
    assert len(dep_html) > 0
    assert "svg" in dep_html.lower()
    
    # Test entity visualization
    ent_html = visualizer.visualize_entities("Apple Inc. was founded by Steve Jobs.")
    assert len(ent_html) > 0
    
    print("✓ PatternVisualizer test passed")


def test_semantic_extractor():
    """Test SemanticPatternExtractor (if medium/large model available)."""
    print("\nTesting SemanticPatternExtractor...")
    
    try:
        extractor = SemanticPatternExtractor()
        text = "Machine learning and artificial intelligence are transforming technology."
        
        # Test semantic clusters
        clusters = extractor.extract_semantic_clusters(text)
        print(f"  Found {len(clusters)} semantic clusters")
        
        # Test concept patterns
        concepts = extractor.extract_concept_patterns(text, ["technology", "science"])
        print(f"  Extracted patterns for {len(concepts)} concepts")
        
        print("✓ SemanticPatternExtractor test passed")
        return True
        
    except (RuntimeError, ValueError) as e:
        print(f"⚠ SemanticPatternExtractor skipped: {e}")
        print("  (This is expected if only small model is installed)")
        return False


def run_all_tests():
    """Run all tests."""
    print("Running NLP module tests...\n")
    
    try:
        # Run tests
        basic_result = test_basic_extraction()
        pattern_result = test_pattern_extractor()
        comprehensive_result = test_comprehensive_extraction()
        test_visualizer()
        semantic_available = test_semantic_extractor()
        
        print("\n" + "=" * 60)
        print("All tests completed successfully!")
        print("=" * 60)
        
        # Summary
        print("\nModule capabilities:")
        print("- Basic pattern extraction: ✓")
        print("- Advanced pattern matching: ✓")
        print("- Syntactic pattern extraction: ✓")
        print("- Pattern visualization: ✓")
        print(f"- Semantic pattern extraction: {'✓' if semantic_available else '⚠ (requires medium/large model)'}")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)