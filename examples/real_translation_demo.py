"""
Real Translation Services Demo

This example demonstrates using Google Translate and DeepL APIs
with the Kimera SWM framework.

Requirements:
- For Google Translate: google-cloud-translate library and API credentials
- For DeepL: deepl library and API key
"""

import asyncio
import os
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.kimera.linguistics import create_translation_service
from src.kimera.linguistics.translation_config import (
    TranslationConfig, TranslationServiceManager
)
from src.kimera.geoid import init_geoid
from src.kimera.resonance import resonance


async def test_google_translate():
    """Test Google Translate integration"""
    print("\n=== Google Translate Demo ===")
    
    # Check if credentials are available
    if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        print("⚠️  Google credentials not found. Set GOOGLE_APPLICATION_CREDENTIALS environment variable.")
        print("   Skipping Google Translate demo...")
        return
    
    try:
        # Create Google Translate service
        translator = create_translation_service(
            'google',
            enable_cache=True
        )
        
        # Test translations
        test_phrases = [
            ("Hello, world!", "es"),
            ("The mind is everything", "ja"),
            ("Love transcends all boundaries", "fr"),
            ("Consciousness is the greatest mystery", "de")
        ]
        
        print("\nTranslating phrases:")
        for text, target_lang in test_phrases:
            result = await translator.translate(text, target_lang)
            print(f"\n{text}")
            print(f"  → {target_lang}: {result.translated_text}")
            print(f"  Confidence: {result.confidence:.2f}")
            print(f"  Detected source: {result.source_language}")
        
        # Test language detection
        print("\n\nLanguage detection:")
        multilingual_texts = [
            "Bonjour le monde",
            "Hola mundo",
            "こんにちは世界",
            "Привет мир"
        ]
        
        for text in multilingual_texts:
            lang, confidence = await translator.detect_language(text)
            print(f"{text} → {lang} (confidence: {confidence:.2f})")
        
        # Test batch translation
        print("\n\nBatch translation to Spanish:")
        batch_texts = [
            "Good morning",
            "Good afternoon", 
            "Good evening",
            "Good night"
        ]
        
        results = await translator.batch_translate(batch_texts, "es")
        for i, result in enumerate(results):
            print(f"{batch_texts[i]} → {result.translated_text}")
        
    except Exception as e:
        print(f"❌ Google Translate error: {e}")


async def test_deepl_translate():
    """Test DeepL integration"""
    print("\n\n=== DeepL Demo ===")
    
    # Check if API key is available
    if not os.getenv('DEEPL_API_KEY'):
        print("⚠️  DeepL API key not found. Set DEEPL_API_KEY environment variable.")
        print("   Skipping DeepL demo...")
        return
    
    try:
        # Create DeepL service
        translator = create_translation_service(
            'deepl',
            enable_cache=True,
            api_type='free'  # or 'pro' if you have a pro account
        )
        
        # Test translations
        test_phrases = [
            ("The beauty of nature inspires creativity", "es"),
            ("Artificial intelligence is transforming our world", "fr"),
            ("Peace begins with understanding", "de"),
            ("Knowledge is power", "ja")
        ]
        
        print("\nTranslating phrases with DeepL:")
        for text, target_lang in test_phrases:
            result = await translator.translate(text, target_lang)
            print(f"\n{text}")
            print(f"  → {target_lang}: {result.translated_text}")
            print(f"  Confidence: {result.confidence:.2f}")
        
        # Get usage statistics
        if hasattr(translator, 'get_usage_stats'):
            stats = translator.get_usage_stats()
            print(f"\n\nDeepL usage statistics:")
            print(f"  Characters used: {stats.get('character_count', 'N/A')}")
            print(f"  Character limit: {stats.get('character_limit', 'N/A')}")
            print(f"  Usage: {stats.get('character_usage_percent', 0):.1f}%")
        
    except Exception as e:
        print(f"❌ DeepL error: {e}")


