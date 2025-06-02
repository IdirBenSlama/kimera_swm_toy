"""
Test the Multi-Language Analyzer implementation
"""

from src.kimera.linguistics import MultiLanguageAnalyzer, select_unrelated_languages
from src.kimera.dimensions.geoid_v2 import GeoidV2, DimensionType, init_geoid_v2
import json


def test_language_selection():
    """Test the unrelated language selection algorithm"""
    print("Testing Language Selection Algorithm")
    print("=" * 50)
    
    # Test selecting languages unrelated to English
    root_lang = 'en'
    unrelated = select_unrelated_languages(root_lang, n=3)
    print(f"Root language: {root_lang}")
    print(f"Selected unrelated languages: {unrelated}")
    print()
    
    # Test with different root languages
    for root in ['zh', 'ar', 'ja']:
        unrelated = select_unrelated_languages(root, n=3)
        print(f"Root: {root} -> Unrelated: {unrelated}")
    print()


def test_multi_language_analysis():
    """Test the full 1+3+1 analysis"""
    print("Testing Multi-Language Analysis (1+3+1 Rule)")
    print("=" * 50)
    
    # Create analyzer
    analyzer = MultiLanguageAnalyzer()
    
    # Test text about immune system
    test_text = "The immune system protects the body from harmful pathogens by identifying and destroying foreign invaders"
    
    # Perform analysis
    insight = analyzer.analyze(test_text, root_lang='en')
    
    # Display results
    print(f"Analyzed text: '{test_text}'")
    print(f"\nRoot language: {insight.root_analysis.language}")
    print(f"Key concepts: {insight.root_analysis.key_concepts}")
    
    print("\nUnrelated language analyses:")
    for analysis in insight.unrelated_analyses:
        print(f"  {analysis.language}:")
        print(f"    Translation: {analysis.translated_text}")
        print(f"    Unique perspective: {analysis.cultural_context.get('unique_perspective', 'N/A')}")
    
    print("\nSymbolic Layer (+1):")
    print(f"  Archetypes: {insight.symbolic_layer.archetypes}")
    print(f"  Paradoxes: {len(insight.symbolic_layer.paradoxes)}")
    print(f"  Chaos patterns: {insight.symbolic_layer.chaos_patterns}")
    print(f"  Transformation potential: {insight.symbolic_layer.transformation_potential:.2f}")
    
    print(f"\nCross-linguistic patterns:")
    for pattern_type, patterns in insight.cross_linguistic_patterns.items():
        if patterns:
            print(f"  {pattern_type}: {patterns}")
    
    print(f"\nInsight score: {insight.insight_score:.2f}")
    print()


def test_geoid_integration():
    """Test integration with GeoidV2"""
    print("Testing GeoidV2 Integration with Multi-Language Analysis")
    print("=" * 50)
    
    # Create a GeoidV2
    text = "A firewall protects computer networks from malicious attacks"
    geoid = init_geoid_v2(text=text, lang='en')
    
    # Perform multi-language analysis
    analyzer = MultiLanguageAnalyzer()
    insight = analyzer.analyze(text, root_lang='en')
    
    # Add linguistic dimension to geoid
    geoid.add_dimension(
        DimensionType.LINGUISTIC,
        {
            'root_analysis': insight.root_analysis.key_concepts,
            'cross_linguistic': insight.cross_linguistic_patterns,
            'languages_analyzed': [insight.root_analysis.language] + 
                                [a.language for a in insight.unrelated_analyses]
        },
        confidence=insight.insight_score
    )
    
    # Add symbolic dimension
    geoid.add_dimension(
        DimensionType.SYMBOLIC,
        {
            'archetypes': insight.symbolic_layer.archetypes,
            'transformation_potential': insight.symbolic_layer.transformation_potential,
            'chaos_patterns': insight.symbolic_layer.chaos_patterns
        },
        confidence=1.0
    )
    
    print(f"GeoidV2 created for: '{text}'")
    print(f"Dimensions added: {list(geoid.dimensions.keys())}")
    print(f"Dimensional coherence: {geoid.measure_dimensional_coherence():.2f}")
    print()
    
    # Show linguistic insights
    ling_dim = geoid.dimensions[DimensionType.LINGUISTIC]
    print("Linguistic dimension insights:")
    print(f"  Languages analyzed: {ling_dim.value['languages_analyzed']}")
    print(f"  Key concepts: {ling_dim.value['root_analysis']}")
    print(f"  Cross-linguistic patterns: {json.dumps(ling_dim.value['cross_linguistic'], indent=2)}")


def test_resonance_discovery():
    """Test discovering resonance between concepts using multi-language analysis"""
    print("\nTesting Cross-Domain Resonance Discovery")
    print("=" * 50)
    
    analyzer = MultiLanguageAnalyzer()
    
    # Analyze two different concepts
    concept1 = "The immune system identifies and eliminates foreign invaders"
    concept2 = "A firewall filters and blocks unauthorized network traffic"
    
    insight1 = analyzer.analyze(concept1, root_lang='en')
    insight2 = analyzer.analyze(concept2, root_lang='en')
    
    # Compare archetypes
    archetypes1 = set(insight1.symbolic_layer.archetypes)
    archetypes2 = set(insight2.symbolic_layer.archetypes)
    shared_archetypes = archetypes1 & archetypes2
    
    print(f"Concept 1: '{concept1}'")
    print(f"  Archetypes: {archetypes1}")
    print(f"\nConcept 2: '{concept2}'")
    print(f"  Archetypes: {archetypes2}")
    print(f"\nShared archetypes: {shared_archetypes}")
    
    # Compare transformation potential
    print(f"\nTransformation potential:")
    print(f"  Concept 1: {insight1.symbolic_layer.transformation_potential:.2f}")
    print(f"  Concept 2: {insight2.symbolic_layer.transformation_potential:.2f}")
    
    # Calculate resonance based on shared patterns
    if shared_archetypes:
        resonance_score = len(shared_archetypes) / len(archetypes1 | archetypes2)
        print(f"\nResonance score (based on archetypes): {resonance_score:.2f}")
        print("These concepts share deep structural patterns around protection and filtering!")


if __name__ == "__main__":
    test_language_selection()
    test_multi_language_analysis()
    test_geoid_integration()
    test_resonance_discovery()
    
    print("\n" + "=" * 50)
    print("Multi-Language Analyzer testing complete!")
    print("This demonstrates the implementation of the SWM '1+3+1' rule")
    print("for discovering deep patterns across linguistic boundaries.")