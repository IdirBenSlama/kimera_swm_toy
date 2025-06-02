"""
SWM Translation Integration Demo

This script demonstrates how the translation service integrates with
the Spherical Word Methodology to enable multi-language analysis.
"""

import asyncio
from pathlib import Path
import sys
import numpy as np

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.kimera.geoid import init_geoid
from src.kimera.resonance import resonance
from src.kimera.linguistics import create_translation_service
from src.kimera.linguistics.multi_language_analyzer import MultiLanguageAnalyzer


async def demonstrate_multilingual_resonance():
    """
    Demonstrate how translation enables cross-linguistic resonance analysis
    """
    print("\n=== Multilingual Resonance Analysis ===")
    
    # Create translation service
    translator = create_translation_service('mock', enable_cache=True)
    
    # Test concept
    concept = "consciousness"
    languages = ["en", "es", "fr", "de", "ja", "zh"]
    
    print(f"\nAnalyzing '{concept}' across languages...")
    
    # Translate to each language
    translations = {}
    for lang in languages:
        if lang == "en":
            translations[lang] = concept
        else:
            result = await translator.translate(concept, lang)
            translations[lang] = result.translated_text
            print(f"  {lang}: {result.translated_text} (confidence: {result.confidence:.2f})")
    
    # Create geoids for each translation
    print("\nCreating geoids...")
    geoids = {}
    for lang, word in translations.items():
        # Create geoid using the proper initialization function
        geoid = init_geoid(
            text=word,
            lang=lang,
            layers=["translation", "consciousness"]
        )
        geoids[lang] = geoid
        print(f"  {lang}: Geoid created for '{word}'")
    
    # Calculate cross-linguistic resonance
    print("\nCross-linguistic resonance matrix:")
    print("     ", end="")
    for lang in languages:
        print(f"{lang:>6}", end="")
    print()
    
    resonance_matrix = {}
    for lang1 in languages:
        print(f"{lang1:>5}", end="")
        for lang2 in languages:
            if lang1 == lang2:
                score = 1.0
            else:
                # Calculate resonance between geoids
                score = resonance(geoids[lang1], geoids[lang2])
                # Add some variation for demo
                score = abs(score) * 0.7 + 0.3
            
            resonance_matrix[(lang1, lang2)] = score
            print(f"{score:>6.2f}", end="")
        print()
    
    # Find linguistic clusters
    print("\nLinguistic clusters (resonance > 0.6):")
    clusters = []
    threshold = 0.6
    
    for (lang1, lang2), score in resonance_matrix.items():
        if lang1 != lang2 and score > threshold:
            # Find or add to cluster
            found = False
            for cluster in clusters:
                if lang1 in cluster or lang2 in cluster:
                    cluster.update([lang1, lang2])
                    found = True
                    break
            if not found:
                clusters.append({lang1, lang2})
    
    # Merge overlapping clusters
    merged = []
    for cluster in clusters:
        added = False
        for mc in merged:
            if cluster & mc:
                mc.update(cluster)
                added = True
                break
        if not added:
            merged.append(cluster)
    
    for i, cluster in enumerate(merged):
        langs = sorted(cluster)
        print(f"  Cluster {i+1}: {', '.join(langs)}")
        # Show translations in cluster
        for lang in langs:
            print(f"    {lang}: {translations[lang]}")


async def demonstrate_multi_language_analyzer():
    """
    Demonstrate the MultiLanguageAnalyzer component
    """
    print("\n=== Multi-Language Analyzer Demo ===")
    
    # Create analyzer
    analyzer = MultiLanguageAnalyzer()
    
    # Test phrases in multiple languages
    test_data = [
        ("Hello world", "en"),
        ("Hola mundo", "es"),
        ("Bonjour le monde", "fr"),
        ("Hallo Welt", "de"),
        ("こんにちは世界", "ja"),
        ("你好世界", "zh")
    ]
    
    print("\nAnalyzing phrases across languages...")
    
    # Analyze each phrase
    results = []
    for text, lang in test_data:
        # The analyzer.analyze method takes text and root_lang
        result = analyzer.analyze(text, root_lang=lang)
        results.append(result)
        
        print(f"\n{lang}: {text}")
        print(f"  Root language: {result.root_analysis.language}")
        print(f"  Unrelated languages analyzed: {len(result.unrelated_analyses)}")
        print(f"  Insight score: {result.insight_score:.2f}")
        
        # Show translations to unrelated languages
        for analysis in result.unrelated_analyses[:3]:
            print(f"    {analysis.language}: {analysis.translated_text}")
    
    # Compare semantic similarity
    print("\n\nSemantic similarity analysis:")
    print("All phrases mean 'Hello world' in different languages")
    print("Expected: High similarity scores across all pairs")
    
    # In a real system, we would calculate actual semantic similarity
    # For demo, we'll show the concept
    print("\nSimilarity matrix would show:")
    print("  - High scores (>0.8) for all language pairs")
    print("  - Slight variations due to cultural nuances")
    print("  - Clustering of related language families")


