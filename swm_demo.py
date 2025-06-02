"""
Kimera SWM Demo - Discovering Hidden Connections

This demo shows how Kimera can discover non-obvious connections
between concepts from different domains using the Spherical Word Methodology.
"""

from src.kimera.dimensions.geoid_v2 import init_geoid_v2
from src.kimera.patterns import PatternAbstractionEngine
from src.kimera.resonance_v2 import EnhancedResonanceDetector
import sys


def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(text.center(60))
    print("="*60 + "\n")


def analyze_concept_pair(concept1_name, concept1_text, concept2_name, concept2_text):
    """Analyze resonance between two concepts"""
    print(f"\nAnalyzing: {concept1_name} <-> {concept2_name}")
    print("-" * 50)
    
    # Create Geoids
    geoid1 = init_geoid_v2(text=concept1_text)
    geoid2 = init_geoid_v2(text=concept2_text)
    
    # Extract patterns
    engine = PatternAbstractionEngine()
    patterns1 = engine.extract_patterns(geoid1)
    patterns2 = engine.extract_patterns(geoid2)
    
    # Detect resonance
    detector = EnhancedResonanceDetector()
    result = detector.detect_resonance(geoid1, geoid2, analyze_languages=False)
    
    # Display results
    print(f"\nResonance Analysis:")
    print(f"  Overall Score: {result.overall_resonance:.2%}")
    print(f"  Domain Distance: {result.domain_distance:.2f}")
    print(f"  Insight Potential: {result.insight_potential:.2%}")
    
    # Show pattern matches
    print(f"\nPattern Similarities:")
    for ptype, score in result.pattern_similarities.items():
        if score > 0.1:
            print(f"  {ptype.value.capitalize()}: {score:.2%}")
    
    # Show insights
    if result.discovered_insights:
        print(f"\nDiscovered Insights:")
        for insight in result.discovered_insights:
            print(f"  • {insight}")
    
    return result


def main():
    print_header("Kimera SWM - Discovering Hidden Connections")
    
    print("The Spherical Word Methodology (SWM) reveals deep patterns")
    print("that connect seemingly unrelated concepts across domains.\n")
    
    # Example 1: Biology <-> Technology
    print_header("Example 1: Biological vs Technological Systems")
    
    immune_system = """
    The immune system defends the body against pathogens through multiple 
    layers of protection. It identifies threats, maintains memory of past 
    encounters, and adapts its responses. White blood cells patrol the body, 
    communicate through chemical signals, and coordinate attacks on invaders.
    """
    
    computer_security = """
    Computer security systems protect networks from cyber threats using 
    layered defenses. They detect intrusions, maintain logs of past attacks, 
    and update their rules. Security software monitors the system, shares 
    threat intelligence, and coordinates responses to malicious activity.
    """
    
    result1 = analyze_concept_pair(
        "Immune System", immune_system,
        "Computer Security", computer_security
    )
    
    # Example 2: Nature <-> Economics
    print_header("Example 2: Natural vs Economic Systems")
    
    ecosystem = """
    Forest ecosystems cycle nutrients through complex food webs. Energy flows 
    from producers to consumers, with decomposers recycling materials. Species 
    compete for resources while also depending on each other. The system 
    self-regulates through feedback loops and maintains dynamic equilibrium.
    """
    
    market_economy = """
    Market economies circulate wealth through networks of exchange. Value flows 
    from producers to consumers, with financial systems recycling capital. 
    Businesses compete for customers while depending on supply chains. The market 
    self-regulates through price signals and seeks equilibrium.
    """
    
    result2 = analyze_concept_pair(
        "Forest Ecosystem", ecosystem,
        "Market Economy", market_economy
    )
    
    # Example 3: Art <-> Science
    print_header("Example 3: Artistic vs Scientific Processes")
    
    musical_composition = """
    Musical composition involves arranging sounds in time to create emotional 
    experiences. Composers work with themes, develop variations, and build 
    tension and release. They balance repetition with novelty, structure with 
    spontaneity, creating works that resonate with listeners.
    """
    
    scientific_research = """
    Scientific research involves organizing observations to understand natural 
    phenomena. Researchers work with hypotheses, test variations, and build 
    evidence through experiments. They balance replication with innovation, 
    methodology with discovery, creating knowledge that advances understanding.
    """
    
    result3 = analyze_concept_pair(
        "Musical Composition", musical_composition,
        "Scientific Research", scientific_research
    )
    
    # Summary
    print_header("Summary: The Power of SWM")
    
    print("Kimera SWM revealed hidden connections:")
    print(f"\n1. Immune System <-> Computer Security")
    print(f"   Resonance: {result1.overall_resonance:.2%} | "
          f"Insight Potential: {result1.insight_potential:.2%}")
    print("   Both are adaptive defense systems with memory and coordination")
    
    print(f"\n2. Forest Ecosystem <-> Market Economy")
    print(f"   Resonance: {result2.overall_resonance:.2%} | "
          f"Insight Potential: {result2.insight_potential:.2%}")
    print("   Both are self-regulating networks with resource flows and feedback")
    
    print(f"\n3. Musical Composition <-> Scientific Research")
    print(f"   Resonance: {result3.overall_resonance:.2%} | "
          f"Insight Potential: {result3.insight_potential:.2%}")
    print("   Both are creative processes balancing structure with discovery")
    
    print("\n" + "-"*60)
    print("\nThese cross-domain insights can inspire:")
    print("• Biological principles applied to cybersecurity")
    print("• Ecological models for sustainable economics")
    print("• Artistic methods for scientific breakthroughs")
    print("\nKimera SWM: Seeing the world through spherical understanding!")


if __name__ == "__main__":
    main()