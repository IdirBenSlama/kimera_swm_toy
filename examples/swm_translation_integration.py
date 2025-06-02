"""
SWM Translation Integration Demo

This script demonstrates how the translation service integrates with
the Spherical Word Methodology to enable multi-language analysis.
"""

import asyncio
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.kimera.geoid import Geoid
from src.kimera.resonance import ResonanceAnalyzer
from src.kimera.pattern_extraction import PatternExtractor
from src.kimera.linguistics import create_translation_service


async def analyze_concept_across_languages(concept: str, languages: list):
    """
    Analyze a concept across multiple languages using SWM
    """
    print(f"\n=== Analyzing '{concept}' across languages ===")
    
    # Create translation service
    translator = create_translation_service('mock', enable_cache=True)
    
    # Create pattern extractor and resonance analyzer
    pattern_extractor = PatternExtractor()
    resonance_analyzer = ResonanceAnalyzer()
    
    # Storage for geoids and translations
    geoids = {}
    translations = {}
    
    # Translate concept to each language
    print("\nTranslating concept...")
    for lang in languages:
        result = await translator.translate(concept, lang)
        translations[lang] = result
        print(f"  {lang}: {result.translated_text}")
    
    # Create geoids for each translation
    print("\nCreating geoids...")
    for lang, trans_result in translations.items():
        # Create geoid with translation metadata
        geoid = Geoid(
            word=trans_result.translated_text,
            metadata={
                'language': lang,
                'original': concept,
                'confidence': trans_result.confidence,
                'source_language': trans_result.source_language
            }
        )
        geoids[lang] = geoid
        print(f"  {lang}: Geoid created for '{trans_result.translated_text}'")
    
    # Extract patterns from each geoid
    print("\nExtracting patterns...")
    patterns_by_lang = {}
    for lang, geoid in geoids.items():
        patterns = pattern_extractor.extract_patterns(geoid)
        patterns_by_lang[lang] = patterns
        print(f"  {lang}: {len(patterns)} patterns extracted")
    
    # Analyze resonance between language pairs
    print("\nAnalyzing cross-linguistic resonance...")
    resonance_results = {}
    
    # Compare each language pair
    for i, lang1 in enumerate(languages):
        for lang2 in languages[i+1:]:
            geoid1 = geoids[lang1]
            geoid2 = geoids[lang2]
            
            resonance = resonance_analyzer.calculate_resonance(geoid1, geoid2)
            pair_key = f"{lang1}-{lang2}"
            resonance_results[pair_key] = resonance
            
            print(f"  {pair_key}: {resonance:.3f}")
    
    # Find linguistic clusters
    print("\nLinguistic clusters (high resonance):")
    threshold = 0.5
    clusters = []
    
    for pair, resonance in resonance_results.items():
        if resonance > threshold:
            lang1, lang2 = pair.split('-')
            # Find or create cluster
            found = False
            for cluster in clusters:
                if lang1 in cluster or lang2 in cluster:
                    cluster.update([lang1, lang2])
                    found = True
                    break
            if not found:
                clusters.append({lang1, lang2})
    
    # Merge overlapping clusters
    merged_clusters = []
    for cluster in clusters:
        merged = False
        for mc in merged_clusters:
            if cluster & mc:  # If there's overlap
                mc.update(cluster)
                merged = True
                break
        if not merged:
            merged_clusters.append(cluster)
    
    for i, cluster in enumerate(merged_clusters):
        print(f"  Cluster {i+1}: {', '.join(sorted(cluster))}")
    
    return {
        'concept': concept,
        'translations': translations,
        'geoids': geoids,
        'patterns': patterns_by_lang,
        'resonance': resonance_results,
        'clusters': merged_clusters
    }


async def demonstrate_conceptual_evolution():
    """
    Demonstrate how concepts evolve across languages
    """
    print("\n=== Conceptual Evolution Demo ===")
    
    # Analyze multiple related concepts
    concepts = ["love", "heart", "soul", "spirit"]
    languages = ["en", "es", "fr", "de", "ja"]
    
    translator = create_translation_service('mock', enable_cache=True)
    
    # Build conceptual network
    conceptual_network = {}
    
    for concept in concepts:
        print(f"\nAnalyzing '{concept}'...")
        
        # Get translations
        translations = {}
        for lang in languages:
            if lang == "en":
                translations[lang] = concept
            else:
                result = await translator.translate(concept, lang)
                translations[lang] = result.translated_text
        
        conceptual_network[concept] = translations
    
    # Show conceptual relationships
    print("\nConceptual Network:")
    for concept, trans in conceptual_network.items():
        print(f"\n{concept}:")
        for lang, word in trans.items():
            print(f"  {lang}: {word}")
    
    # Identify cross-linguistic patterns
    print("\nCross-linguistic patterns:")
    print("  - Romance languages (es, fr) show Latin roots")
    print("  - Germanic languages (de, en) share common ancestry")
    print("  - Japanese (ja) uses both native and borrowed terms")
    print("  - Conceptual boundaries vary by culture")


async def demonstrate_translation_caching():
    """
    Demonstrate the performance benefits of translation caching
    """
    print("\n=== Translation Caching Performance ===")
    
    import time
    
    # Create service with caching
    translator = create_translation_service('mock', enable_cache=True)
    
    # Test data
    test_phrases = [
        "Hello world",
        "Artificial intelligence",
        "Machine learning",
        "Natural language processing",
        "Deep learning"
    ] * 10  # Repeat for more data
    
    languages = ["es", "fr", "de"]
    
    # First pass - populate cache
    print("\nFirst pass (populating cache)...")
    start = time.time()
    
    for phrase in test_phrases:
        for lang in languages:
            await translator.translate(phrase, lang)
    
    first_pass_time = time.time() - start
    print(f"Time: {first_pass_time:.2f}s")
    
    # Second pass - use cache
    print("\nSecond pass (using cache)...")
    start = time.time()
    
    for phrase in test_phrases:
        for lang in languages:
            await translator.translate(phrase, lang)
    
    second_pass_time = time.time() - start
    print(f"Time: {second_pass_time:.2f}s")
    
    # Show improvement
    speedup = first_pass_time / second_pass_time
    print(f"\nSpeedup: {speedup:.1f}x")
    
    # Show cache statistics
    if hasattr(translator, 'get_cache_stats'):
        stats = translator.get_cache_stats()
        print(f"\nCache statistics:")
        print(f"  Total requests: {stats['total_requests']}")
        print(f"  Cache hits: {stats['hits']}")
        print(f"  Cache misses: {stats['misses']}")
        print(f"  Hit rate: {stats['hit_rate']:.1%}")


async def main():
    """Run all demonstrations"""
    print("Kimera SWM Translation Integration Demo")
    print("=" * 50)
    
    # Analyze a concept across languages
    result = await analyze_concept_across_languages(
        "consciousness", 
        ["en", "es", "fr", "de", "ja", "zh"]
    )
    
    # Demonstrate conceptual evolution
    await demonstrate_conceptual_evolution()
    
    # Show caching benefits
    await demonstrate_translation_caching()
    
    print("\n" + "=" * 50)
    print("Integration demo completed!")
    print("\nNext steps:")
    print("  1. Implement Google Translate API integration")
    print("  2. Add Hugging Face model support")
    print("  3. Integrate with advanced NLP features")
    print("  4. Build real-time translation pipeline")


if __name__ == "__main__":
    asyncio.run(main())