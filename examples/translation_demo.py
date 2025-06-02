"""
Translation Service Demo

This script demonstrates the translation service capabilities including:
- Basic translation
- Language detection
- Batch translation
- Caching behavior
- Performance metrics
"""

import asyncio
import time
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.kimera.linguistics import (
    create_translation_service,
    TranslationCache
)


async def basic_translation_demo():
    """Demonstrate basic translation functionality"""
    print("\n=== Basic Translation Demo ===")
    
    # Create translation service with caching
    service = create_translation_service(
        service_type='mock',
        enable_cache=True,
        cache_ttl=3600
    )
    
    # Test translations
    test_phrases = [
        ("hello", "es"),
        ("world", "fr"),
        ("love", "de"),
        ("hello", "ja"),
        ("peace", "ar"),
    ]
    
    for text, target_lang in test_phrases:
        result = await service.translate(text, target_lang)
        print(f"\n'{text}' -> {target_lang}:")
        print(f"  Translation: {result.translated_text}")
        print(f"  Source language: {result.source_language}")
        print(f"  Confidence: {result.confidence:.2f}")
    
    # Test cache hit
    print("\n--- Testing cache hit ---")
    start = time.time()
    result1 = await service.translate("hello", "es")
    time1 = time.time() - start
    
    start = time.time()
    result2 = await service.translate("hello", "es")  # Should hit cache
    time2 = time.time() - start
    
    print(f"First call: {time1:.4f}s")
    print(f"Second call (cached): {time2:.4f}s")
    if time2 > 0:
        print(f"Speedup: {time1/time2:.1f}x")
    else:
        print("Speedup: Instant (from cache)")
    
    # Show cache statistics
    if hasattr(service, 'get_cache_stats'):
        stats = service.get_cache_stats()
        print(f"\nCache stats: {stats}")


async def language_detection_demo():
    """Demonstrate language detection"""
    print("\n=== Language Detection Demo ===")
    
    service = create_translation_service('mock')
    
    test_texts = [
        "Hello world",
        "Hola mundo",
        "Bonjour le monde",
        "こんにちは世界",
        "你好世界",
        "مرحبا بالعالم",
        "Привет мир"
    ]
    
    for text in test_texts:
        lang, confidence = await service.detect_language(text)
        print(f"'{text}' -> Language: {lang} (confidence: {confidence:.2f})")


async def batch_translation_demo():
    """Demonstrate batch translation"""
    print("\n=== Batch Translation Demo ===")
    
    service = create_translation_service('mock', enable_cache=True)
    
    # Batch of texts to translate
    texts = [
        "Hello", "World", "Love", "Peace", "Friend",
        "Family", "Hope", "Dream", "Future", "Together"
    ]
    
    # Translate to Spanish
    print("\nTranslating batch to Spanish...")
    start = time.time()
    results = await service.batch_translate(texts, "es")
    elapsed = time.time() - start
    
    for i, result in enumerate(results):
        print(f"{texts[i]} -> {result.translated_text}")
    
    print(f"\nBatch translation time: {elapsed:.3f}s")
    print(f"Average per text: {elapsed/len(texts):.3f}s")
    
    # Translate same batch again (should be cached)
    print("\nTranslating same batch again (cached)...")
    start = time.time()
    results2 = await service.batch_translate(texts, "es")
    elapsed2 = time.time() - start
    
    print(f"Cached batch time: {elapsed2:.3f}s")
    if elapsed2 > 0:
        print(f"Speedup: {elapsed/elapsed2:.1f}x")
    else:
        print("Speedup: Instant (from cache)")


async def advanced_cache_demo():
    """Demonstrate advanced caching features"""
    print("\n=== Advanced Cache Demo ===")
    
    # Create cache with persistence
    cache = TranslationCache(
        cache_dir=Path("./test_cache"),
        max_memory_items=100,
        max_disk_items=1000,
        ttl_seconds=3600,
        enable_persistence=True
    )
    
    # Create service with custom cache
    base_service = create_translation_service('mock', enable_cache=False)
    
    # Simulate some translations
    print("\nPopulating cache...")
    for i in range(20):
        text = f"test_{i}"
        for lang in ['es', 'fr', 'de']:
            result = await base_service.translate(text, lang)
            cache_key = f"{text}|{lang}"
            await cache.put(cache_key, result)
    
    # Show cache statistics
    stats = cache.get_stats()
    print(f"\nCache statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test cache retrieval
    print("\nTesting cache retrieval...")
    test_key = "test_5|es"
    result = await cache.get(test_key)
    if result:
        print(f"Retrieved from cache: {result.source_text} -> {result.translated_text}")
    
    # Export cache
    export_path = Path("./test_cache/cache_export.pkl")
    exported = await cache.export_cache(export_path)
    print(f"\nExported {exported} entries to {export_path}")
    
    # Clean up expired entries
    cleaned = await cache.cleanup_expired()
    print(f"Cleaned up {cleaned} expired entries")
    
    # Clear cache
    await cache.clear()
    print("Cache cleared")


async def multi_language_analysis_demo():
    """Demonstrate multi-language analysis for SWM"""
    print("\n=== Multi-Language Analysis Demo ===")
    
    service = create_translation_service('mock', enable_cache=True)
    
    # Concept to analyze across languages
    concept = "love"
    languages = ['es', 'fr', 'de', 'it', 'pt', 'ja', 'zh', 'ar']
    
    print(f"\nAnalyzing concept '{concept}' across languages:")
    
    translations = {}
    for lang in languages:
        result = await service.translate(concept, lang)
        translations[lang] = result
        print(f"  {lang}: {result.translated_text}")
    
    # Simulate pattern extraction (would integrate with SWM patterns)
    print("\nCross-linguistic patterns:")
    print("  - Romance languages (es, fr, it, pt) show similar roots")
    print("  - Germanic languages (de) have distinct patterns")
    print("  - Asian languages (ja, zh) use ideographic representations")
    print("  - Semitic languages (ar) have triconsonantal roots")
    
    # Show how this would feed into SWM
    print("\nSWM Integration Points:")
    print("  1. Each translation becomes a node in the linguistic network")
    print("  2. Semantic similarities create resonance patterns")
    print("  3. Cultural contexts add dimensional depth")
    print("  4. Evolution tracking shows conceptual drift across languages")


async def main():
    """Run all demos"""
    print("Kimera Translation Service Demo")
    print("=" * 50)
    
    # Run demos
    await basic_translation_demo()
    await language_detection_demo()
    await batch_translation_demo()
    await advanced_cache_demo()
    await multi_language_analysis_demo()
    
    print("\n" + "=" * 50)
    print("Demo completed!")


if __name__ == "__main__":
    asyncio.run(main())