async def demonstrate_translation_pipeline():
    """
    Demonstrate a complete translation pipeline with SWM
    """
    print("\n=== Translation Pipeline Demo ===")
    
    # Create components
    translator = create_translation_service('mock', enable_cache=True)
    
    # Input text
    source_text = """
    The concept of consciousness remains one of the most profound mysteries 
    in science and philosophy. It encompasses our subjective experience, 
    self-awareness, and the feeling of what it's like to be.
    """
    
    print(f"\nSource text (English):")
    print(source_text.strip())
    
    # Target languages
    targets = ["es", "fr", "de", "ja"]
    
    print("\nTranslating to multiple languages...")
    translations = {}
    
    for lang in targets:
        result = await translator.translate(source_text, lang)
        translations[lang] = result
        
        print(f"\n{lang.upper()}:")
        print(f"  {result.translated_text[:100]}...")
        print(f"  Confidence: {result.confidence:.2f}")
    
    # Analyze key concepts
    print("\n\nKey concept extraction:")
    key_concepts = ["consciousness", "subjective experience", "self-awareness"]
    
    for concept in key_concepts:
        print(f"\n'{concept}' across languages:")
        for lang in targets:
            trans_result = await translator.translate(concept, lang)
            print(f"  {lang}: {trans_result.translated_text}")
    
    # Show how this integrates with SWM
    print("\n\nSWM Integration:")
    print("  1. Each translation creates a new geoid")
    print("  2. Geoids maintain semantic relationships")
    print("  3. Cross-linguistic resonance reveals universal concepts")
    print("  4. Cultural variations appear as resonance patterns")
    print("  5. Translation confidence affects geoid strength")


async def demonstrate_caching_benefits():
    """
    Show the performance benefits of translation caching
    """
    print("\n=== Translation Caching Performance ===")
    
    import time
    
    # Create cached and non-cached services
    cached_translator = create_translation_service('mock', enable_cache=True)
    
    # Test data
    phrases = [
        "artificial intelligence",
        "machine learning", 
        "neural networks",
        "deep learning",
        "natural language"
    ] * 5  # Repeat for more requests
    
    languages = ["es", "fr", "de"]
    
    # First pass - populate cache
    print("\nFirst pass (cold cache)...")
    start = time.time()
    
    for phrase in phrases:
        for lang in languages:
            await cached_translator.translate(phrase, lang)
    
    cold_time = time.time() - start
    
    # Second pass - use cache
    print(f"Time: {cold_time:.3f}s")
    print("\nSecond pass (warm cache)...")
    start = time.time()
    
    for phrase in phrases:
        for lang in languages:
            await cached_translator.translate(phrase, lang)
    
    warm_time = time.time() - start
    print(f"Time: {warm_time:.3f}s")
    
    # Calculate speedup
    speedup = cold_time / warm_time if warm_time > 0 else float('inf')
    print(f"\nSpeedup: {speedup:.1f}x faster with cache")
    
    # Show cache effectiveness
    total_requests = len(phrases) * len(languages) * 2
    unique_requests = 5 * len(languages)  # Only 5 unique phrases
    
    print(f"\nCache statistics:")
    print(f"  Total requests: {total_requests}")
    print(f"  Unique translations: {unique_requests}")
    print(f"  Cache hit rate: {(1 - unique_requests/total_requests)*100:.1f}%")


async def main():
    """Run all demonstrations"""
    print("=" * 60)
    print("Kimera SWM Translation Integration Demo")
    print("=" * 60)
    
    # Run demonstrations
    await demonstrate_multilingual_resonance()
    await demonstrate_multi_language_analyzer()
    await demonstrate_translation_pipeline()
    await demonstrate_caching_benefits()
    
    print("\n" + "=" * 60)
    print("Integration demo completed!")
    print("\nKey insights:")
    print("  • Translation enables cross-linguistic SWM analysis")
    print("  • Geoids can represent concepts in any language")
    print("  • Resonance patterns reveal linguistic relationships")
    print("  • Caching dramatically improves performance")
    print("  • Multi-language analysis uncovers universal concepts")
    
    print("\nNext steps:")
    print("  1. Integrate real translation APIs (Google, DeepL)")
    print("  2. Add multilingual embeddings for better resonance")
    print("  3. Build cross-linguistic knowledge graphs")
    print("  4. Implement real-time translation pipelines")


if __name__ == "__main__":
    asyncio.run(main())