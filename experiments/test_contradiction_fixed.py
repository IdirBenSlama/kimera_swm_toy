"""
Test the fixed contradiction detection
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from kimera.geoid import init_geoid
from kimera.contradiction_v2_fixed import analyze_contradiction


def test_basic_contradictions():
    """Test basic contradiction cases."""
    test_cases = [
        # Should detect contradictions
        ("The sky is blue", "The sky is not blue", True),
        ("The sky is blue", "The sky is red", True),
        ("It is raining", "It is not raining", True),
        ("The light is on", "The light is off", True),
        
        # Should NOT detect contradictions
        ("The sky is blue", "Grass is green", False),
        ("I like pizza", "Birds can fly", False),
        ("The sky is blue", "The sky is beautiful", False),
    ]
    
    print("Testing Fixed Contradiction Detection")
    print("=" * 60)
    
    passed = 0
    for text1, text2, expected in test_cases:
        g1 = init_geoid(text1)
        g2 = init_geoid(text2)
        
        analysis = analyze_contradiction(g1, g2)
        result = analysis.is_contradiction
        
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"\n{status} - '{text1}' vs '{text2}'")
        print(f"  Expected: {expected}, Got: {result}")
        print(f"  Confidence: {analysis.confidence:.3f}")
        print(f"  Type: {analysis.contradiction_type}")
        print(f"  Reasoning: {analysis.reasoning}")
        
        if result == expected:
            passed += 1
    
    print(f"\nSUMMARY: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


if __name__ == "__main__":
    success = test_basic_contradictions()
    if success:
        print("\n✅ Fixed contradiction detection works!")
    else:
        print("\n❌ Still has issues")