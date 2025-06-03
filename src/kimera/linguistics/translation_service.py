"""
Translation Service Abstraction for Kimera SWM

This module provides a unified interface for translation services with support for:
- Multiple translation backends (Google Translate, Hugging Face, Mock)
- Caching for performance optimization
- Automatic language detection
- Batch translation support
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import hashlib
import json
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@dataclass
class TranslationResult:
    """Result of a translation operation"""
    source_text: str
    translated_text: str
    source_language: str
    target_language: str
    confidence: float = 1.0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class TranslationService(ABC):
    """Abstract base class for translation services"""
    
    def __init__(self, cache_ttl: int = 86400):  # 24 hours default
        self.cache_ttl = cache_ttl
        self._cache = {}
        
    @abstractmethod
    async def translate(
        self, 
        text: str, 
        target_language: str,
        source_language: Optional[str] = None
    ) -> TranslationResult:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_language: Target language code (e.g., 'es', 'fr', 'de')
            source_language: Source language code (auto-detect if None)
            
        Returns:
            TranslationResult object
        """
        pass
    
    @abstractmethod
    async def detect_language(self, text: str) -> Tuple[str, float]:
        """
        Detect the language of the given text
        
        Args:
            text: Text to analyze
            
        Returns:
            Tuple of (language_code, confidence_score)
        """
        pass
    
    @abstractmethod
    async def get_supported_languages(self) -> List[str]:
        """Get list of supported language codes"""
        pass
    
    async def batch_translate(
        self,
        texts: List[str],
        target_language: str,
        source_language: Optional[str] = None
    ) -> List[TranslationResult]:
        """
        Translate multiple texts in batch
        
        Default implementation translates sequentially.
        Subclasses can override for optimized batch processing.
        """
        results = []
        for text in texts:
            result = await self.translate(text, target_language, source_language)
            results.append(result)
        return results
    
    def _get_cache_key(
        self, 
        text: str, 
        target_language: str,
        source_language: Optional[str] = None
    ) -> str:
        """Generate cache key for translation"""
        key_parts = [text, target_language]
        if source_language:
            key_parts.append(source_language)
        key_string = "|".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()


