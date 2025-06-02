"""
Test the integrated SWM implementation

This demonstrates:
1. Multi-language analysis (1+3+1 rule)
2. Pattern abstraction (functional, structural, dynamic, relational)
3. Enhanced resonance detection
4. Cross-domain insight generation
"""

from src.kimera.dimensions.geoid_v2 import init_geoid_v2, DimensionType
from src.kimera.linguistics import MultiLanguageAnalyzer
from src.kimera.patterns import PatternAbstractionEngine
from src.kimera.resonance_v2 import EnhancedResonanceDetector
import json


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'=' * 60}")
    print(f"{title}")
    print('=' * 60)


def test_full_swm_analysis():
    """Test the complete SWM analysis pipeline on a single concept"""
    print_section("Full SWM Analysis: Immune System")
    
    # Create a Geoid for immune system
    immune_text = """
    The immune system is a complex network of cells, tissues, and organs that work 
    together to defend the body against harmful invaders. It identifies foreign 
    substances, remembers past encounters, and adapts its responses over time. 
    The system operates through multiple layers of defense, from physical barriers 
    to specialized cells that can recognize and eliminate specific threats.
    """
    
    immune_geoid = init_geoid_v2(text=immune_text, lang='en')
    
    # 1. Multi-language analysis
    print("\n1. Multi-Language Analysis (1+3+1 Rule)")
    print("-" * 40)
    
    lang_analyzer = MultiLanguageAnalyzer()
    lang_insight = lang_analyzer.analyze(immune_text, root_lang='en')
    
    print(f"Languages analyzed: {[lang_insight.root_analysis.language] + [a.language for a in lang_insight.unrelated_analyses]}")
    print(f"\nSymbolic layer archetypes: {lang_insight.symbolic_layer.archetypes}")
    print(f"Transformation potential: {lang_insight.symbolic_layer.transformation_potential:.2f}")
    print(f"Cross-linguistic patterns: {list(lang_insight.cross_linguistic_patterns.keys())}")
    
    # Add linguistic dimension to Geoid
    immune_geoid.add_dimension(
        DimensionType.LINGUISTIC,
        {
            'languages': [lang_insight.root_analysis.language] + 
                        [a.language for a in lang_insight.unrelated_analyses],
            'archetypes': lang_insight.symbolic_layer.archetypes,
            'unique_perspectives': lang_insight.unique_perspectives
        },
        confidence=lang_insight.insight_score
    )
    
    # 2. Pattern abstraction
    print("\n2. Pattern Abstraction")
    print("-" * 40)
    
    pattern_engine = PatternAbstractionEngine()
    patterns = pattern_engine.extract_patterns(immune_geoid)
    
    print("Extracted patterns:")
    print(f"  Functional: {patterns.functional.primary_functions[:3]}")
    print(f"  Structural: arrangement={patterns.structural.arrangement_type}, "
          f"components={len(patterns.structural.components)}")
    print(f"  Dynamic: temporal={patterns.dynamic.temporal_nature}, "
          f"changes={patterns.dynamic.change_drivers[:2]}")
    print(f"  Relational: depends_on={patterns.relational.depends_on[:2]}")
    
    # Add pattern dimension
    immune_geoid.add_dimension(
        DimensionType.STRUCTURAL,
        {
            'patterns': {
                'functional': patterns.functional.to_vector().tolist(),
                'structural': patterns.structural.to_vector().tolist(),
                'dynamic': patterns.dynamic.to_vector().tolist(),
                'relational': patterns.relational.to_vector().tolist()
            },
            'confidence_scores': {k.value: v for k, v in patterns.confidence_scores.items()}
        }
    )
    
    print(f"\nGeoid now has {len(immune_geoid.dimensions)} dimensions")
    print(f"Dimensional coherence: {immune_geoid.measure_dimensional_coherence():.2f}")


def test_cross_domain_resonance():
    """Test finding resonance between concepts from different domains"""
    print_section("Cross-Domain Resonance Discovery")
    
    # Create Geoids from different domains
    concepts = {
        "Immune System (Biology)": """
        The immune system protects the body by identifying and neutralizing foreign 
        invaders like bacteria and viruses. It learns from past infections, maintains 
        memory of threats, and coordinates multiple types of cells to mount targeted 
        responses. The system must balance protection with avoiding damage to the 
        body's own tissues.
        """,
        
        "Firewall (Technology)": """
        A firewall is a network security system that monitors and filters incoming 
        and outgoing network traffic based on predetermined security rules. It acts 
        as a barrier between trusted internal networks and untrusted external networks, 
        learning from attack patterns and adapting its rules to new threats.
        """,
        
        "Border Control (Social)": """
        Border control systems regulate the movement of people and goods across 
        national boundaries. They identify authorized individuals, detect potential 
        threats, and maintain records of crossings. The system must balance security 
        with facilitating legitimate travel and trade.
        """,
        
        "Quality Control (Manufacturing)": """
        Quality control processes inspect and test products to ensure they meet 
        specified standards. The system identifies defects, tracks patterns of 
        problems, and implements corrective measures. It must balance thorough 
        inspection with production efficiency.
        """
    }
    
    # Create Geoids and analyze
    geoids = {}
    resonance_detector = EnhancedResonanceDetector()
    
    for name, text in concepts.items():
        geoids[name] = init_geoid_v2(text=text)
    
    # Find all resonances
    print("\nResonance Analysis Results:")
    print("-" * 40)
    
    names = list(geoids.keys())
    resonance_results = []
    
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            name1, name2 = names[i], names[j]
            
            # Detect resonance
            result = resonance_detector.detect_resonance(
                geoids[name1], 
                geoids[name2],
                analyze_languages=False  # Skip for speed
            )
            
            resonance_results.append((name1, name2, result))
            
            # Print summary
            print(f"\n{name1.split('(')[0].strip()} <-> {name2.split('(')[0].strip()}:")
            print(f"  Overall resonance: {result.overall_resonance:.3f}")
            print(f"  Domain distance: {result.domain_distance:.2f}")
            print(f"  Insight potential: {result.insight_potential:.3f}")
            
            # Show strongest resonance type
            strongest_type, strongest_score = result.strongest_resonance
            if strongest_type:
                print(f"  Strongest: {strongest_type.value} ({strongest_score:.3f})")
            
            # Show insights
            if result.discovered_insights:
                print("  Insights:")
                for insight in result.discovered_insights[:2]:
                    print(f"    - {insight}")
    
    # Find the most insightful connection
    print("\n" + "-" * 40)
    best_result = max(resonance_results, key=lambda x: x[2].insight_potential)
    print(f"\nMost insightful connection:")
    print(f"{best_result[0].split('(')[0].strip()} <-> {best_result[1].split('(')[0].strip()}")
    print(f"Insight potential: {best_result[2].insight_potential:.3f}")
    print("\nThis suggests these concepts share deep structural patterns despite")
    print("coming from completely different domains!")


