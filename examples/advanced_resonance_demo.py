"""
Advanced Resonance Demo
======================

Demonstrates Kimera's advanced pattern extraction and resonance detection
using all four SWM pattern types.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from kimera.geoid import init_geoid
from kimera.resonance import resonance as resonance_v1
from kimera.enhanced_resonance import resonance_v2, resonance_v3
from kimera.advanced_patterns import extract_patterns_advanced

def demonstrate_pattern_types():
    """Show how different pattern types are extracted."""
    
    print("=" * 70)
    print("ADVANCED PATTERN EXTRACTION - ALL FOUR SWM TYPES")
    print("=" * 70)
    
    examples = {
        "Functional": [
            "The heart pumps blood through the body",
            "The CPU processes data in the computer",
            "The teacher guides students towards knowledge"
        ],
        "Structural": [
            "The company consists of three divisions",
            "The CEO leads the organization",
            "The ecosystem contains many species"
        ],
        "Dynamic": [
            "Information flows through the network",
            "The company grows towards new markets",
            "Water circulates through the system"
        ],
        "Relational": [
            "The economy depends on consumer confidence",
            "This approach differs from traditional methods",
            "The solution requires careful planning"
        ]
    }
    
    for pattern_type, texts in examples.items():
        print(f"\n{pattern_type} Patterns:")
        print("-" * 50)
        
        for text in texts:
            patterns = extract_patterns_advanced(text)
            print(f"\nText: '{text}'")
            
            if patterns:
                for p in patterns:
                    print(f"  Type: {p.pattern_type}")
                    
                    if p.pattern_type == "functional":
                        print(f"    Action: {p.action}")
                        print(f"    Agent: {p.agent}")
                        print(f"    Patient: {p.patient}")
                        if p.attributes:
                            print(f"    Category: {p.attributes.get('action_category')}")
                    
                    elif p.pattern_type == "structural":
                        print(f"    Organization: {p.organization}")
                        print(f"    Whole: {p.whole}")
                        print(f"    Parts: {p.parts}")
                    
                    elif p.pattern_type == "dynamic":
                        print(f"    Process: {p.process}")
                        print(f"    Nature: {p.temporal_nature}")
                        print(f"    Direction: {p.direction}")
                    
                    elif p.pattern_type == "relational":
                        print(f"    Relation: {p.relation_type}")
                        print(f"    Entity 1: {p.entity1}")
                        print(f"    Entity 2: {p.entity2}")
            else:
                print("  No patterns extracted")

def compare_resonance_versions():
    """Compare three versions of resonance detection."""
    
    print("\n\n" + "=" * 70)
    print("COMPARING RESONANCE DETECTION VERSIONS")
    print("=" * 70)
    
    test_pairs = [
        # High functional similarity
        ("The heart pumps blood through arteries",
         "The pump circulates water through pipes"),
        
        # High structural similarity
        ("The CEO manages the company",
         "The captain leads the team"),
        
        # High dynamic similarity
        ("Rivers flow towards the ocean",
         "Traffic flows towards downtown"),
        
        # High relational similarity
        ("Plants depend on sunlight",
         "Businesses depend on customers"),
        
        # Cross-pattern similarity
        ("The immune system protects the body",
         "The firewall protects the network"),
        
        # Low similarity
        ("The cat sleeps peacefully",
         "Democracy requires participation")
    ]
    
    print("\nComparing Basic (v1) vs Enhanced (v2) vs Advanced (v3) resonance:\n")
    
    for text1, text2 in test_pairs:
        g1 = init_geoid(text1, "en", ["demo"])
        g2 = init_geoid(text2, "en", ["demo"])
        
        score_v1 = resonance_v1(g1, g2)
        score_v2 = resonance_v2(g1, g2)
        score_v3 = resonance_v3(g1, g2)
        
        print(f"'{text1[:40]}...' ←→")
        print(f"'{text2[:40]}...'")
        print(f"  Basic (v1):    {score_v1:.3f}")
        print(f"  Enhanced (v2): {score_v2:.3f} {'↑' if score_v2 > score_v1 else ''}")
        print(f"  Advanced (v3): {score_v3:.3f} {'↑' if score_v3 > score_v2 else ''}")
        
        # Show detected patterns
        patterns1 = extract_patterns_advanced(text1)
        patterns2 = extract_patterns_advanced(text2)
        if patterns1 and patterns2:
            print(f"  Patterns: {patterns1[0].pattern_type} ←→ {patterns2[0].pattern_type}")
        
        print()

def demonstrate_cross_domain_resonance():
    """Show how advanced resonance finds connections across domains."""
    
    print("\n" + "=" * 70)
    print("CROSS-DOMAIN RESONANCE DISCOVERY")
    print("=" * 70)
    
    # Concepts from different domains that share deep patterns
    concepts = {
        "Biology": "The heart pumps blood through the circulatory system",
        "Technology": "The router directs data through the network",
        "Economics": "The bank circulates money through the economy",
        "Sociology": "Leaders guide communities through challenges",
        "Physics": "Energy flows through the system",
        "Psychology": "Thoughts flow through consciousness"
    }
    
    print("\nFinding resonances across different domains:\n")
    
    # Create geoids
    domain_geoids = {domain: init_geoid(text, "en", ["cross-domain"]) 
                     for domain, text in concepts.items()}
    
    # Find all cross-domain resonances above threshold
    threshold = 0.6
    resonances = []
    
    domains = list(domain_geoids.keys())
    for i in range(len(domains)):
        for j in range(i+1, len(domains)):
            domain1, domain2 = domains[i], domains[j]
            score = resonance_v3(domain_geoids[domain1], domain_geoids[domain2])
            
            if score > threshold:
                resonances.append((domain1, domain2, score))
    
    # Sort by score
    resonances.sort(key=lambda x: x[2], reverse=True)
    
    print(f"Strong cross-domain resonances (>{threshold}):")
    print("-" * 50)
    
    for domain1, domain2, score in resonances[:5]:  # Top 5
        print(f"\n{domain1} ←→ {domain2}: {score:.3f}")
        print(f"  '{concepts[domain1][:40]}...'")
        print(f"  '{concepts[domain2][:40]}...'")
        
        # Extract and show shared patterns
        patterns1 = extract_patterns_advanced(concepts[domain1])
        patterns2 = extract_patterns_advanced(concepts[domain2])
        
        if patterns1 and patterns2:
            shared_types = set(p.pattern_type for p in patterns1) & set(p.pattern_type for p in patterns2)
            if shared_types:
                print(f"  Shared pattern types: {', '.join(shared_types)}")

def demonstrate_practical_applications():
    """Show practical applications of advanced resonance."""
    
    print("\n\n" + "=" * 70)
    print("PRACTICAL APPLICATIONS")
    print("=" * 70)
    
    print("\n1. Innovation through Cross-Domain Insights:")
    print("-" * 50)
    
    problem = "How to improve urban traffic flow"
    analogies = [
        "Blood flows through arteries and veins",
        "Data packets flow through network routers",
        "Water flows through irrigation channels",
        "Electricity flows through power grids"
    ]
    
    problem_geoid = init_geoid(problem, "en", ["problem"])
    
    print(f"Problem: {problem}")
    print("\nFinding analogous systems for inspiration:\n")
    
    for analogy in analogies:
        analogy_geoid = init_geoid(analogy, "en", ["analogy"])
        score = resonance_v3(problem_geoid, analogy_geoid)
        
        if score > 0.5:
            print(f"  • {analogy} (resonance: {score:.3f})")
            patterns = extract_patterns_advanced(analogy)
            if patterns and patterns[0].pattern_type == "dynamic":
                print(f"    → Insight: Study {patterns[0].process} patterns")
    
    print("\n2. Knowledge Discovery:")
    print("-" * 50)
    
    concept = "Machine learning trains models on data"
    knowledge_base = [
        "Teachers train students with examples",
        "Athletes train muscles through repetition",
        "Gardeners train vines along structures",
        "Dogs learn tricks through rewards"
    ]
    
    concept_geoid = init_geoid(concept, "en", ["concept"])
    
    print(f"Concept: {concept}")
    print("\nDiscovering related knowledge:\n")
    
    for knowledge in knowledge_base:
        knowledge_geoid = init_geoid(knowledge, "en", ["knowledge"])
        score = resonance_v3(concept_geoid, knowledge_geoid)
        
        if score > 0.4:
            print(f"  • {knowledge} (resonance: {score:.3f})")

if __name__ == "__main__":
    # Run all demonstrations
    demonstrate_pattern_types()
    compare_resonance_versions()
    demonstrate_cross_domain_resonance()
    demonstrate_practical_applications()
    
    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("Advanced resonance detection with all four SWM pattern types")
    print("enables Kimera to find deep structural similarities across")
    print("domains, leading to creative insights and knowledge discovery.")
    print("=" * 70)