#!/usr/bin/env python3
"""
Simple test of negation detection on sample data
"""
import sys
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from kimera.resonance import negation_mismatch

def test_on_sample_data():
    """Test negation detection on actual dataset samples"""
    print("Testing negation detection on sample data...")
    
    # Load a small sample from the dataset
    try:
        df = pd.read_csv("data/mixed_quick.csv")
        print(f"Loaded {len(df)} pairs from mixed_quick.csv")
        
        negation_cases = []
        
        for idx, row in df.head(20).iterrows():  # Test first 20 pairs
            text1 = row['text1']
            text2 = row['text2']
            label = row['label']  # True = contradiction
            
            has_negation_mismatch = negation_mismatch(text1, text2)
            
            if has_negation_mismatch:
                negation_cases.append((text1, text2, label))
                print(f"Negation detected: '{text1}' vs '{text2}' (label: {label})")
        
        print(f"\nFound {len(negation_cases)} pairs with negation mismatches")
        
        if negation_cases:
            print("\nAnalysis:")
            correct_negations = sum(1 for _, _, label in negation_cases if label)
            print(f"  Correctly identified contradictions: {correct_negations}/{len(negation_cases)}")
            print(f"  Accuracy on negation cases: {100 * correct_negations / len(negation_cases):.1f}%")
        
    except FileNotFoundError:
        print("mixed_quick.csv not found. Testing with hardcoded examples...")
        
        test_cases = [
            ("Birds can fly", "Birds cannot fly", True),
            ("Snow is white", "Snow is black", False),
            ("I like cats", "I don't like cats", True),
            ("The sky is blue", "The ocean is blue", False),
            ("Fire is hot", "Fire is not hot", True),
            ("Water boils at 100°C", "Water boils at 50°C", False),
        ]
        
        print("Testing hardcoded examples:")
        for text1, text2, expected_contradiction in test_cases:
            has_negation = negation_mismatch(text1, text2)
            status = "✓" if (has_negation and expected_contradiction) or (not has_negation and not expected_contradiction) else "?"
            print(f"{status} '{text1}' vs '{text2}' -> negation: {has_negation}, contradiction: {expected_contradiction}")

if __name__ == "__main__":
    test_on_sample_data()