class MockTranslationService(TranslationService):
    """Mock translation service for testing and development"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.supported_languages = [
            'en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'zh', 'ar'
        ]
        
        # Simple mock translations for demonstration
        self.mock_translations = {
            ('hello', 'es'): 'hola',
            ('hello', 'fr'): 'bonjour',
            ('hello', 'de'): 'hallo',
            ('hello', 'ja'): 'こんにちは',
            ('world', 'es'): 'mundo',
            ('world', 'fr'): 'monde',
            ('world', 'de'): 'welt',
            ('love', 'es'): 'amor',
            ('love', 'fr'): 'amour',
            ('love', 'de'): 'liebe',
        }
    
    async def translate(
        self, 
        text: str, 
        target_language: str,
        source_language: Optional[str] = None
    ) -> TranslationResult:
        """Mock translation - returns simple transformations"""
        
        # Auto-detect source language if not provided
        if not source_language:
            source_language, _ = await self.detect_language(text)
        
        # Check for predefined translations
        key = (text.lower(), target_language)
        if key in self.mock_translations:
            translated = self.mock_translations[key]
        else:
            # Simple mock: add language tag
            translated = f"[{target_language}]{text}"
        
        return TranslationResult(
            source_text=text,
            translated_text=translated,
            source_language=source_language,
            target_language=target_language,
            confidence=0.95,
            metadata={'service': 'mock', 'timestamp': datetime.now().isoformat()}
        )
    
    async def detect_language(self, text: str) -> Tuple[str, float]:
        """Mock language detection"""
        # Simple heuristic for testing
        if any(ord(c) > 127 for c in text):
            if any('\u4e00' <= c <= '\u9fff' for c in text):
                return ('zh', 0.9)
            elif any('\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff' for c in text):
                return ('ja', 0.9)
            elif any('\u0600' <= c <= '\u06ff' for c in text):
                return ('ar', 0.9)
            else:
                return ('unknown', 0.5)
        
        # Default to English for ASCII text
        return ('en', 0.8)
    
    async def get_supported_languages(self) -> List[str]:
        """Return list of supported languages"""
        return self.supported_languages.copy()


class CachedTranslationService(TranslationService):
    """
    Decorator that adds caching to any translation service
    """
    
    def __init__(self, base_service: TranslationService, cache_backend=None, **kwargs):
        super().__init__(**kwargs)
        self.base_service = base_service
        self.cache_backend = cache_backend  # For future Redis/external cache support
        self._memory_cache = {}
        self._cache_stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0
        }
    
    async def translate(
        self, 
        text: str, 
        target_language: str,
        source_language: Optional[str] = None
    ) -> TranslationResult:
        """Translate with caching"""
        
        # Generate cache key
        cache_key = self._get_cache_key(text, target_language, source_language)
        
        # Check cache
        cached_result = self._get_from_cache(cache_key)
        if cached_result:
            self._cache_stats['hits'] += 1
            logger.debug(f"Cache hit for key: {cache_key}")
            return cached_result
        
        # Cache miss - perform translation
        self._cache_stats['misses'] += 1
        result = await self.base_service.translate(text, target_language, source_language)
        
        # Store in cache
        self._store_in_cache(cache_key, result)
        
        return result
    
    async def detect_language(self, text: str) -> Tuple[str, float]:
        """Delegate to base service"""
        return await self.base_service.detect_language(text)
    
    async def get_supported_languages(self) -> List[str]:
        """Delegate to base service"""
        return await self.base_service.get_supported_languages()
    
    async def batch_translate(
        self,
        texts: List[str],
        target_language: str,
        source_language: Optional[str] = None
    ) -> List[TranslationResult]:
        """Batch translate with caching"""
        results = []
        uncached_texts = []
        uncached_indices = []
        
        # Check cache for each text
        for i, text in enumerate(texts):
            cache_key = self._get_cache_key(text, target_language, source_language)
            cached_result = self._get_from_cache(cache_key)
            
            if cached_result:
                self._cache_stats['hits'] += 1
                results.append(cached_result)
            else:
                self._cache_stats['misses'] += 1
                results.append(None)  # Placeholder
                uncached_texts.append(text)
                uncached_indices.append(i)
        
        # Translate uncached texts
        if uncached_texts:
            new_results = await self.base_service.batch_translate(
                uncached_texts, target_language, source_language
            )
            
            # Update results and cache
            for idx, result in zip(uncached_indices, new_results):
                results[idx] = result
                cache_key = self._get_cache_key(
                    result.source_text, target_language, source_language
                )
                self._store_in_cache(cache_key, result)
        
        return results
    
    def _get_from_cache(self, key: str) -> Optional[TranslationResult]:
        """Get item from cache if not expired"""
        if key in self._memory_cache:
            entry = self._memory_cache[key]
            if datetime.now() < entry['expires']:
                return entry['result']
            else:
                # Expired - remove from cache
                del self._memory_cache[key]
                self._cache_stats['evictions'] += 1
        return None
    
    def _store_in_cache(self, key: str, result: TranslationResult):
        """Store item in cache with expiration"""
        expires = datetime.now() + timedelta(seconds=self.cache_ttl)
        self._memory_cache[key] = {
            'result': result,
            'expires': expires
        }
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics"""
        total = self._cache_stats['hits'] + self._cache_stats['misses']
        hit_rate = self._cache_stats['hits'] / total if total > 0 else 0
        
        return {
            **self._cache_stats,
            'total_requests': total,
            'hit_rate': hit_rate,
            'cache_size': len(self._memory_cache)
        }
    
    def clear_cache(self):
        """Clear the cache"""
        self._memory_cache.clear()
        logger.info("Translation cache cleared")


# Factory function for creating translation services
def create_translation_service(
    service_type: str = 'mock',
    enable_cache: bool = True,
    **kwargs
) -> TranslationService:
    """
    Factory function to create translation service instances
    
    Args:
        service_type: Type of service ('mock', 'google', 'deepl', 'huggingface')
        enable_cache: Whether to wrap service with caching
        **kwargs: Additional arguments for service initialization
        
    Returns:
        TranslationService instance
    """
    
    # Create base service
    if service_type == 'mock':
        base_service = MockTranslationService(**kwargs)
    elif service_type == 'google':
        try:
            from .google_translate_service import GoogleTranslateService
            base_service = GoogleTranslateService(**kwargs)
        except ImportError as e:
            logger.error(f"Failed to import Google Translate service: {e}")
            raise NotImplementedError(
                "Google Translate service requires google-cloud-translate. "
                "Install with: pip install google-cloud-translate"
            )
    elif service_type == 'deepl':
        try:
            from .deepl_translate_service import DeepLTranslateService
            base_service = DeepLTranslateService(**kwargs)
        except ImportError as e:
            logger.error(f"Failed to import DeepL service: {e}")
            raise NotImplementedError(
                "DeepL service requires deepl library. "
                "Install with: pip install deepl"
            )
    elif service_type == 'huggingface':
        try:
            from .huggingface_translate_service import HuggingFaceTranslationService
            base_service = HuggingFaceTranslationService(**kwargs)
        except ImportError as e:
            logger.error(f"Failed to import Hugging Face service: {e}")
            raise NotImplementedError(
                "Hugging Face service requires transformers and torch. "
                "Install with: pip install transformers torch"
            )
    else:
        raise ValueError(f"Unknown service type: {service_type}")
    
    # Wrap with caching if requested
    if enable_cache:
        return CachedTranslationService(base_service, **kwargs)
    
    return base_service