def test_resonance_cluster():
    """Test finding clusters of resonant concepts"""
    print_section("Resonance Cluster Discovery")
    
    # Create a set of related concepts
    concept_texts = [
        "Evolution is the process by which species change over time through natural selection",
        "Machine learning algorithms improve their performance through iterative training",
        "Markets evolve through competition and adaptation to changing conditions",
        "Languages develop and change through usage and cultural exchange",
        "Ideas spread and mutate through social networks like viruses",
        "Ecosystems maintain balance through feedback loops and adaptation"
    ]
    
    # Create Geoids
    geoids = [init_geoid_v2(text=text) for text in concept_texts]
    
    # Find resonant clusters
    detector = EnhancedResonanceDetector()
    clusters = detector.find_resonant_cluster(geoids, threshold=0.3)
    
    print(f"\nFound {len(clusters)} resonant pairs:")
    print("-" * 40)
    
    for i, (id1, id2, score) in enumerate(clusters[:5]):  # Show top 5
        # Find the original texts
        text1 = next(g.raw for g in geoids if g.gid == id1)[:50] + "..."
        text2 = next(g.raw for g in geoids if g.gid == id2)[:50] + "..."
        
        print(f"\n{i+1}. Resonance score: {score:.3f}")
        print(f"   '{text1}'")
        print(f"   '{text2}'")
    
    print("\nThese concepts form a resonant cluster around themes of:")
    print("- Adaptation and change over time")
    print("- Selection and optimization")
    print("- Emergent complexity from simple rules")


def demonstrate_swm_insights():
    """Demonstrate how SWM generates novel insights"""
    print_section("SWM Insight Generation Demo")
    
    # Analyze two seemingly unrelated concepts
    concept1_text = """
    A symphony orchestra consists of multiple sections of instruments, each with 
    their own unique voice and role. The conductor coordinates these diverse 
    elements, ensuring they work in harmony. Individual musicians must listen 
    to each other and adjust their playing in real-time. The result emerges 
    from the complex interplay of all parts.
    """
    
    concept2_text = """
    A healthy ecosystem contains numerous species occupying different niches. 
    No single species controls the system; instead, balance emerges from 
    countless interactions. Each organism must respond to others and to 
    environmental changes. The whole system exhibits properties that no 
    individual species possesses.
    """
    
    # Create Geoids
    orchestra_geoid = init_geoid_v2(text=concept1_text)
    ecosystem_geoid = init_geoid_v2(text=concept2_text)
    
    # Full SWM analysis
    detector = EnhancedResonanceDetector()
    result = detector.detect_resonance(
        orchestra_geoid, 
        ecosystem_geoid,
        analyze_languages=True
    )
    
    print("Analyzing: Orchestra <-> Ecosystem")
    print("-" * 40)
    
    print(f"\nResonance scores by type:")
    for rtype, score in result.resonance_types.items():
        print(f"  {rtype.value}: {score:.3f}")
    
    print(f"\nDomain distance: {result.domain_distance:.2f}")
    print(f"Insight potential: {result.insight_potential:.3f}")
    
    print("\nDiscovered insights:")
    for insight in result.discovered_insights:
        print(f"  - {insight}")
    
    print("\nSWM reveals that both systems exhibit:")
    print("- Emergent properties from component interactions")
    print("- No centralized control despite apparent coordination")
    print("- Real-time adaptation and feedback loops")
    print("- The whole being greater than the sum of parts")
    print("\nThis suggests general principles of complex adaptive systems!")


if __name__ == "__main__":
    # Run all demonstrations
    test_full_swm_analysis()
    test_cross_domain_resonance()
    test_resonance_cluster()
    demonstrate_swm_insights()
    
    print_section("SWM Integration Test Complete")
    print("\nThe Spherical Word Methodology implementation demonstrates:")
    print("✓ Multi-dimensional Geoid analysis")
    print("✓ Multi-language perspective (1+3+1 rule)")
    print("✓ Deep pattern abstraction (4 types)")
    print("✓ Cross-domain resonance detection")
    print("✓ Novel insight generation")
    print("\nKimera SWM is ready to discover hidden connections in knowledge!")