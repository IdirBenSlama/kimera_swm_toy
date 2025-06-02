"""
Comprehensive tests for the translation service
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.kimera.linguistics.translation_service import (
    TranslationService, TranslationResult,
    MockTranslationService, CachedTranslationService,
    create_translation_service
)


class TestTranslationResult:
    """Test the TranslationResult dataclass"""
    
    def test_translation_result_creation(self):
        """Test creating a TranslationResult"""
        result = TranslationResult(
            source_text="Hello",
            translated_text="Hola",
            source_language="en",
            target_language="es",
            confidence=0.95
        )
        
        assert result.source_text == "Hello"
        assert result.translated_text == "Hola"
        assert result.source_language == "en"
        assert result.target_language == "es"
        assert result.confidence == 0.95
    
    def test_translation_result_defaults(self):
        """Test default values"""
        result = TranslationResult(
            source_text="Test",
            translated_text="Prueba",
            source_language="en",
            target_language="es"
        )
        
        assert result.source_language == "en"
        assert result.confidence == 1.0


class TestMockTranslationService:
    """Test the mock translation service"""
    
    @pytest.fixture
    def mock_service(self):
        return MockTranslationService()
    
    @pytest.mark.asyncio
    async def test_basic_translation(self, mock_service):
        """Test basic translation functionality"""
        result = await mock_service.translate("Hello", "es")
        
        assert result.source_text == "Hello"
        # Mock service has predefined translation for "hello" -> "hola"
        assert result.translated_text == "hola"
        assert result.target_language == "es"
        assert result.confidence == 0.95
    
    @pytest.mark.asyncio
    async def test_source_language_detection(self, mock_service):
        """Test source language parameter"""
        result = await mock_service.translate("Bonjour", "en", source_language="fr")
        
        assert result.source_language == "fr"
        assert result.translated_text == "[en]Bonjour"
    
    @pytest.mark.asyncio
    async def test_empty_text(self, mock_service):
        """Test handling of empty text"""
        result = await mock_service.translate("", "es")
        
        assert result.source_text == ""
        assert result.translated_text == "[es]"
        assert result.confidence == 0.95
    
    @pytest.mark.asyncio
    async def test_whitespace_text(self, mock_service):
        """Test handling of whitespace-only text"""
        result = await mock_service.translate("   \n\t  ", "fr")
        
        assert result.translated_text.strip() == "[fr]"
    
    @pytest.mark.asyncio
    async def test_special_characters(self, mock_service):
        """Test handling of special characters"""
        special_text = "Hello! @#$%^&*() 你好 🌍"
        result = await mock_service.translate(special_text, "es")
        
        assert result.source_text == special_text
        assert result.translated_text == f"[es]{special_text}"
    
    @pytest.mark.asyncio
    async def test_long_text(self, mock_service):
        """Test handling of long text"""
        long_text = "Lorem ipsum " * 100
        result = await mock_service.translate(long_text, "de")
        
        assert result.source_text == long_text
        assert result.translated_text.startswith("[de]")
    
    @pytest.mark.asyncio
    async def test_multiple_languages(self, mock_service):
        """Test translating to multiple languages"""
        text = "Hello world"
        languages = ["es", "fr", "de", "ja", "zh", "ar", "ru", "pt"]
        
        results = []
        for lang in languages:
            result = await mock_service.translate(text, lang)
            results.append(result)
        
        assert len(results) == len(languages)
        assert all(r.translated_text.startswith(f"[{r.target_language}]") for r in results)
    
    @pytest.mark.asyncio
    async def test_concurrent_translations(self, mock_service):
        """Test concurrent translation requests"""
        texts = [f"Text {i}" for i in range(10)]
        
        # Create concurrent tasks
        tasks = [mock_service.translate(text, "es") for text in texts]
        results = await asyncio.gather(*tasks)
        
        assert len(results) == len(texts)
        assert all(isinstance(r, TranslationResult) for r in results)


class TestCachedTranslationService:
    """Test the cached translation service wrapper"""
    
    @pytest.fixture
    def base_service(self):
        return MockTranslationService()
    
    @pytest.fixture
    def cached_service(self, base_service):
        return CachedTranslationService(base_service)
    
    @pytest.mark.asyncio
    async def test_cache_hit(self, cached_service):
        """Test that cache returns same result"""
        text = "Hello"
        target = "es"
        
        # First call - cache miss
        result1 = await cached_service.translate(text, target)
        
        # Second call - cache hit
        result2 = await cached_service.translate(text, target)
        
        assert result1.translated_text == result2.translated_text
        assert result1.confidence == result2.confidence
    
    @pytest.mark.asyncio
    async def test_cache_different_targets(self, cached_service):
        """Test cache with different target languages"""
        text = "Hello"
        
        result_es = await cached_service.translate(text, "es")
        result_fr = await cached_service.translate(text, "fr")
        
        assert result_es.translated_text != result_fr.translated_text
        assert result_es.target_language == "es"
        assert result_fr.target_language == "fr"
    
    @pytest.mark.asyncio
    async def test_cache_different_sources(self, cached_service):
        """Test cache with different source languages"""
        text = "Hello"
        
        result1 = await cached_service.translate(text, "es", source_language="en")
        result2 = await cached_service.translate(text, "es", source_language="fr")
        
        # Should be different cache entries
        assert result1.source_language == "en"
        assert result2.source_language == "fr"
    
    @pytest.mark.asyncio
    async def test_cache_case_sensitive(self, cached_service):
        """Test that cache is case-sensitive"""
        result1 = await cached_service.translate("Hello", "es")
        result2 = await cached_service.translate("hello", "es")
        
        # Different texts should have different cache entries
        assert result1.source_text != result2.source_text
    
    @pytest.mark.asyncio
    async def test_cache_whitespace_sensitive(self, cached_service):
        """Test cache with whitespace differences"""
        result1 = await cached_service.translate("Hello world", "es")
        result2 = await cached_service.translate("Hello  world", "es")  # Double space
        
        # Different whitespace should be different entries
        assert result1.source_text != result2.source_text
    
    def test_cache_statistics(self, cached_service):
        """Test cache statistics tracking"""
        stats = cached_service.get_cache_stats()
        
        assert stats['total_requests'] == 0
        assert stats['hits'] == 0
        assert stats['misses'] == 0
        assert stats['hit_rate'] == 0.0
    
    @pytest.mark.asyncio
    async def test_cache_stats_update(self, cached_service):
        """Test cache statistics update correctly"""
        # First request - miss
        await cached_service.translate("Hello", "es")
        stats1 = cached_service.get_cache_stats()
        assert stats1['misses'] == 1
        assert stats1['hits'] == 0
        
        # Second request - hit
        await cached_service.translate("Hello", "es")
        stats2 = cached_service.get_cache_stats()
        assert stats2['misses'] == 1
        assert stats2['hits'] == 1
        assert stats2['hit_rate'] == 0.5
    
    def test_clear_cache(self, cached_service):
        """Test clearing the cache"""
        # Add some entries
        asyncio.run(cached_service.translate("Hello", "es"))
        asyncio.run(cached_service.translate("World", "fr"))
        
        # Clear cache
        cached_service.clear_cache()
        
        # Check cache is cleared but stats remain
        stats = cached_service.get_cache_stats()
        assert stats['total_requests'] == 2
        assert len(cached_service._memory_cache) == 0


class TestTranslationServiceFactory:
    """Test the translation service factory"""
    
    def test_create_mock_service(self):
        """Test creating mock service"""
        service = create_translation_service('mock', enable_cache=False)
        assert isinstance(service, MockTranslationService)
    
    def test_create_cached_mock_service(self):
        """Test creating cached mock service"""
        service = create_translation_service('mock', enable_cache=True)
        assert isinstance(service, CachedTranslationService)
        assert isinstance(service.base_service, MockTranslationService)
    
    def test_invalid_backend(self):
        """Test invalid backend raises error"""
        with pytest.raises(ValueError, match="Unknown service type"):
            create_translation_service('invalid_backend')
    
    def test_google_backend_not_implemented(self):
        """Test Google backend not yet implemented"""
        with pytest.raises(NotImplementedError):
            create_translation_service('google')
    
    def test_huggingface_backend_not_implemented(self):
        """Test HuggingFace backend not yet implemented"""
        with pytest.raises(NotImplementedError):
            create_translation_service('huggingface')


class TestTranslationServiceEdgeCases:
    """Test edge cases and error handling"""
    
    @pytest.fixture
    def service(self):
        return MockTranslationService()
    
    @pytest.mark.asyncio
    async def test_none_text(self, service):
        """Test handling None text"""
        with pytest.raises(TypeError):
            await service.translate(None, "es")
    
    @pytest.mark.asyncio
    async def test_none_target_language(self, service):
        """Test handling None target language"""
        # Mock service handles None target language
        result = await service.translate("Hello", None)
        assert result.target_language is None
    
    @pytest.mark.asyncio
    async def test_invalid_language_code(self, service):
        """Test handling invalid language codes"""
        # Mock service accepts any language code
        result = await service.translate("Hello", "xyz")
        assert result.target_language == "xyz"
    
    @pytest.mark.asyncio
    async def test_unicode_text(self, service):
        """Test handling various Unicode text"""
        unicode_texts = [
            "Hello 世界",  # Mixed scripts
            "مرحبا بالعالم",  # Arabic
            "Здравствуй мир",  # Cyrillic
            "🌍🌎🌏",  # Emojis
            "Ñoño",  # Spanish special chars
            "Café",  # Accented characters
        ]
        
        for text in unicode_texts:
            result = await service.translate(text, "en")
            assert result.source_text == text
            assert result.translated_text == f"[en]{text}"
    
    @pytest.mark.asyncio
    async def test_multiline_text(self, service):
        """Test handling multiline text"""
        multiline = """Line 1
        Line 2
        Line 3"""
        
        result = await service.translate(multiline, "es")
        assert result.source_text == multiline
        assert "\n" in result.translated_text


class TestTranslationServiceIntegration:
    """Integration tests with other Kimera components"""
    
    @pytest.mark.asyncio
    async def test_with_geoid_creation(self):
        """Test translation service with geoid creation"""
        from src.kimera.geoid import init_geoid
        
        service = create_translation_service('mock')
        
        # Translate a concept
        result = await service.translate("consciousness", "es")
        
        # Create geoid from translation
        geoid = init_geoid(
            text=result.translated_text,
            lang=result.target_language,
            layers=["translation"]
        )
        
        assert geoid.lang_axis == "es"
        assert geoid.raw == result.translated_text
    
    @pytest.mark.asyncio
    async def test_batch_translation_pattern(self):
        """Test batch translation pattern"""
        service = create_translation_service('mock', enable_cache=True)
        
        # Simulate batch processing
        concepts = ["love", "peace", "harmony", "wisdom", "truth"]
        languages = ["es", "fr", "de", "ja"]
        
        results = {}
        for concept in concepts:
            results[concept] = {}
            for lang in languages:
                result = await service.translate(concept, lang)
                results[concept][lang] = result.translated_text
        
        # Verify all translations completed
        assert len(results) == len(concepts)
        assert all(len(results[c]) == len(languages) for c in concepts)
    
    @pytest.mark.asyncio
    async def test_translation_pipeline(self):
        """Test a complete translation pipeline"""
        service = create_translation_service('mock', enable_cache=True)
        
        # Input text
        text = "The mind is everything. What you think you become."
        
        # Translation pipeline
        pipeline_languages = ["es", "fr", "de", "ja", "zh"]
        translations = []
        
        for lang in pipeline_languages:
            result = await service.translate(text, lang)
            translations.append({
                'language': lang,
                'text': result.translated_text,
                'confidence': result.confidence
            })
        
        # Verify pipeline results
        assert len(translations) == len(pipeline_languages)
        assert all(t['confidence'] > 0 for t in translations)
        assert all(t['text'].startswith(f"[{t['language']}]") for t in translations)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])