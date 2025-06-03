"""
Test Translation Services
========================

Demo script to test the various translation services implemented for Kimera.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from kimera.linguistics.translation_service import create_translation_service
from kimera.linguistics.translation_config import get_config
from kimera.linguistics.translation_cache import create_translation_cache


async def test_mock_service():
    """Test the mock translation service."""
    print("\n" + "="*60)
    print("Testing Mock Translation Service")
    print("="*60)
    
    service = create_translation_service(service_type='mock', enable_cache=True)
    
    # Test single translation
    result = await service.translate("Hello world", "es")
    print(f"\nEnglish -> Spanish:")
    print(f"  Source: {result.source_text}")
    print(f"  Translation: {result.translated_text}")
    print(f"  Confidence: {result.confidence}")
    
    # Test language detection
    lang, conf = await service.detect_language("Bonjour le monde")
    print(f"\nLanguage detection for 'Bonjour le monde':")
    print(f"  Detected: {lang} (confidence: {conf})")
    
    # Test batch translation
    texts = ["Hello", "World", "Love", "Peace"]
    results = await service.batch_translate(texts, "fr")
    print(f"\nBatch translation to French:")
    for r in results:
        print(f"  {r.source_text} -> {r.translated_text}")
    
    # Test cache
    if hasattr(service, 'get_cache_stats'):
        stats = service.get_cache_stats()
        print(f"\nCache stats: {stats}")


async def test_google_service():
    """Test Google Translate service (requires API credentials)."""
    print("\n" + "="*60)
    print("Testing Google Translate Service")
    print("="*60)
    
    # Check if credentials are available
    if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        print("  ⚠️  Google credentials not found. Set GOOGLE_APPLICATION_CREDENTIALS")
        print("     to test Google Translate service.")
        return
    
    try:
        service = create_translation_service(service_type='google', enable_cache=True)
        
        # Test real translation
        test_phrases = [
            ("Hello world", "es"),
            ("The heart pumps blood", "fr"),
            ("Rivers flow to the ocean", "de"),
            ("Knowledge is power", "ja")
        ]
        
        for text, target_lang in test_phrases:
            result = await service.translate(text, target_lang)
            print(f"\n{text} -> {target_lang}:")
            print(f"  Translation: {result.translated_text}")
            print(f"  Detected source: {result.source_language}")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")


async def test_huggingface_service():
    """Test Hugging Face translation service."""
    print("\n" + "="*60)
    print("Testing Hugging Face Translation Service")
    print("="*60)
    
    try:
        # Create service with CPU device for testing
        service = create_translation_service(
            service_type='huggingface',
            enable_cache=True,
            device='cpu'
        )
        
        print("  ℹ️  Note: First run will download models (~500MB each)")
        print("     Subsequent runs will use cached models.")
        
        # Test translations
        test_cases = [
            ("Hello world", "es", "en"),
            ("The sun is shining", "fr", "en"),
            ("I love programming", "de", "en")
        ]
        
        for text, target_lang, source_lang in test_cases:
            print(f"\nTranslating: '{text}' ({source_lang} -> {target_lang})")
            result = await service.translate(text, target_lang, source_lang)
            print(f"  Result: {result.translated_text}")
            print(f"  Model: {result.metadata.get('model', 'unknown')}")
        
        # Test language detection
        detect_tests = [
            "Hello world",
            "Bonjour le monde",
            "Hola mundo",
            "Hallo Welt"
        ]
        
        print("\nLanguage Detection:")
        for text in detect_tests:
            lang, conf = await service.detect_language(text)
            print(f"  '{text}' -> {lang} (confidence: {conf:.2f})")
            
    except ImportError:
        print("  ⚠️  Transformers not installed. Run: pip install transformers torch")
    except Exception as e:
        print(f"  ❌ Error: {e}")


async def test_cache_functionality():
    """Test translation caching."""
    print("\n" + "="*60)
    print("Testing Translation Cache")
    print("="*60)
    
    # Test SQLite cache
    from kimera.linguistics.translation_cache import TranslationCache
    
    cache = TranslationCache(backend="sqlite", ttl=3600)
    
    # Store some translations
    cache.set("Hello", "en", "es", "Hola", {"service": "test"})
    cache.set("World", "en", "es", "Mundo", {"service": "test"})
    
    # Retrieve translations
    result = cache.get("Hello", "en", "es")
    if result:
        print(f"\nCached translation found:")
        print(f"  {result['source_text']} -> {result['translated_text']}")
        print(f"  Cached at: {result['cached_at']}")
    
    # Check stats
    stats = cache.stats()
    print(f"\nCache statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Clean up
    cache.cleanup()


async def test_configuration():
    """Test configuration loading."""
    print("\n" + "="*60)
    print("Testing Configuration")
    print("="*60)
    
    config = get_config()
    
    print(f"\nDefault service: {config.get_default_service()}")
    print(f"Supported languages: {config.get_supported_languages()}")
    print(f"Available services: {config.get_available_services()}")
    
    # Validate configuration
    validation = config.validate()
    print(f"\nConfiguration valid: {validation['valid']}")
    if validation['errors']:
        print("Errors:")
        for error in validation['errors']:
            print(f"  - {error}")
    if validation['warnings']:
        print("Warnings:")
        for warning in validation['warnings']:
            print(f"  - {warning}")


async def main():
    """Run all tests."""
    print("Kimera Translation Services Test Suite")
    print("=====================================")
    
    # Test configuration first
    await test_configuration()
    
    # Test mock service (always available)
    await test_mock_service()
    
    # Test cache functionality
    await test_cache_functionality()
    
    # Test real services if available
    await test_google_service()
    await test_huggingface_service()
    
    print("\n" + "="*60)
    print("Testing complete!")
    print("="*60)
    
    print("\nNext steps:")
    print("1. Set up Google Cloud credentials for real translations")
    print("2. Install transformers for local translation: pip install transformers torch")
    print("3. Configure config/translation_config.yaml with your API keys")
    print("4. Integrate translation services into main Kimera pipeline")


if __name__ == "__main__":
    asyncio.run(main())