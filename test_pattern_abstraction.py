"""
Test the Pattern Abstraction Engine implementation
"""

from src.kimera.patterns import PatternAbstractionEngine, PatternType
from src.kimera.dimensions.geoid_v2 import init_geoid_v2
import json


def test_pattern_extraction():
    """Test extracting patterns from a Geoid"""
    print("Testing Pattern Extraction")
    print("=" * 50)
    
    # Create pattern engine
    engine = PatternAbstractionEngine()
    
    # Test text with rich patterns
    test_text = """
    The immune system protects the body from harmful pathogens by identifying 
    and destroying foreign invaders. It consists of multiple layers including 
    physical barriers, innate immunity, and adaptive immunity. The system evolves 
    and adapts over time, learning from past infections to provide better protection. 
    It depends on proper nutrition and works in harmony with other body systems.
    """
    
    # Create geoid
    geoid = init_geoid_v2(text=test_text)
    
    # Extract patterns
    patterns = engine.extract_patterns(geoid)
    
    print(f"Extracted patterns for: '{test_text[:50]}...'")
    print("\nFunctional Pattern (What does it DO?):")
    print(f"  Primary functions: {patterns.functional.primary_functions}")
    print(f"  Actions: {patterns.functional.performs_actions}")
    print(f"  Inputs: {patterns.functional.inputs}")
    print(f"  Outputs: {patterns.functional.outputs}")
    
    print("\nStructural Pattern (How is it BUILT?):")
    print(f"  Components: {patterns.structural.components}")
    print(f"  Arrangement: {patterns.structural.arrangement_type}")
    print(f"  Organization: {patterns.structural.organization_principle}")
    
    print("\nDynamic Pattern (How does it CHANGE?):")
    print(f"  States: {patterns.dynamic.states}")
    print(f"  Temporal nature: {patterns.dynamic.temporal_nature}")
    print(f"  Change drivers: {patterns.dynamic.change_drivers}")
    
    print("\nRelational Pattern (How does it RELATE?):")
    print(f"  Depends on: {patterns.relational.depends_on}")
    print(f"  Works with: {patterns.relational.complements}")
    
    print("\nConfidence scores:")
    for ptype, score in patterns.confidence_scores.items():
        print(f"  {ptype.value}: {score:.2f}")
    print()


def test_pattern_comparison():
    """Test comparing patterns between different concepts"""
    print("Testing Pattern Comparison and Resonance")
    print("=" * 50)
    
    engine = PatternAbstractionEngine()
    
    # Create two concepts to compare
    concept1 = """
    The immune system is a complex network that protects organisms from disease. 
    It identifies and neutralizes harmful substances and pathogens through multiple 
    layers of defense. The system adapts and evolves based on exposure to threats.
    """
    
    concept2 = """
    A firewall is a network security system that monitors and controls incoming 
    and outgoing network traffic. It establishes a barrier between trusted internal 
    networks and untrusted external networks, filtering data based on security rules.
    """
    
    # Create geoids and extract patterns
    geoid1 = init_geoid_v2(text=concept1)
    geoid2 = init_geoid_v2(text=concept2)
    
    patterns1 = engine.extract_patterns(geoid1)
    patterns2 = engine.extract_patterns(geoid2)
    
    # Compare patterns
    similarities = engine.compare_patterns(patterns1, patterns2)
    
    print("Concept 1: Immune System")
    print("Concept 2: Firewall")
    print("\nPattern similarities:")
    for ptype, score in similarities.items():
        print(f"  {ptype.value}: {score:.3f}")
    
    # Find resonance
    resonance = engine.find_pattern_resonance(patterns1, patterns2, threshold=0.3)
    
    print(f"\nOverall resonance score: {resonance['overall_score']:.3f}")
    print(f"Is resonant: {resonance['is_resonant']}")
    
    if resonance['strong_resonances']:
        print("\nStrong resonances:")
        for ptype, score in resonance['strong_resonances'].items():
            print(f"  {ptype.value}: {score:.3f}")
    
    if resonance['insights']:
        print("\nCross-pattern insights:")
        for insight in resonance['insights']:
            print(f"  - {insight}")
    print()


def test_cross_domain_resonance():
    """Test finding resonance across very different domains"""
    print("Testing Cross-Domain Resonance Discovery")
    print("=" * 50)
    
    engine = PatternAbstractionEngine()
    
    # Three concepts from different domains
    concepts = {
        "Ecosystem": """
        An ecosystem is a community of living organisms interacting with their 
        physical environment. It cycles nutrients, transforms energy, and maintains 
        balance through complex feedback loops. Species depend on each other and 
        evolve together over time.
        """,
        
        "Economy": """
        An economy is a system of production, distribution, and consumption of goods 
        and services. It involves multiple actors including producers, consumers, and 
        regulators. The system evolves through market cycles and adapts to changing 
        conditions.
        """,
        
        "Neural Network": """
        A neural network is a computational system inspired by biological brains. 
        It consists of interconnected nodes that process information in layers. 
        The network learns and adapts through training, adjusting connections based 
        on feedback.
        """
    }
    
    # Extract patterns for all concepts
    all_patterns = {}
    for name, text in concepts.items():
        geoid = init_geoid_v2(text=text)
        all_patterns[name] = engine.extract_patterns(geoid)
    
    # Compare all pairs
    print("Cross-domain resonance analysis:")
    print("-" * 40)
    
    names = list(concepts.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            name1, name2 = names[i], names[j]
            
            resonance = engine.find_pattern_resonance(
                all_patterns[name1], 
                all_patterns[name2],
                threshold=0.3
            )
            
            print(f"\n{name1} <-> {name2}:")
            print(f"  Overall resonance: {resonance['overall_score']:.3f}")
            
            # Show which patterns resonate most
            best_pattern = max(resonance['similarities'].items(), 
                             key=lambda x: x[1])
            print(f"  Strongest pattern match: {best_pattern[0].value} ({best_pattern[1]:.3f})")
            
            if resonance['insights']:
                print(f"  Insights: {', '.join(resonance['insights'])}")


def test_pattern_vectors():
    """Test pattern vector representations"""
    print("\nTesting Pattern Vector Representations")
    print("=" * 50)
    
    engine = PatternAbstractionEngine()
    
    # Create a concept with clear patterns
    text = """
    The heart is a muscular organ that pumps blood throughout the body. 
    It consists of four chambers working in a coordinated rhythm. The heart 
    beats continuously, adapting its rate based on the body's needs. It depends 
    on electrical signals and works closely with the circulatory system.
    """
    
    geoid = init_geoid_v2(text=text)
    patterns = engine.extract_patterns(geoid)
    
    print("Pattern vectors for 'Heart' concept:")
    print(f"Functional vector: {patterns.functional.to_vector()}")
    print(f"Structural vector: {patterns.structural.to_vector()}")
    print(f"Dynamic vector: {patterns.dynamic.to_vector()}")
    print(f"Relational vector: {patterns.relational.to_vector()}")
    
    # Composite vector
    composite = patterns.to_composite_vector()
    print(f"\nComposite vector shape: {composite.shape}")
    print(f"Composite vector (first 10 elements): {composite[:10]}")


if __name__ == "__main__":
    test_pattern_extraction()
    test_pattern_comparison()
    test_cross_domain_resonance()
    test_pattern_vectors()
    
    print("\n" + "=" * 50)
    print("Pattern Abstraction Engine testing complete!")
    print("This demonstrates deep pattern extraction according to SWM methodology.")
    print("The engine can identify functional, structural, dynamic, and relational")
    print("patterns, enabling the discovery of profound cross-domain resonances.")