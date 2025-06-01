"""
Quick test to verify Kimera is working correctly
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from kimera.api import Kimera

def test_kimera():
    """Run quick tests on all major functions."""
    
    print("Testing Kimera functionality...\n")
    
    kimera = Kimera()
    
    # Test 1: Resonance
    print("1. Testing Resonance Detection:")
    res = kimera.find_resonance(
        "The river flows to the ocean",
        "Information flows through networks"
    )
    print(f"   ✓ Resonance score: {res['score']:.3f}")
    assert res['score'] > 0.5, "Expected moderate resonance"
    
    # Test 2: Contradiction
    print("\n2. Testing Contradiction Detection:")
    contra = kimera.detect_contradiction(
        "It is raining",
        "It is not raining"
    )
    print(f"   ✓ Contradiction detected: {contra['is_contradiction']}")
    assert contra['is_contradiction'] == True, "Expected contradiction"
    
    # Test 3: Pattern Extraction
    print("\n3. Testing Pattern Extraction:")
    patterns = kimera.extract_patterns(
        "The CEO leads the company"
    )
    print(f"   ✓ Patterns found: {len(patterns)}")
    assert len(patterns) > 0, "Expected at least one pattern"
    
    # Test 4: Cross-domain insights
    print("\n4. Testing Cross-Domain Insights:")
    insights = kimera.find_cross_domain_insights(
        "How to organize information",
        ["Trees have hierarchical branches", "Libraries use classification systems"],
        threshold=0.3
    )
    print(f"   ✓ Insights found: {len(insights)}")
    
    print("\n✅ All tests passed! Kimera is working correctly.")

if __name__ == "__main__":
    test_kimera()