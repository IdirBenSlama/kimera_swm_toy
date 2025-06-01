"""
Enhanced Resonance Demo
======================

Demonstrates how pattern extraction improves resonance detection
for finding structural similarities across domains.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from kimera.geoid import init_geoid
from kimera.resonance import resonance as basic_resonance
from kimera.enhanced_resonance import resonance_v2
from kimera.pattern_extraction import extract_patterns

def compare_resonance_methods():
    """Compare basic vs enhanced resonance detection."""
    
    print("=" * 70)
    print("COMPARING BASIC vs ENHANCED RESONANCE DETECTION")
    print("=" * 70)
    
    test_pairs = [
        # High structural similarity (should have high resonance)
        ("The heart pumps blood through the body", 
         "The pump circulates water through the system"),
        
        ("Neurons transmit electrical signals",
         "Wires transmit electrical current"),
        
        ("The CEO leads the company",
         "The captain leads the team"),
        
        # Moderate structural similarity
        ("Rivers flow to the ocean",
         "Information flows through networks"),
        
        ("Trees grow towards sunlight",
         "Companies grow towards profit"),
        
        # Low structural similarity
        ("The cat sleeps on the mat",
         "Democracy requires participation"),
    ]
    
    print("\nAnalyzing concept pairs:\n")
    
    for text1, text2 in test_pairs:
        # Create geoids
        g1 = init_geoid(text1, "en", ["demo"])
        g2 = init_geoid(text2, "en", ["demo"])
        
        # Calculate both resonance scores
        basic_score = basic_resonance(g1, g2)
        enhanced_score = resonance_v2(g1, g2)
        
        # Extract patterns for display
        patterns1 = extract_patterns(text1)
        patterns2 = extract_patterns(text2)
        
        print(f"Pair: '{text1}' ←→ '{text2}'")
        print(f"  Basic Resonance:    {basic_score:.3f}")
        print(f"  Enhanced Resonance: {enhanced_score:.3f} {'↑' if enhanced_score > basic_score else ''}")
        
        # Show extracted patterns
        if patterns1:
            p1 = patterns1[0]
            print(f"  Pattern 1: {p1.action} ({p1.pattern_type})")
        if patterns2:
            p2 = patterns2[0]
            print(f"  Pattern 2: {p2.action} ({p2.pattern_type})")
        
        # Interpretation
        if enhanced_score > 0.7:
            print("  → Strong structural similarity detected!")
        elif enhanced_score > 0.5:
            print("  → Moderate structural similarity")
        else:
            print("  → Low structural similarity")
        print()

def demonstrate_pattern_extraction():
    """Show how pattern extraction works."""
    
    print("\n" + "=" * 70)
    print("PATTERN EXTRACTION DEMONSTRATION")
    print("=" * 70)
    
    examples = [
        "The immune system protects the body from invaders",
        "Antivirus software protects computers from malware",
        "The firewall blocks unauthorized access",
        "Plants absorb nutrients through their roots",
        "The company absorbs smaller competitors",
    ]
    
    print("\nExtracting patterns from example sentences:\n")
    
    for text in examples:
        patterns = extract_patterns(text)
        print(f"Text: '{text}'")
        
        if patterns:
            for p in patterns:
                print(f"  Pattern Type: {p.pattern_type}")
                print(f"  Subject: {p.subject}")
                print(f"  Action: {p.action}")
                print(f"  Object: {p.object}")
                if p.attributes:
                    print(f"  Attributes: {p.attributes}")
        else:
            print("  No patterns extracted")
        print()

def show_cross_domain_insights():
    """Demonstrate cross-domain pattern matching."""
    
    print("\n" + "=" * 70)
    print("CROSS-DOMAIN PATTERN INSIGHTS")
    print("=" * 70)
    
    # Groups of concepts with similar patterns
    pattern_groups = {
        "Protection Pattern": [
            "The immune system defends against viruses",
            "The firewall defends against hackers",
            "The army defends against invaders",
            "Insurance defends against financial loss"
        ],
        "Flow Pattern": [
            "Blood flows through arteries",
            "Traffic flows through highways",
            "Data flows through networks",
            "Money flows through markets"
        ],
        "Growth Pattern": [
            "Plants grow towards light",
            "Businesses grow towards profit",
            "Cities grow towards resources",
            "Knowledge grows towards understanding"
        ]
    }
    
    for pattern_name, concepts in pattern_groups.items():
        print(f"\n{pattern_name}:")
        print("-" * 50)
        
        # Create geoids
        geoids = [init_geoid(c, "en", ["pattern"]) for c in concepts]
        
        # Calculate average resonance within group
        total_resonance = 0
        comparisons = 0
        
        for i in range(len(geoids)):
            for j in range(i+1, len(geoids)):
                score = resonance_v2(geoids[i], geoids[j])
                total_resonance += score
                comparisons += 1
                
                if i == 0 and j == 1:  # Show first comparison
                    print(f"  Example: '{concepts[i][:30]}...' ←→")
                    print(f"           '{concepts[j][:30]}...'")
                    print(f"  Enhanced Resonance: {score:.3f}")
        
        avg_resonance = total_resonance / comparisons if comparisons > 0 else 0
        print(f"  Average within-pattern resonance: {avg_resonance:.3f}")
        print(f"  → This group shares the '{pattern_name}' across different domains")

if __name__ == "__main__":
    # Run all demonstrations
    compare_resonance_methods()
    demonstrate_pattern_extraction()
    show_cross_domain_insights()
    
    print("\n" + "=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    print("1. Enhanced resonance better captures structural similarities")
    print("2. Pattern extraction reveals hidden connections across domains")
    print("3. This approach aligns with SWM's goal of finding deep patterns")
    print("4. Further improvements could include:")
    print("   - More sophisticated pattern extraction")
    print("   - Multi-language pattern analysis")
    print("   - Symbolic and metaphorical pattern matching")
    print("=" * 70)