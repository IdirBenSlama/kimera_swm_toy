"""
Kimera Resonance Benchmark
=========================

This benchmark tests Kimera's ability to detect semantic and structural
resonance between concepts - what it's actually designed to do according
to the Spherical Word Methodology (SWM).
"""

import csv
import time
import json
from pathlib import Path
from typing import List, Tuple, Dict
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from kimera.geoid import init_geoid
from kimera.resonance import resonance

# Test cases for resonance detection
RESONANCE_TEST_CASES = [
    # High resonance (>0.7) - strong semantic/structural similarity
    {
        "pair": ("The heart pumps blood through the body", "The pump circulates water through the system"),
        "expected_resonance": "high",
        "domain_pair": ("biology", "engineering"),
        "pattern": "circulation system"
    },
    {
        "pair": ("Neurons transmit electrical signals", "Wires transmit electrical current"),
        "expected_resonance": "high", 
        "domain_pair": ("neuroscience", "electronics"),
        "pattern": "signal transmission"
    },
    {
        "pair": ("The CEO leads the company", "The captain leads the team"),
        "expected_resonance": "high",
        "domain_pair": ("business", "sports"),
        "pattern": "leadership structure"
    },
    
    # Moderate resonance (0.4-0.7) - some structural similarity
    {
        "pair": ("Rivers flow to the ocean", "Information flows through networks"),
        "expected_resonance": "moderate",
        "domain_pair": ("geography", "technology"),
        "pattern": "flow dynamics"
    },
    {
        "pair": ("Trees grow towards sunlight", "Companies grow towards profit"),
        "expected_resonance": "moderate",
        "domain_pair": ("botany", "economics"),
        "pattern": "growth orientation"
    },
    {
        "pair": ("Bees build hexagonal honeycomb", "Architects design efficient structures"),
        "expected_resonance": "moderate",
        "domain_pair": ("nature", "architecture"),
        "pattern": "efficient construction"
    },
    
    # Low resonance (<0.4) - little semantic/structural similarity
    {
        "pair": ("The cat sleeps on the mat", "Democracy requires participation"),
        "expected_resonance": "low",
        "domain_pair": ("daily life", "politics"),
        "pattern": "none"
    },
    {
        "pair": ("Water boils at 100 degrees", "Music has rhythm and melody"),
        "expected_resonance": "low",
        "domain_pair": ("physics", "arts"),
        "pattern": "none"
    },
    {
        "pair": ("The phone is ringing", "History repeats itself"),
        "expected_resonance": "low",
        "domain_pair": ("technology", "philosophy"),
        "pattern": "none"
    }
]