async def test_translation_manager():
    """Test Translation Service Manager with fallback"""
    print("\n\n=== Translation Service Manager Demo ===")
    
    # Create configuration
    config = TranslationConfig(
        default_service='deepl' if os.getenv('DEEPL_API_KEY') else 'mock',
        fallback_service='mock',
        enable_cache=True,
        quality_threshold=0.8
    )
    
    # Add API keys if available
    if os.getenv('DEEPL_API_KEY'):
        config.deepl_config['api_key'] = os.getenv('DEEPL_API_KEY')
    if os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        config.google_config['credentials_path'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    
    # Create manager
    manager = TranslationServiceManager(config)
    
    print(f"Available services: {manager.list_services()}")
    print(f"Primary service: {config.default_service}")
    print(f"Fallback service: {config.fallback_service}")
    
    # Test translation with automatic fallback
    test_text = "The universe is full of infinite possibilities"
    target_langs = ["es", "fr", "de", "ja", "zh"]
    
    print(f"\nTranslating: '{test_text}'")
    for lang in target_langs:
        result = await manager.translate(test_text, lang)
        print(f"  {lang}: {result.translated_text[:50]}...")
        print(f"       (service: {result.metadata.get('service', 'unknown')}, "
              f"confidence: {result.confidence:.2f})")
    
    # Get usage statistics
    print("\n\nService usage statistics:")
    stats = await manager.get_usage_stats()
    for service, service_stats in stats.items():
        print(f"\n{service}:")
        for key, value in service_stats.items():
            print(f"  {key}: {value}")


async def test_swm_integration():
    """Test translation services with SWM components"""
    print("\n\n=== SWM Integration Demo ===")
    
    # Use manager for robust translation
    config = TranslationConfig.from_env()
    manager = TranslationServiceManager(config)
    
    # Concept to analyze
    concept = "consciousness"
    languages = ["en", "es", "fr", "de", "ja"]
    
    print(f"\nAnalyzing '{concept}' across languages using {config.default_service} service...")
    
    # Translate and create geoids
    geoids = {}
    translations = {"en": concept}
    
    for lang in languages[1:]:
        result = await manager.translate(concept, lang, source_language="en")
        translations[lang] = result.translated_text
        print(f"  {lang}: {result.translated_text}")
    
    # Create geoids
    print("\nCreating geoids...")
    for lang, text in translations.items():
        geoid = init_geoid(
            text=text,
            lang=lang,
            layers=["consciousness", "philosophy"]
        )
        geoids[lang] = geoid
    
    # Calculate cross-linguistic resonance
    print("\nCross-linguistic resonance matrix:")
    print("     ", end="")
    for lang in languages:
        print(f"{lang:>6}", end="")
    print()
    
    for lang1 in languages:
        print(f"{lang1:>5}", end="")
        for lang2 in languages:
            if lang1 == lang2:
                score = 1.0
            else:
                score = resonance(geoids[lang1], geoids[lang2])
            print(f"{score:>6.2f}", end="")
        print()
    
    # Find linguistic clusters
    print("\nLinguistic clusters (resonance > 0.5):")
    clusters = []
    threshold = 0.5
    
    for i, lang1 in enumerate(languages):
        for lang2 in languages[i+1:]:
            score = resonance(geoids[lang1], geoids[lang2])
            if score > threshold:
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


async def save_config_example():
    """Example of saving and loading configuration"""
    print("\n\n=== Configuration Management Demo ===")
    
    # Create a configuration
    config = TranslationConfig(
        default_service='deepl',
        fallback_service='google',
        enable_cache=True,
        cache_ttl=3600,  # 1 hour
        batch_size=100,
        quality_threshold=0.85,
        preferred_variants={
            'en': 'en-US',
            'es': 'es-ES',
            'pt': 'pt-BR'
        }
    )
    
    # Save to file
    config_path = "translation_config.json"
    config.to_file(config_path)
    print(f"Configuration saved to {config_path}")
    
    # Load from file
    loaded_config = TranslationConfig.from_file(config_path)
    print(f"\nLoaded configuration:")
    print(f"  Default service: {loaded_config.default_service}")
    print(f"  Fallback service: {loaded_config.fallback_service}")
    print(f"  Cache enabled: {loaded_config.enable_cache}")
    print(f"  Quality threshold: {loaded_config.quality_threshold}")
    
    # Clean up
    Path(config_path).unlink(missing_ok=True)


async def main():
    """Run all demonstrations"""
    print("=" * 60)
    print("Kimera SWM - Real Translation Services Demo")
    print("=" * 60)
    
    # Test individual services
    await test_google_translate()
    await test_deepl_translate()
    
    # Test service manager
    await test_translation_manager()
    
    # Test SWM integration
    await test_swm_integration()
    
    # Configuration example
    await save_config_example()
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("\nTo use real translation services:")
    print("1. For Google Translate:")
    print("   - Install: pip install google-cloud-translate")
    print("   - Set GOOGLE_APPLICATION_CREDENTIALS environment variable")
    print("2. For DeepL:")
    print("   - Install: pip install deepl")
    print("   - Set DEEPL_API_KEY environment variable")
    print("3. Configure default service:")
    print("   - Set KIMERA_TRANSLATION_SERVICE environment variable")
    print("   - Or use TranslationConfig for programmatic configuration")


if __name__ == "__main__":
    asyncio.run(main())