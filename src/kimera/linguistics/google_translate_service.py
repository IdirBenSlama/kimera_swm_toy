"""
Google Translate API integration for Kimera SWM

This module provides integration with Google Cloud Translation API.
Requires: google-cloud-translate library and API credentials.
"""

import os
import logging
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime

from .translation_service import TranslationService, TranslationResult

logger = logging.getLogger(__name__)

# Check if Google Cloud Translation is available
try:
    from google.cloud import translate_v2 as translate
    from google.oauth2 import service_account
    GOOGLE_TRANSLATE_AVAILABLE = True
except ImportError:
    GOOGLE_TRANSLATE_AVAILABLE = False
    logger.warning("Google Cloud Translation library not installed. Install with: pip install google-cloud-translate")


class GoogleTranslateService(TranslationService):
    """
    Google Cloud Translation API implementation
    
    Requires:
    - Google Cloud project with Translation API enabled
    - Service account credentials (JSON key file)
    - Environment variable: GOOGLE_APPLICATION_CREDENTIALS or explicit credentials
    """
    
    def __init__(
        self,
        credentials_path: Optional[str] = None,
        project_id: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize Google Translate service
        
        Args:
            credentials_path: Path to service account JSON file
            project_id: Google Cloud project ID
            **kwargs: Additional arguments for parent class
        """
        super().__init__(**kwargs)
        
        if not GOOGLE_TRANSLATE_AVAILABLE:
            raise ImportError(
                "Google Cloud Translation library not installed. "
                "Install with: pip install google-cloud-translate"
            )
        
        # Initialize client
        self._client = None
        self._credentials_path = credentials_path or os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        self._project_id = project_id or os.getenv('GOOGLE_CLOUD_PROJECT')
        
        # Language code mapping (Google uses different codes for some languages)
        self._language_map = {
            'zh': 'zh-CN',  # Chinese simplified
            'zh-tw': 'zh-TW',  # Chinese traditional
            'he': 'iw',  # Hebrew (Google uses old code)
            'jv': 'jw',  # Javanese (Google uses old code)
        }
        
        # Reverse mapping
        self._reverse_language_map = {v: k for k, v in self._language_map.items()}
        
        # Initialize client
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Google Translate client"""
        try:
            if self._credentials_path:
                # Use explicit credentials
                credentials = service_account.Credentials.from_service_account_file(
                    self._credentials_path
                )
                self._client = translate.Client(credentials=credentials)
            else:
                # Use default credentials (from environment)
                self._client = translate.Client()
            
            logger.info("Google Translate client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Translate client: {e}")
            raise
    
    def _map_language_code(self, code: str, to_google: bool = True) -> str:
        """Map between standard and Google language codes"""
        if to_google:
            return self._language_map.get(code, code)
        else:
            return self._reverse_language_map.get(code, code)
    
    async def translate(
        self,
        text: str,
        target_language: str,
        source_language: Optional[str] = None
    ) -> TranslationResult:
        """
        Translate text using Google Translate API
        
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
            source_lang = self._map_language_code(source_language) if source_language else None
            
            # Perform translation
            result = self._client.translate(
                text,
                target_language=target_lang,
                source_language=source_lang
            )
            
            # Extract results
            translated_text = result['translatedText']
            detected_language = result.get('detectedSourceLanguage', source_language or 'auto')
            
            # Map detected language back to standard code
            detected_language = self._map_language_code(detected_language, to_google=False)
            
            # Google doesn't provide confidence scores, so we estimate based on detection
            confidence = 0.95 if source_language else 0.90
            
            return TranslationResult(
                source_text=text,
                translated_text=translated_text,
                source_language=detected_language,
                target_language=target_language,
                confidence=confidence,
                metadata={
                    'service': 'google',
                    'timestamp': datetime.now().isoformat(),
                    'model': result.get('model', 'nmt'),  # Neural Machine Translation
                    'detected_language_raw': result.get('detectedSourceLanguage')
                }
            )
            
        except Exception as e:
            logger.error(f"Google Translate error: {e}")
            # Return mock translation as fallback
            return TranslationResult(
                source_text=text,
                translated_text=f"[{target_language}]{text}",
                source_language=source_language or "auto",
                target_language=target_language,
                confidence=0.0,
                metadata={
                    'service': 'google',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
            )
    
    async def detect_language(self, text: str) -> Tuple[str, float]:
        """
        Detect language of text
        
        Args:
            text: Text to analyze
            
        Returns:
            Tuple of (language_code, confidence)
        """
        if not text or not text.strip():
            return ('unknown', 0.0)
        
        try:
            result = self._client.detect_language(text)
            
            # Google returns a list of detections
            if result and isinstance(result, list) and len(result) > 0:
                detection = result[0]
                language = self._map_language_code(
                    detection['language'], 
                    to_google=False
                )
                confidence = detection.get('confidence', 0.0)
                return (language, confidence)
            
            return ('unknown', 0.0)
            
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return ('unknown', 0.0)
    
    async def get_supported_languages(self) -> List[str]:
        """Get list of supported language codes"""
        try:
            # Get languages with English names
            languages = self._client.get_languages()
            
            # Extract language codes and map to standard codes
            codes = []
            for lang in languages:
                code = lang['language']
                standard_code = self._map_language_code(code, to_google=False)
                codes.append(standard_code)
            
            return sorted(codes)
            
        except Exception as e:
            logger.error(f"Error fetching supported languages: {e}")
            # Return common languages as fallback
            return [
                'en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh',
                'ar', 'hi', 'tr', 'pl', 'nl', 'sv', 'da', 'no', 'fi', 'cs'
            ]
    
    async def batch_translate(
        self,
        texts: List[str],
        target_language: str,
        source_language: Optional[str] = None
    ) -> List[TranslationResult]:
        """
        Translate multiple texts efficiently
        
        Google Translate supports batch requests natively
        """
        if not texts:
            return []
        
        try:
            # Map language codes
            target_lang = self._map_language_code(target_language)
            source_lang = self._map_language_code(source_language) if source_language else None
            
            # Batch translate
            results = self._client.translate(
                texts,
                target_language=target_lang,
                source_language=source_lang
            )
            
            # Convert to TranslationResult objects
            translation_results = []
            
            for i, result in enumerate(results):
                detected_lang = result.get('detectedSourceLanguage', source_language or 'auto')
                detected_lang = self._map_language_code(detected_lang, to_google=False)
                
                translation_results.append(TranslationResult(
                    source_text=texts[i],
                    translated_text=result['translatedText'],
                    source_language=detected_lang,
                    target_language=target_language,
                    confidence=0.95 if source_language else 0.90,
                    metadata={
                        'service': 'google',
                        'timestamp': datetime.now().isoformat(),
                        'model': result.get('model', 'nmt'),
                        'batch_index': i
                    }
                ))
            
            return translation_results
            
        except Exception as e:
            logger.error(f"Batch translation error: {e}")
            # Fallback to sequential translation
            return await super().batch_translate(texts, target_language, source_language)
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics (if available)
        
        Note: Google Cloud provides usage stats through Cloud Console,
        not directly through the API
        """
        return {
            'service': 'google',
            'client_initialized': self._client is not None,
            'project_id': self._project_id,
            'note': 'Usage statistics available in Google Cloud Console'
        }