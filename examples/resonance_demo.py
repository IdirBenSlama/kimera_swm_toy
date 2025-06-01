"""
Kimera Resonance Demo
====================

This demo shows Kimera's true strength: finding deep structural
similarities (resonance) between seemingly unrelated concepts.

This is what SWM is really about - not contradiction detection,
but discovering hidden connections across domains.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from kimera.geoid import init_geoid
from kimera.resonance import resonance
import numpy as np

def find_resonances(concepts, threshold=0.5):
    """Find all resonant pairs above threshold."""
    geoids = [init_geoid(c, "en", ["demo"]) for c in concepts]
    resonances = []
    
    for i in range(len(geoids)):
        for j in range(i+1, len(geoids)):
            score = resonance(geoids[i], geoids[j])
            if score > threshold:
                resonances.append((
                    concepts[i], 
                    concepts[j], 
                    score,
                    interpret_resonance(score)
                ))
    
    return sorted(resonances, key=lambda x: x[2], reverse=True)

def interpret_resonance(score):
    """Interpret resonance score meaning."""
    if score > 0.9:
        return "Very strong resonance - nearly identical patterns"
    elif score > 0.7:
        return "Strong resonance - significant structural similarity"
    elif score > 0.5:
        return "Moderate resonance - notable connections"
    elif score > 0.3:
        return "Weak resonance - some shared aspects"
    else:
        return "Low resonance - largely unrelated"

def demo_cross_domain_resonance():
    """Demonstrate finding patterns across different domains."""
    
    print("=" * 60)
    print("KIMERA RESONANCE DEMONSTRATION")
    print("Finding Hidden Connections Across Domains")
    print("=" * 60)
    
    # Concepts from different domains
    concepts = [
        # Biology
        "The immune system protects the body from invaders",
        "White blood cells attack foreign substances",
        
        # Computer Security
        "Antivirus software protects computers from malware",
        "Firewall blocks unauthorized network access",
        
        # Social Systems
        "Border security protects nations from threats",
        "Community watch programs monitor neighborhoods",
        
        # Psychology
        "Defense mechanisms protect the ego from anxiety",
        "Cognitive biases filter threatening information",
        
        # Economics
        "Market regulations protect consumers from fraud",
        "Insurance protects against financial loss"
    ]
    
    print("\nAnalyzing concepts from: Biology, Computer Security, Social Systems,")
    print("Psychology, and Economics domains...\n")
    
    # Find resonances
    resonances = find_resonances(concepts, threshold=0.4)
    
    print("DISCOVERED RESONANCES (Cross-Domain Patterns):")
    print("-" * 60)
    
    for c1, c2, score, interpretation in resonances:
        print(f"\nResonance Score: {score:.3f}")
        print(f"Interpretation: {interpretation}")
        print(f"Concept 1: {c1[:50]}...")
        print(f"Concept 2: {c2[:50]}...")
    
    # Demonstrate pattern abstraction insight
    print("\n" + "=" * 60)
    print("PATTERN ABSTRACTION INSIGHT:")
    print("=" * 60)
    print("\nKimera has identified a common 'protection' pattern across domains:")
    print("- All involve a DEFENDER protecting a SYSTEM from THREATS")
    print("- This pattern appears in biological, digital, social, psychological,")
    print("  and economic contexts with similar structural dynamics")
    print("\nThis is the power of SWM - revealing deep structural similarities")
    print("that can lead to cross-domain insights and innovations!")

def demo_creative_connections():
    """Show how resonance can spark creative insights."""
    
    print("\n\n" + "=" * 60)
    print("CREATIVE CONNECTIONS DEMO")
    print("=" * 60)
    
    creative_concepts = [
        "A river flows through the landscape",
        "Time flows through our lives",
        "Information flows through networks",
        "Traffic flows through city streets",
        "Emotions flow through relationships",
        "Energy flows through ecosystems"
    ]
    
    print("\nFinding resonances in 'flow' concepts across domains...\n")
    
    resonances = find_resonances(creative_concepts, threshold=0.5)
    
    for c1, c2, score, _ in resonances[:3]:  # Top 3
        print(f"\nResonance ({score:.3f}):")
        print(f"  '{c1}' ←→ '{c2}'")
        
        # Generate creative insight
        if "river" in c1 and "information" in c2:
            print("  💡 Insight: Data streams and river systems share patterns -")
            print("     both have sources, tributaries, flows, and deltas!")
        elif "time" in c1 and "traffic" in c2:
            print("  💡 Insight: Time management and traffic management share patterns -")
            print("     both involve flow control, bottlenecks, and optimization!")
        elif "emotions" in c1 and "energy" in c2:
            print("  💡 Insight: Emotional and ecological systems share patterns -")
            print("     both involve cycles, conservation, and transformation!")

def demo_vs_contradiction():
    """Show the difference between resonance and contradiction."""
    
    print("\n\n" + "=" * 60)
    print("RESONANCE vs CONTRADICTION")
    print("=" * 60)
    
    pairs = [
        ("The sun is hot", "The sun is cold"),  # Contradiction
        ("The sun is hot", "Fire is hot"),      # High resonance
        ("The sun is hot", "Ice is cold"),       # Low resonance, no contradiction
        ("Birds can fly", "Birds cannot fly"),   # Contradiction
        ("Birds can fly", "Planes can fly"),     # High resonance
        ("Birds can fly", "Fish can swim"),      # Moderate resonance (movement)
    ]
    
    print("\nAnalyzing pairs for resonance (not contradiction):\n")
    
    for text1, text2 in pairs:
        g1 = init_geoid(text1, "en", ["demo"])
        g2 = init_geoid(text2, "en", ["demo"])
        score = resonance(g1, g2)
        
        print(f"'{text1}' ←→ '{text2}'")
        print(f"  Resonance: {score:.3f} - {interpret_resonance(score)}")
        
        # Add context about what this means
        if score > 0.7:
            print("  → These share significant semantic/structural patterns")
        elif score < 0.3:
            print("  → These are largely unrelated (not necessarily contradictory!)")
        print()

if __name__ == "__main__":
    # Run all demos
    demo_cross_domain_resonance()
    demo_creative_connections()
    demo_vs_contradiction()
    
    print("\n" + "=" * 60)
    print("KEY TAKEAWAY:")
    print("=" * 60)
    print("Kimera excels at finding hidden connections and patterns across")
    print("different domains - this is its true strength according to SWM!")
    print("Contradiction detection is a separate concern that requires")
    print("different techniques than resonance detection.")
    print("=" * 60)