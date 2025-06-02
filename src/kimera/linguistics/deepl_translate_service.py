"""
DeepL API integration for Kimera SWM

This module provides integration with DeepL translation API.
Requires: deepl library and API key.
"""

import os
import logging
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime
import asyncio

from .translation_service import TranslationService, TranslationResult

logger = logging.getLogger(__name__)

# Check if DeepL is available
try:
    import deepl
    DEEPL_AVAILABLE = True
except ImportError:
    DEEPL_AVAILABLE = False
    logger.warning("DeepL library not installed. Install with: pip install deepl")


class DeepLTranslateService(TranslationService):
    """
    DeepL API implementation
    
    DeepL is known for high-quality translations with better context understanding
    than many other services. Supports fewer languages but with higher quality.
    
    Requires:
    - DeepL API key (free or pro)
    - deepl Python library
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_type: str = 'free',  # 'free' or 'pro'
        **kwargs
    ):
        """
        Initialize DeepL service
        
        Args:
            api_key: DeepL API key (or set DEEPL_API_KEY env var)
            api_type: 'free' for free API, 'pro' for paid API
            **kwargs: Additional arguments for parent class
        """
        super().__init__(**kwargs)
        
        if not DEEPL_AVAILABLE:
            raise ImportError(
                "DeepL library not installed. "
                "Install with: pip install deepl"
            )
        
        # Get API key
        self._api_key = api_key or os.getenv('DEEPL_API_KEY')
        if not self._api_key:
            raise ValueError(
                "DeepL API key required. Set DEEPL_API_KEY environment variable "
                "or pass api_key parameter"
            )
        
        # Initialize translator
        self._translator = None
        self._api_type = api_type
        self._usage_cache = None
        self._supported_languages_cache = None
        
        # Language code mapping (DeepL uses specific codes)
        self._language_map = {
            'en': 'EN-US',  # DeepL prefers regional variants
            'pt': 'PT-PT',  # Portuguese (Portugal)
            'pt-br': 'PT-BR',  # Portuguese (Brazil)
            'zh': 'ZH',  # Chinese (simplified)
        }
        
        # Source language mapping (different for source)
        self._source_language_map = {
            'en': 'EN',  # No regional variant for source
            'pt': 'PT',
            'zh': 'ZH',
        }
        
        # Initialize client
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize DeepL translator client"""
        try:
            self._translator = deepl.Translator(self._api_key)
            
            # Test the connection and cache usage
            self._usage_cache = self._translator.get_usage()
            
            logger.info(f"DeepL translator initialized successfully ({self._api_type} API)")
            logger.info(f"Character usage: {self._usage_cache.character.count}/{self._usage_cache.character.limit}")
            
        except Exception as e:
            logger.error(f"Failed to initialize DeepL translator: {e}")
            raise
    
    def _map_language_code(self, code: str, for_source: bool = False) -> str:
        """Map between standard and DeepL language codes"""
        if not code:
            return None
            
        code = code.lower()
        
        if for_source:
            # Use source language mapping
            return self._source_language_map.get(code, code.upper())
        else:
            # Use target language mapping
            return self._language_map.get(code, code.upper())
    
    async def translate(
        self,
        text: str,
        target_language: str,
        source_language: Optional[str] = None
    ) -> TranslationResult:
        """
        Translate text using DeepL API
        
        Args:
            text: Text to translate
            target_language: Target language code
            source_language: Source language code (auto-detect if None)
            
        Returns:
            TranslationResult with translation details
        """
        if not text or not text.strip():
            return TranslationResult(
                source_text=text,
                translated_text="",
                source_language=source_language or "auto",
                target_language=target_language,
                confidence=1.0
            )
        
        try:
            # Map language codes
            target_lang = self._map_language_code(target_language)
            source_lang = self._map_language_code(source_language, for_source=True) if source_language else None
            
            # Perform translation
            # DeepL is synchronous, so we run it in executor
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self._translator.translate_text(
                    text,
                    target_lang=target_lang,
                    source_lang=source_lang
                )
            )
            
            # Extract results
            translated_text = result.text
            detected_language = result.detected_source_lang.lower() if result.detected_source_lang else (source_language or 'auto')
            
            # DeepL provides high confidence translations
            confidence = 0.98 if source_language else 0.95
            
            return TranslationResult(
                source_text=text,
                translated_text=translated_text,
                source_language=detected_language,
                target_language=target_language,
                confidence=confidence,
                metadata={
                    'service': 'deepl',
                    'timestamp': datetime.now().isoformat(),
                    'api_type': self._api_type,
                    'detected_language_raw': result.detected_source_lang,
                    'billed_characters': len(text)  # DeepL bills by character
                }
            )
            
        except deepl.DeepLException as e:
            logger.error(f"DeepL translation error: {e}")
            # Check if it's a quota error
            if "quota" in str(e).lower():
                logger.warning("DeepL quota exceeded")
                
            # Return mock translation as fallback
            return TranslationResult(
                source_text=text,
                translated_text=f"[{target_language}]{text}",
                source_language=source_language or "auto",
                target_language=target_language,
                confidence=0.0,
                metadata={
                    'service': 'deepl',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
            )
        except Exception as e:
            logger.error(f"Unexpected error in DeepL translation: {e}")
            return TranslationResult(
                source_text=text,
                translated_text=f"[{target_language}]{text}",
                source_language=source_language or "auto",
                target_language=target_language,
                confidence=0.0,
                metadata={
                    'service': 'deepl',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
            )
    
    async def detect_language(self, text: str) -> Tuple[str, float]:
        """
        Detect language of text
        
        Note: DeepL doesn't have a separate language detection endpoint,
        so we use a translation to detect the language
        """
        if not text or not text.strip():
            return ('unknown', 0.0)
        
        try:
            # Translate to English to detect source language
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self._translator.translate_text(
                    text,
                    target_lang='EN-US'
                )
            )
            
            if result.detected_source_lang:
                language = result.detected_source_lang.lower()
                # DeepL has high confidence in detection
                confidence = 0.95
                return (language, confidence)
            
            return ('unknown', 0.0)
            
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return ('unknown', 0.0)
    
    async def get_supported_languages(self) -> List[str]:
        """Get list of supported language codes"""
        try:
            if not self._supported_languages_cache:
                # Get target languages
                loop = asyncio.get_event_loop()
                target_languages = await loop.run_in_executor(
                    None,
                    self._translator.get_target_languages
                )
                
                # Convert to standard codes
                codes = []
                for lang in target_languages:
                    code = lang.code.lower()
                    # Handle regional variants
                    if '-' in code:
                        # Keep full code for variants like pt-br
                        codes.append(code)
                    else:
                        codes.append(code)
                
                self._supported_languages_cache = sorted(list(set(codes)))
            
            return self._supported_languages_cache
            
        except Exception as e:
            logger.error(f"Error fetching supported languages: {e}")
            # Return DeepL's typical supported languages
            return [
                'bg', 'cs', 'da', 'de', 'el', 'en', 'es', 'et', 'fi', 'fr',
                'hu', 'id', 'it', 'ja', 'ko', 'lt', 'lv', 'nb', 'nl', 'pl',
                'pt', 'pt-br', 'ro', 'ru', 'sk', 'sl', 'sv', 'tr', 'uk', 'zh'
            ]
    
    async def batch_translate(
        self,
        texts: List[str],
        target_language: str,
        source_language: Optional[str] = None
    ) -> List[TranslationResult]:
        """
        Translate multiple texts efficiently
        
        DeepL supports batch translation natively
        """
        if not texts:
            return []
        
        try:
            # Map language codes
            target_lang = self._map_language_code(target_language)
            source_lang = self._map_language_code(source_language, for_source=True) if source_language else None
            
            # Batch translate
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None,
                lambda: self._translator.translate_text(
                    texts,
                    target_lang=target_lang,
                    source_lang=source_lang
                )
            )
            
            # Convert to TranslationResult objects
            translation_results = []
            
            for i, result in enumerate(results):
                detected_lang = result.detected_source_lang.lower() if result.detected_source_lang else (source_language or 'auto')
                
                translation_results.append(TranslationResult(
                    source_text=texts[i],
                    translated_text=result.text,
                    source_language=detected_lang,
                    target_language=target_language,
                    confidence=0.98 if source_language else 0.95,
                    metadata={
                        'service': 'deepl',
                        'timestamp': datetime.now().isoformat(),
                        'api_type': self._api_type,
                        'batch_index': i,
                        'billed_characters': len(texts[i])
                    }
                ))
            
            return translation_results
            
        except Exception as e:
            logger.error(f"Batch translation error: {e}")
            # Fallback to sequential translation
            return await super().batch_translate(texts, target_language, source_language)
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics from DeepL API"""
        try:
            usage = self._translator.get_usage()
            
            return {
                'service': 'deepl',
                'api_type': self._api_type,
                'character_count': usage.character.count,
                'character_limit': usage.character.limit,
                'character_usage_percent': (usage.character.count / usage.character.limit * 100) if usage.character.limit else 0,
                'document_count': usage.document.count if hasattr(usage, 'document') else None,
                'document_limit': usage.document.limit if hasattr(usage, 'document') else None,
                'team_document_count': usage.team_document.count if hasattr(usage, 'team_document') else None,
                'team_document_limit': usage.team_document.limit if hasattr(usage, 'team_document') else None,
            }
            
        except Exception as e:
            logger.error(f"Error fetching usage stats: {e}")
            return {
                'service': 'deepl',
                'api_type': self._api_type,
                'error': str(e)
            }
    
    async def translate_with_alternatives(
        self,
        text: str,
        target_language: str,
        source_language: Optional[str] = None,
        num_alternatives: int = 3
    ) -> List[TranslationResult]:
        """
        Get multiple translation alternatives (DeepL feature)
        
        Note: This is a premium feature and may not be available on all plans
        """
        # For now, just return single translation
        # Full implementation would use DeepL's alternatives API
        result = await self.translate(text, target_language, source_language)
        return [result]
    
    async def translate_with_glossary(
        self,
        text: str,
        target_language: str,
        glossary_id: str,
        source_language: Optional[str] = None
    ) -> TranslationResult:
        """
        Translate using a glossary for consistent terminology
        
        Note: Glossaries are a DeepL Pro feature
        """
        # Simplified implementation - would use glossary in real version
        result = await self.translate(text, target_language, source_language)
        result.metadata['glossary_id'] = glossary_id
        return result