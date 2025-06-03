"""
Simple Kimera API Demo
=====================

Shows how easy it is to use Kimera's unified API for:
- Finding resonance (deep similarities)
- Detecting contradictions
- Extracting patterns
- Discovering insights
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from kimera.api import Kimera, find_resonance, detect_contradiction, extract_patterns

def demo_basic_usage():
    """Show basic API usage."""
    
    print("=" * 70)
    print("KIMERA SIMPLE API DEMO")
    print("=" * 70)
    
    # Initialize Kimera
    kimera = Kimera()
    
    # Example 1: Find Resonance
    print("\n1. Finding Resonance (Deep Similarity)")
    print("-" * 50)
    
    text1 = "The heart pumps blood through the body"
    text2 = "The CPU processes data through the system"
    
    result = kimera.find_resonance(text1, text2)
    
    print(f"Text 1: '{text1}'")
    print(f"Text 2: '{text2}'")
    print(f"\nResonance Score: {result['score']:.3f}")
    print(f"Interpretation: {result['interpretation']}")
    print(f"Patterns found: {len(result['patterns']['text1']) + len(result['patterns']['text2'])}")
    
    # Example 2: Detect Contradiction
    print("\n\n2. Detecting Contradiction")
    print("-" * 50)
    
    stmt1 = "The Earth is round"
    stmt2 = "The Earth is flat"
    
    result = kimera.analyze_contradiction(stmt1, stmt2)
    
    print(f"Statement 1: '{stmt1}'")
    print(f"Statement 2: '{stmt2}'")
    print(f"\nIs Contradiction: {result['is_contradiction']}")
    print(f"Confidence: {result['confidence']:.2f}")
    print(f"Reasoning: {result['reasoning']}")
    
    # Example 3: Extract Patterns
    print("\n\n3. Extracting Patterns")
    print("-" * 50)
    
    text = "Information flows through the network continuously"
    patterns = kimera.extract_patterns(text)
    
    print(f"Text: '{text}'")
    print(f"\nExtracted {len(patterns)} patterns:")
    
    for p in patterns:
        print(f"  - {p['type'].capitalize()} pattern")
        if 'action' in p:
            print(f"    Action: {p['action']}")
        if 'process' in p:
            print(f"    Process: {p['process']}")
        if 'temporal_nature' in p:
            print(f"    Nature: {p['temporal_nature']}")

def demo_insight_discovery():
    """Show how to discover insights across domains."""
    
    print("\n\n" + "=" * 70)
    print("CROSS-DOMAIN INSIGHT DISCOVERY")
    print("=" * 70)
    
    kimera = Kimera()
    
    # Problem to solve
    problem = "How to improve team communication"
    
    # Knowledge base from different domains
    knowledge_base = [
        "Neurons transmit signals through synapses",
        "Rivers flow through channels to reach the ocean",
        "Bees communicate through dance patterns",
        "Networks route data through optimal paths",
        "Musicians synchronize through rhythm and tempo",
        "Plants share nutrients through root networks"
    ]
    
    print(f"Problem: {problem}")
    print("\nSearching for insights from other domains...\n")
    
    insights = kimera.find_cross_domain_insights(problem, knowledge_base, threshold=0.3)
    
    for i, insight in enumerate(insights[:3], 1):  # Top 3
        print(f"{i}. {insight['text']}")
        print(f"   Resonance: {insight['resonance_score']:.3f}")
        print(f"   Insight: {insight['potential_insight']}")
        print()

def demo_quick_functions():
    """Show convenience functions for quick use."""
    
    print("\n" + "=" * 70)
    print("QUICK FUNCTION EXAMPLES")
    print("=" * 70)
    
    # Quick resonance check
    score = find_resonance(
        "The company grows rapidly",
        "The plant grows quickly"
    )
    print(f"\nQuick resonance score: {score:.3f}")
    
    # Quick contradiction check
    is_contra = analyze_contradiction(
        "It is raining",
        "It is not raining"
    )
    print(f"Quick contradiction check: {is_contra}")
    
    # Quick pattern extraction
    patterns = extract_patterns("The manager leads the team effectively")
    print(f"Quick pattern extraction: Found {len(patterns)} patterns")

def demo_practical_example():
    """Show a practical use case."""
    
    print("\n\n" + "=" * 70)
    print("PRACTICAL EXAMPLE: Finding Design Patterns in Nature")
    print("=" * 70)
    
    kimera = Kimera()
    
    # Engineering challenge
    challenge = "Design an efficient distribution network"
    
    # Natural systems to learn from
    natural_systems = [
        "Blood vessels branch from arteries to capillaries",
        "River deltas spread water across the landscape",
        "Tree roots branch to absorb nutrients",
        "Lightning follows branching paths to the ground",
        "Leaf veins distribute nutrients throughout the leaf",
        "Neural networks connect through branching dendrites"
    ]
    
    print(f"Engineering Challenge: {challenge}")
    print("\nAnalyzing natural systems for design insights...\n")
    
    insights = kimera.find_cross_domain_insights(challenge, natural_systems, threshold=0.4)
    
    print("Key Design Patterns Found:")
    print("-" * 50)
    
    # Analyze common patterns
    pattern_types = {}
    for insight in insights:
        for pattern in insight['patterns']:
            ptype = pattern['type']
            pattern_types[ptype] = pattern_types.get(ptype, 0) + 1
    
    for ptype, count in pattern_types.items():
        print(f"  • {ptype.capitalize()} patterns: {count} occurrences")
    
    print("\nTop Natural Analogies:")
    for insight in insights[:3]:
        print(f"  • {insight['text']} (resonance: {insight['resonance_score']:.3f})")
    
    print("\nDesign Insight: These natural systems suggest using a branching,")
    print("hierarchical structure for efficient distribution.")

if __name__ == "__main__":
    # Run all demos
    demo_basic_usage()
    demo_insight_discovery()
    demo_quick_functions()
    demo_practical_example()
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("Kimera provides a simple, unified API for:")
    print("  • Finding deep similarities (resonance)")
    print("  • Detecting logical contradictions")
    print("  • Extracting structural patterns")
    print("  • Discovering cross-domain insights")
    print("\nUse Kimera to enhance creativity, solve problems,")
    print("and discover hidden connections in knowledge!")
    print("=" * 70)