def evaluate_resonance_detection():
    """Evaluate Kimera's resonance detection accuracy."""
    
    print("=" * 60)
    print("KIMERA RESONANCE DETECTION BENCHMARK")
    print("=" * 60)
    print(f"\nTesting {len(RESONANCE_TEST_CASES)} cross-domain concept pairs...\n")
    
    results = []
    correct_classifications = 0
    
    # Define thresholds
    HIGH_THRESHOLD = 0.7
    LOW_THRESHOLD = 0.4
    
    start_time = time.perf_counter()
    
    for i, test_case in enumerate(RESONANCE_TEST_CASES):
        text1, text2 = test_case["pair"]
        expected = test_case["expected_resonance"]
        
        # Create geoids and calculate resonance
        g1 = init_geoid(text1, "en", ["benchmark"])
        g2 = init_geoid(text2, "en", ["benchmark"])
        score = resonance(g1, g2)
        
        # Classify based on score
        if score >= HIGH_THRESHOLD:
            detected = "high"
        elif score >= LOW_THRESHOLD:
            detected = "moderate"
        else:
            detected = "low"
        
        # Check if correct
        correct = detected == expected
        if correct:
            correct_classifications += 1
        
        result = {
            "id": i,
            "text1": text1,
            "text2": text2,
            "domains": test_case["domain_pair"],
            "pattern": test_case["pattern"],
            "expected": expected,
            "detected": detected,
            "score": score,
            "correct": correct
        }
        results.append(result)
        
        # Print progress
        status = "✓" if correct else "✗"
        print(f"{status} Pair {i+1}: {expected} resonance, detected {detected} (score: {score:.3f})")
        print(f"  '{text1[:40]}...' ←→ '{text2[:40]}...'")
        print(f"  Domains: {test_case['domain_pair'][0]} ←→ {test_case['domain_pair'][1]}")
        if test_case["pattern"] != "none":
            print(f"  Pattern: {test_case['pattern']}")
        print()
    
    end_time = time.perf_counter()
    total_time = end_time - start_time
    
    # Calculate metrics
    accuracy = correct_classifications / len(RESONANCE_TEST_CASES)
    avg_time_ms = (total_time / len(RESONANCE_TEST_CASES)) * 1000
    
    # Group results by expected resonance level
    high_results = [r for r in results if r["expected"] == "high"]
    moderate_results = [r for r in results if r["expected"] == "moderate"]
    low_results = [r for r in results if r["expected"] == "low"]
    
    print("=" * 60)
    print("BENCHMARK RESULTS")
    print("=" * 60)
    print(f"\nOverall Accuracy: {accuracy:.1%} ({correct_classifications}/{len(RESONANCE_TEST_CASES)})")
    print(f"Average Processing Time: {avg_time_ms:.2f}ms per pair")
    print(f"Total Time: {total_time:.2f}s")
    
    print("\nAccuracy by Resonance Level:")
    print(f"  High resonance: {sum(r['correct'] for r in high_results)}/{len(high_results)}")
    print(f"  Moderate resonance: {sum(r['correct'] for r in moderate_results)}/{len(moderate_results)}")
    print(f"  Low resonance: {sum(r['correct'] for r in low_results)}/{len(low_results)}")
    
    print("\nScore Distribution:")
    high_scores = [f"{r['score']:.3f}" for r in high_results]
    moderate_scores = [f"{r['score']:.3f}" for r in moderate_results]
    low_scores = [f"{r['score']:.3f}" for r in low_results]
    print(f"  High resonance pairs: {high_scores}")
    print(f"  Moderate resonance pairs: {moderate_scores}")
    print(f"  Low resonance pairs: {low_scores}")
    
    # Save detailed results
    output_file = Path("benchmark_resonance_results.csv")
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "text1", "text2", "domain1", "domain2", "pattern",
            "expected", "detected", "score", "correct"
        ])
        writer.writeheader()
        
        for r in results:
            writer.writerow({
                "id": r["id"],
                "text1": r["text1"],
                "text2": r["text2"],
                "domain1": r["domains"][0],
                "domain2": r["domains"][1],
                "pattern": r["pattern"],
                "expected": r["expected"],
                "detected": r["detected"],
                "score": f"{r['score']:.4f}",
                "correct": r["correct"]
            })
    
    print(f"\nDetailed results saved to: {output_file}")
    
    return results, accuracy, avg_time_ms

def analyze_cross_domain_patterns():
    """Analyze how well Kimera identifies patterns across domains."""
    
    print("\n\n" + "=" * 60)
    print("CROSS-DOMAIN PATTERN ANALYSIS")
    print("=" * 60)
    
    # Group test cases by pattern
    patterns = {}
    for test_case in RESONANCE_TEST_CASES:
        pattern = test_case["pattern"]
        if pattern not in patterns:
            patterns[pattern] = []
        patterns[pattern].append(test_case)
    
    print("\nTesting pattern recognition across domains:\n")
    
    for pattern, cases in patterns.items():
        if pattern == "none":
            continue
            
        print(f"Pattern: {pattern.upper()}")
        print("-" * 40)
        
        # Calculate average resonance for this pattern
        scores = []
        for case in cases:
            g1 = init_geoid(case["pair"][0], "en", ["pattern"])
            g2 = init_geoid(case["pair"][1], "en", ["pattern"])
            score = resonance(g1, g2)
            scores.append(score)
            
            print(f"  {case['domain_pair'][0]} ←→ {case['domain_pair'][1]}: {score:.3f}")
        
        avg_score = sum(scores) / len(scores)
        print(f"  Average resonance: {avg_score:.3f}\n")

if __name__ == "__main__":
    # Run the benchmark
    results, accuracy, avg_time = evaluate_resonance_detection()
    
    # Analyze patterns
    analyze_cross_domain_patterns()
    
    print("\n" + "=" * 60)
    print("CONCLUSION")
    print("=" * 60)
    print("This benchmark tests Kimera's core strength: detecting semantic")
    print("and structural resonance between concepts across different domains.")
    print("This aligns with the Spherical Word Methodology's goal of finding")
    print("hidden connections and patterns in knowledge.")
    print("=" * 60)