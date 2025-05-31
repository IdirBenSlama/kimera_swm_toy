#!/usr/bin/env python3
"""
Focused experiment to validate negation fix
"""
import os
import sys
import csv
from pathlib import Path

# Add src to path
sys.path.insert(0, 'src')

def test_negation_cases():
    """Test specific negation cases"""
    print("🎯 Testing Negation Cases")
    print("=" * 30)
    
    # Test cases with clear negation patterns
    test_cases = [
        ("Birds can fly", "Birds cannot fly", True),      # Clear negation
        ("I like cats", "I don't like cats", True),       # Contraction negation
        ("Water is hot", "Water is not hot", True),       # Simple negation
        ("Fire is hot", "Fire is cold", False),           # Antonym, not negation
        ("Snow is white", "Snow is black", False),        # Different property
        ("Paris is in France", "Paris is in Germany", False),  # Different location
    ]
    
    results = []
    
    for negation_enabled in [False, True]:
        print(f"\n{'='*20}")
        print(f"Negation Fix: {'ON' if negation_enabled else 'OFF'}")
        print(f"{'='*20}")
        
        # Set environment
        os.environ["KIMERA_NEGATION_FIX"] = "1" if negation_enabled else "0"
        
        # Clear cached modules
        modules_to_clear = [k for k in sys.modules.keys() if k.startswith('kimera')]
        for mod in modules_to_clear:
            del sys.modules[mod]
        
        try:
            from kimera.geoid import init_geoid
            from kimera.resonance import resonance, ENABLE_NEGATION_FIX
            
            print(f"ENABLE_NEGATION_FIX = {ENABLE_NEGATION_FIX}")
            
            case_results = []
            for text1, text2, is_negation in test_cases:
                try:
                    # Create geoids using proper init_geoid function
                    g1 = init_geoid(text=text1, lang="en", tags=["test"])
                    g2 = init_geoid(text=text2, lang="en", tags=["test"])
                    
                    # Get resonance score
                    score = resonance(g1, g2)
                    
                    case_results.append({
                        'text1': text1,
                        'text2': text2,
                        'is_negation': is_negation,
                        'score': score,
                        'negation_enabled': negation_enabled
                    })
                    
                    print(f"  {score:.3f} | '{text1}' vs '{text2}' {'(NEG)' if is_negation else ''}")
                    
                except Exception as e:
                    print(f"  ERROR | '{text1}' vs '{text2}' → {e}")
            
            results.extend(case_results)
            
        except Exception as e:
            print(f"❌ Import error: {e}")
            import traceback
            traceback.print_exc()
    
    # Analyze results
    print(f"\n{'='*50}")
    print("ANALYSIS")
    print(f"{'='*50}")
    
    # Group by case
    cases = {}
    for result in results:
        key = (result['text1'], result['text2'])
        if key not in cases:
            cases[key] = {}
        cases[key][result['negation_enabled']] = result['score']
    
    print("\nScore Differences (Negation ON - Negation OFF):")
    print("-" * 50)
    
    for (text1, text2), scores in cases.items():
        if False in scores and True in scores:
            diff = scores[True] - scores[False]
            is_neg = any(r['is_negation'] for r in results 
                        if r['text1'] == text1 and r['text2'] == text2)
            
            print(f"{diff:+.3f} | {text1[:20]:<20} vs {text2[:20]:<20} {'(NEG)' if is_neg else ''}")
    
    print("\n✅ Experiment complete!")
    print("\nExpected: Negation cases should have LOWER scores when negation fix is ON")

if __name__ == "__main__":
    test_negation_cases()