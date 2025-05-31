#!/usr/bin/env python3
"""
Quick test for the negation fix implementation
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from kimera.geoid import init_geoid
from kimera.resonance import resonance, negation_mismatch

def test_negation_detection():
    """Test the negation detection logic"""
    print("Testing negation detection...")
    
    # Test cases
    test_cases = [
        ("Birds can fly", "Birds cannot fly", True),  # Should detect mismatch
        ("Snow is white", "Snow is black", False),    # No negation mismatch
        ("I like cats", "I don't like cats", True),   # Should detect mismatch
        ("The sky is blue", "The ocean is blue", False),  # No negation
    ]
    
    for text1, text2, expected in test_cases:
        result = negation_mismatch(text1, text2)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{text1}' vs '{text2}' -> {result} (expected {expected})")
    
    print()

def test_resonance_with_negation():
    """Test resonance function with negation penalty"""
    print("Testing resonance with negation penalty...")
    
    # Create test geoids
    geoid1 = init_geoid("Birds can fly", "en", ["test"], raw="Birds can fly")
    geoid2 = init_geoid("Birds cannot fly", "en", ["test"], raw="Birds cannot fly")
    geoid3 = init_geoid("Snow is white", "en", ["test"], raw="Snow is white")
    geoid4 = init_geoid("Snow is black", "en", ["test"], raw="Snow is black")
    
    # Test resonance scores
    score_negation = resonance(geoid1, geoid2)  # Should have penalty
    score_no_negation = resonance(geoid3, geoid4)  # No penalty
    
    print(f"Resonance (with negation): {score_negation:.3f}")
    print(f"Resonance (without negation): {score_no_negation:.3f}")
    print(f"Negation penalty applied: {score_negation < score_no_negation}")
    print()

if __name__ == "__main__":
    test_negation_detection()
    test_resonance_with_negation()
    print("Negation fix test completed!")