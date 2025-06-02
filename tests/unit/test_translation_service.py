"""
Unit tests for translation service
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
import tempfile
import shutil

from src.kimera.linguistics import (
    TranslationService,
    TranslationResult,
    MockTranslationService,
    CachedTranslationService,
    create_translation_service,
    TranslationCache
)


class TestMockTranslationService:
    """Test mock translation service"""
    
    @pytest.mark.asyncio
    async def test_basic_translation(self):
        """Test basic translation functionality"""
        service = MockTranslationService()
        
        result = await service.translate("hello", "es")
        assert result.source_text == "hello"
        assert result.translated_text == "hola"
        assert result.source_language == "en"
        assert result.target_language == "es"
        assert result.confidence > 0.9
    
    @pytest.mark.asyncio
    async def test_unknown_translation(self):
        """Test translation of unknown text"""
        service = MockTranslationService()
        
        result = await service.translate("unknown", "fr")
        assert result.source_text == "unknown"
        assert result.translated_text == "[fr]unknown"
        assert result.target_language == "fr"
    
    @pytest.mark.asyncio
    async def test_language_detection(self):
        """Test language detection"""
        service = MockTranslationService()
        
        # Test English detection
        lang, conf = await service.detect_language("hello world")
        assert lang == "en"
        assert conf > 0.7
        
        # Test non-ASCII detection
        lang, conf = await service.detect_language("你好")
        assert lang == "zh"
        assert conf > 0.8
    
    @pytest.mark.asyncio
    async def test_supported_languages(self):
        """Test getting supported languages"""
        service = MockTranslationService()
        
        languages = await service.get_supported_languages()
        assert isinstance(languages, list)
        assert "en" in languages
        assert "es" in languages
        assert len(languages) >= 10
    
    @pytest.mark.asyncio
    async def test_batch_translation(self):
        """Test batch translation"""
        service = MockTranslationService()
        
        texts = ["hello", "world", "love"]
        results = await service.batch_translate(texts, "es")
        
        assert len(results) == 3
        assert results[0].translated_text == "hola"
        assert results[1].translated_text == "mundo"
        assert results[2].translated_text == "amor"


class TestCachedTranslationService:
    """Test cached translation service"""
    
    @pytest.mark.asyncio
    async def test_cache_hit(self):
        """Test cache hit behavior"""
        base_service = MockTranslationService()
        cached_service = CachedTranslationService(base_service)
        
        # First call - cache miss
        result1 = await cached_service.translate("hello", "es")
        stats = cached_service.get_cache_stats()
        assert stats['misses'] == 1
        assert stats['hits'] == 0
        
        # Second call - cache hit
        result2 = await cached_service.translate("hello", "es")
        stats = cached_service.get_cache_stats()
        assert stats['misses'] == 1
        assert stats['hits'] == 1
        
        # Results should be identical
        assert result1.translated_text == result2.translated_text
    
    @pytest.mark.asyncio
    async def test_cache_expiration(self):
        """Test cache expiration"""
        base_service = MockTranslationService()
        # Very short TTL for testing
        cached_service = CachedTranslationService(base_service, cache_ttl=0.1)
        
        # First call
        await cached_service.translate("hello", "es")
        
        # Wait for expiration
        await asyncio.sleep(0.2)
        
        # Should be a cache miss now
        await cached_service.translate("hello", "es")
        stats = cached_service.get_cache_stats()
        assert stats['misses'] == 2
        assert stats['evictions'] == 1
    
    @pytest.mark.asyncio
    async def test_batch_caching(self):
        """Test batch translation with caching"""
        base_service = MockTranslationService()
        cached_service = CachedTranslationService(base_service)
        
        texts = ["hello", "world", "hello"]  # Duplicate "hello"
        
        # First batch - all misses
        results1 = await cached_service.batch_translate(texts, "es")
        stats = cached_service.get_cache_stats()
        assert stats['misses'] == 3
        assert stats['hits'] == 0
        
        # Second batch - should have hits
        results2 = await cached_service.batch_translate(texts, "es")
        stats = cached_service.get_cache_stats()
        assert stats['hits'] == 3  # All should hit cache
        
        # Results should match
        for r1, r2 in zip(results1, results2):
            assert r1.translated_text == r2.translated_text
    
    @pytest.mark.asyncio
    async def test_clear_cache(self):
        """Test cache clearing"""
        base_service = MockTranslationService()
        cached_service = CachedTranslationService(base_service)
        
        # Populate cache
        await cached_service.translate("hello", "es")
        await cached_service.translate("world", "fr")
        
        stats = cached_service.get_cache_stats()
        assert stats['cache_size'] == 2
        
        # Clear cache
        cached_service.clear_cache()
        
        stats = cached_service.get_cache_stats()
        assert stats['cache_size'] == 0


class TestTranslationCache:
    """Test advanced translation cache"""
    
    @pytest.fixture
    def temp_cache_dir(self):
        """Create temporary cache directory"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    @pytest.mark.asyncio
    async def test_persistent_cache(self, temp_cache_dir):
        """Test persistent cache storage"""
        cache = TranslationCache(
            cache_dir=temp_cache_dir,
            max_memory_items=10,
            enable_persistence=True
        )
        
        # Create test result
        result = TranslationResult(
            source_text="hello",
            translated_text="hola",
            source_language="en",
            target_language="es",
            confidence=0.95
        )
        
        # Store in cache
        await cache.put("test_key", result)
        
        # Retrieve from cache
        retrieved = await cache.get("test_key")
        assert retrieved is not None
        assert retrieved.translated_text == "hola"
        
        # Check stats
        stats = cache.get_stats()
        assert stats['memory_hits'] == 1
    
    @pytest.mark.asyncio
    async def test_lru_eviction(self, temp_cache_dir):
        """Test LRU eviction policy"""
        cache = TranslationCache(
            cache_dir=temp_cache_dir,
            max_memory_items=3,
            enable_persistence=False
        )
        
        # Fill cache beyond capacity
        for i in range(5):
            result = TranslationResult(
                source_text=f"text_{i}",
                translated_text=f"trans_{i}",
                source_language="en",
                target_language="es"
            )
            await cache.put(f"key_{i}", result)
        
        # First two should be evicted
        assert await cache.get("key_0") is None
        assert await cache.get("key_1") is None
        
        # Last three should be present
        assert await cache.get("key_2") is not None
        assert await cache.get("key_3") is not None
        assert await cache.get("key_4") is not None
    
    @pytest.mark.asyncio
    async def test_cache_export_import(self, temp_cache_dir):
        """Test cache export and import"""
        cache1 = TranslationCache(cache_dir=temp_cache_dir)
        
        # Populate cache
        for i in range(5):
            result = TranslationResult(
                source_text=f"text_{i}",
                translated_text=f"trans_{i}",
                source_language="en",
                target_language="es"
            )
            await cache1.put(f"key_{i}", result)
        
        # Export cache
        export_path = temp_cache_dir / "export.pkl"
        exported = await cache1.export_cache(export_path)
        assert exported == 5
        
        # Create new cache and import
        cache2 = TranslationCache(cache_dir=temp_cache_dir / "cache2")
        imported = await cache2.import_cache(export_path)
        assert imported == 5
        
        # Verify imported data
        result = await cache2.get("key_2")
        assert result is not None
        assert result.translated_text == "trans_2"
    
    @pytest.mark.asyncio
    async def test_cleanup_expired(self, temp_cache_dir):
        """Test cleanup of expired entries"""
        cache = TranslationCache(
            cache_dir=temp_cache_dir,
            ttl_seconds=1  # Very short TTL
        )
        
        # Add entries
        result = TranslationResult(
            source_text="test",
            translated_text="prueba",
            source_language="en",
            target_language="es"
        )
        await cache.put("test_key", result)
        
        # Wait for expiration
        await asyncio.sleep(1.5)
        
        # Cleanup
        cleaned = await cache.cleanup_expired()
        assert cleaned >= 1
        
        # Should not be retrievable
        assert await cache.get("test_key") is None


class TestTranslationServiceFactory:
    """Test translation service factory"""
    
    def test_create_mock_service(self):
        """Test creating mock service"""
        service = create_translation_service(service_type='mock', enable_cache=False)
        assert isinstance(service, MockTranslationService)
    
    def test_create_cached_service(self):
        """Test creating cached service"""
        service = create_translation_service(service_type='mock', enable_cache=True)
        assert isinstance(service, CachedTranslationService)
    
    def test_invalid_service_type(self):
        """Test invalid service type"""
        with pytest.raises(ValueError):
            create_translation_service(service_type='invalid')
    
    def test_not_implemented_services(self):
        """Test not yet implemented services"""
        with pytest.raises(NotImplementedError):
            create_translation_service(service_type='google')
        
        with pytest.raises(NotImplementedError):
            create_translation_service(service_type='huggingface')