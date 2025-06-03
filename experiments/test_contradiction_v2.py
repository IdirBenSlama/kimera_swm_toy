"""
Comprehensive Test Suite for Contradiction Detection V2
======================================================

Tests the redesigned contradiction detection against known examples.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from kimera.geoid import init_geoid
from kimera.contradiction_v2 import analyze_contradiction, ContradictionDetectorV2


def run_test_suite():
    """Run comprehensive tests on contradiction detection."""
    
    # Test cases: (text1, text2, expected_contradiction, test_name)
    test_cases = [
        # Negation contradictions
        ("The sky is blue", "The sky is not blue", True, "Direct negation"),
        ("It is raining", "It is not raining", True, "Simple negation"),
        ("All birds can fly", "Not all birds can fly", True, "Quantifier negation"),
        ("Nobody likes taxes", "Somebody likes taxes", True, "Nobody/somebody"),
        
        # Antonym contradictions
        ("The sky is blue", "The sky is red", True, "Color antonyms"),
        ("The water is hot", "The water is cold", True, "Temperature antonyms"),
        ("The answer is true", "The answer is false", True, "Boolean antonyms"),
        ("The box is open", "The box is closed", True, "State antonyms"),
        
        # Mutual exclusions
        ("The light is on", "The light is off", True, "Binary states"),
        ("The substance is solid", "The substance is liquid", True, "Matter states"),
        ("We're going north", "We're going south", True, "Directions"),
        
        # NOT contradictions (unrelated)
        ("The sky is blue", "Grass is green", False, "Unrelated facts"),
        ("I like pizza", "Birds can fly", False, "Completely unrelated"),
        ("Mathematics is beautiful", "The weather is sunny", False, "Different domains"),
        
        # NOT contradictions (compatible)
        ("The sky is blue", "The sky is beautiful", False, "Compatible descriptions"),
        ("Some birds can fly", "Eagles can fly", False, "General and specific"),
        ("Water is wet", "Water is a liquid", False, "Related properties"),
        
        # Edge cases
        ("This statement is true", "This statement is false", True, "Liar paradox"),
        ("A and B", "A and not B", True, "Logical contradiction"),
        ("X equals 5", "X equals 10", True, "Mathematical contradiction"),
    ]
    
    print("Contradiction Detection V2 Test Suite")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for text1, text2, expected, test_name in test_cases:
        g1 = init_geoid(text1)
        g2 = init_geoid(text2)
        
        analysis = analyze_contradiction(g1, g2)
        
        # Check if result matches expectation
        if analysis.is_contradiction == expected:
            passed += 1
            status = "✓ PASS"
        else:
            failed += 1
            status = "✗ FAIL"
        
        print(f"\n{status} - {test_name}")
        print(f"  Text 1: '{text1}'")
        print(f"  Text 2: '{text2}'")
        print(f"  Expected: {expected}, Got: {analysis.is_contradiction}")
        print(f"  Confidence: {analysis.confidence:.3f}")
        print(f"  Type: {analysis.contradiction_type}")
        print(f"  Reasoning: {analysis.reasoning}")
        
        if analysis.shared_topic:
            print(f"  Shared topic: {analysis.shared_topic}")
        if analysis.opposing_claims:
            print(f"  Opposing claims: {analysis.opposing_claims}")
    
    # Summary
    print("\n" + "=" * 70)
    print(f"SUMMARY: {passed}/{len(test_cases)} tests passed ({passed/len(test_cases)*100:.1f}%)")
    
    if failed > 0:
        print(f"Failed tests: {failed}")
    else:
        print("All tests passed! ✓")
    
    return passed, failed


def test_edge_cases():
    """Test specific edge cases and complex scenarios."""
    print("\n\nEdge Case Testing")
    print("=" * 70)
    
    detector = ContradictionDetectorV2()
    
    # Test subject/predicate extraction
    test_sentences = [
        "The sky is blue",
        "Birds can fly",
        "Democracy has flaws",
        "This statement is false",
        "Water freezes at 0 degrees",
    ]
    
    print("\nSubject/Predicate Extraction:")
    for sent in test_sentences:
        subj, pred = detector.extract_subject_predicate(sent)
        print(f"  '{sent}' → Subject: '{subj}', Predicate: '{pred}'")
    
    # Test similarity detection
    print("\n\nContent Similarity Tests:")
    pairs = [
        ("The sky is blue", "The sky is not blue"),
        ("The cat is black", "A dog is white"),
        ("Democracy is good", "Democracy is flawed"),
    ]
    
    for t1, t2 in pairs:
        similar = detector._similar_content(t1.lower(), t2.lower())
        print(f"  '{t1}' ~ '{t2}': {similar}")


def test_performance():
    """Test performance with larger corpus."""
    print("\n\nPerformance Testing")
    print("=" * 70)
    
    import time
    
    # Generate test corpus
    templates = [
        "The {} is {}",
        "{} can {}",
        "All {} are {}",
        "{} is not {}",
    ]
    
    subjects = ["sky", "water", "fire", "earth", "wind"]
    properties = ["blue", "red", "hot", "cold", "fast", "slow"]
    
    texts = []
    for template in templates:
        for subj in subjects:
            for prop in properties:
                if "{}" in template:
                    text = template.format(subj, prop)
                    texts.append(text)
    
    geoids = [init_geoid(t) for t in texts[:50]]  # Limit for speed
    
    print(f"Testing with {len(geoids)} geoids...")
    
    start = time.time()
    contradictions = 0
    
    for i in range(len(geoids)):
        for j in range(i + 1, len(geoids)):
            analysis = analyze_contradiction(geoids[i], geoids[j])
            if analysis.is_contradiction:
                contradictions += 1
    
    elapsed = time.time() - start
    total_pairs = len(geoids) * (len(geoids) - 1) // 2
    
    print(f"Analyzed {total_pairs} pairs in {elapsed:.2f} seconds")
    print(f"Found {contradictions} contradictions")
    print(f"Rate: {total_pairs/elapsed:.1f} pairs/second")


def main():
    """Run all tests."""
    # Basic test suite
    passed, failed = run_test_suite()
    
    # Edge cases
    test_edge_cases()
    
    # Performance
    test_performance()
    
    # Final verdict
    print("\n" + "=" * 70)
    if failed == 0:
        print("✅ CONTRADICTION DETECTION V2: ALL TESTS PASSED")
        print("The new implementation correctly identifies contradictions!")
    else:
        print(f"⚠️  CONTRADICTION DETECTION V2: {failed} TESTS FAILED")
        print("Further refinement needed.")


if __name__ == "__main__":
    main()