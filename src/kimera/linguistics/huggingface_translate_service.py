"""
Hugging Face Translation Service Implementation
==============================================

Provides local translation using Hugging Face transformers models.
This serves as a fallback when API services are unavailable.
"""

import os
import logging
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime
import torch

from .translation_service import TranslationService, TranslationResult

logger = logging.getLogger(__name__)

# Check if transformers is available
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.warning("Transformers library not installed. Install with: pip install transformers torch")


class HuggingFaceTranslationService(TranslationService):
    """
    Hugging Face Transformers-based translation service.
    
    Uses local models for translation, providing a free alternative
    to cloud-based services.
    """
    
    # Model mapping for language pairs
    MODEL_MAP = {
        # Multi-language models
        "multi": "Helsinki-NLP/opus-mt-mul-en",  # Multiple languages to English
        
        # English to other languages
        ("en", "es"): "Helsinki-NLP/opus-mt-en-es",
        ("en", "fr"): "Helsinki-NLP/opus-mt-en-fr",
        ("en", "de"): "Helsinki-NLP/opus-mt-en-de",
        ("en", "it"): "Helsinki-NLP/opus-mt-en-it",
        ("en", "pt"): "Helsinki-NLP/opus-mt-en-pt",
        ("en", "ru"): "Helsinki-NLP/opus-mt-en-ru",
        ("en", "zh"): "Helsinki-NLP/opus-mt-en-zh",
        ("en", "ja"): "Helsinki-NLP/opus-mt-en-ja",
        ("en", "ar"): "Helsinki-NLP/opus-mt-en-ar",
        ("en", "hi"): "Helsinki-NLP/opus-mt-en-hi",
        
        # Other languages to English
        ("es", "en"): "Helsinki-NLP/opus-mt-es-en",
        ("fr", "en"): "Helsinki-NLP/opus-mt-fr-en",
        ("de", "en"): "Helsinki-NLP/opus-mt-de-en",
        ("it", "en"): "Helsinki-NLP/opus-mt-it-en",
        ("pt", "en"): "Helsinki-NLP/opus-mt-pt-en",
        ("ru", "en"): "Helsinki-NLP/opus-mt-ru-en",
        ("zh", "en"): "Helsinki-NLP/opus-mt-zh-en",
        ("ja", "en"): "Helsinki-NLP/opus-mt-ja-en",
        ("ar", "en"): "Helsinki-NLP/opus-mt-ar-en",
        ("hi", "en"): "Helsinki-NLP/opus-mt-hi-en",
        
        # Romance language pairs
        ("es", "fr"): "Helsinki-NLP/opus-mt-es-fr",
        ("fr", "es"): "Helsinki-NLP/opus-mt-fr-es",
        ("es", "it"): "Helsinki-NLP/opus-mt-es-it",
        ("it", "es"): "Helsinki-NLP/opus-mt-it-es",
        ("es", "pt"): "Helsinki-NLP/opus-mt-es-pt",
        ("pt", "es"): "Helsinki-NLP/opus-mt-pt-es",
    }
    
    def __init__(
        self,
        model_name: Optional[str] = None,
        device: Optional[str] = None,
        cache_dir: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize Hugging Face translation service.
        
        Args:
            model_name: Specific model to use (overrides auto-selection)
            device: Device to use ('cpu', 'cuda', 'mps', or auto-detect)
            cache_dir: Directory to cache downloaded models
            **kwargs: Additional arguments for parent class
        """
        super().__init__(**kwargs)
        
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError(
                "Transformers library not installed. "
                "Install with: pip install transformers torch"
            )
        
        self.model_name = model_name
        self.cache_dir = cache_dir or os.path.expanduser("~/.cache/huggingface")
        
        # Auto-detect device if not specified
        if device is None:
            if torch.cuda.is_available():
                self.device = "cuda"
            elif torch.backends.mps.is_available():
                self.device = "mps"
            else:
                self.device = "cpu"
        else:
            self.device = device
        
        # Cache for loaded pipelines
        self._pipelines = {}
        
        # Language detection model
        self._lang_detector = None
        
        logger.info(f"Initialized Hugging Face translation service on {self.device}")
    
    def _get_model_for_pair(self, source_lang: str, target_lang: str) -> str:
        """Get the best model for a language pair."""
        # Check if specific model was provided
        if self.model_name:
            return self.model_name
        
        # Look for exact match
        if (source_lang, target_lang) in self.MODEL_MAP:
            return self.MODEL_MAP[(source_lang, target_lang)]
        
        # Try multi-language model for translations to English
        if target_lang == "en":
            return self.MODEL_MAP["multi"]
        
        # Default fallback
        return "Helsinki-NLP/opus-mt-en-mul"  # English to multiple languages
    
    def _get_pipeline(self, model_name: str):
        """Get or create translation pipeline."""
        if model_name not in self._pipelines:
            logger.info(f"Loading model: {model_name}")
            
            try:
                # Create pipeline with specific device
                self._pipelines[model_name] = pipeline(
                    "translation",
                    model=model_name,
                    device=0 if self.device == "cuda" else -1,
                    model_kwargs={"cache_dir": self.cache_dir}
                )
            except Exception as e:
                logger.error(f"Failed to load model {model_name}: {e}")
                raise
        
        return self._pipelines[model_name]
    
    async def translate(
        self,
        text: str,
        target_language: str,
        source_language: Optional[str] = None
    ) -> TranslationResult:
        """
        Translate text using Hugging Face models.
        
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
            # Auto-detect source language if not provided
            if not source_language:
                source_language, confidence = await self.detect_language(text)
                if source_language == "unknown":
                    source_language = "en"  # Default fallback
            
            # Get appropriate model
            model_name = self._get_model_for_pair(source_language, target_language)
            translator = self._get_pipeline(model_name)
            
            # Perform translation
            result = translator(text, max_length=512)
            
            if result and len(result) > 0:
                translated_text = result[0]['translation_text']
                
                return TranslationResult(
                    source_text=text,
                    translated_text=translated_text,
                    source_language=source_language,
                    target_language=target_language,
                    confidence=0.85,  # Hugging Face models don't provide confidence
                    metadata={
                        'service': 'huggingface',
                        'model': model_name,
                        'device': self.device,
                        'timestamp': datetime.now().isoformat()
                    }
                )
            else:
                raise ValueError("No translation result returned")
            
        except Exception as e:
            logger.error(f"Hugging Face translation error: {e}")
            # Return mock translation as fallback
            return TranslationResult(
                source_text=text,
                translated_text=f"[{target_language}]{text}",
                source_language=source_language or "auto",
                target_language=target_language,
                confidence=0.0,
                metadata={
                    'service': 'huggingface',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
            )
    
    async def detect_language(self, text: str) -> Tuple[str, float]:
        """
        Detect language of text.
        
        Uses a language identification model.
        """
        if not text or not text.strip():
            return ('unknown', 0.0)
        
        try:
            # Load language detection model if not already loaded
            if self._lang_detector is None:
                self._lang_detector = pipeline(
                    "text-classification",
                    model="papluca/xlm-roberta-base-language-detection",
                    device=0 if self.device == "cuda" else -1,
                    model_kwargs={"cache_dir": self.cache_dir}
                )
            
            # Detect language
            results = self._lang_detector(text)
            
            if results and len(results) > 0:
                # Get top result
                top_result = results[0]
                lang_code = top_result['label']
                confidence = top_result['score']
                
                # Map language codes if needed
                lang_map = {
                    'zh-CN': 'zh',
                    'zh-TW': 'zh',
                    'pt-BR': 'pt',
                    'pt-PT': 'pt'
                }
                
                lang_code = lang_map.get(lang_code, lang_code)
                
                return (lang_code, confidence)
            
            return ('unknown', 0.0)
            
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            # Simple heuristic fallback
            if any(ord(c) > 127 for c in text):
                if any('\u4e00' <= c <= '\u9fff' for c in text):
                    return ('zh', 0.5)
                elif any('\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff' for c in text):
                    return ('ja', 0.5)
                elif any('\u0600' <= c <= '\u06ff' for c in text):
                    return ('ar', 0.5)
                else:
                    return ('unknown', 0.3)
            
            return ('en', 0.6)
    
    async def get_supported_languages(self) -> List[str]:
        """Get list of supported language codes."""
        # Extract unique language codes from model map
        languages = set(['en'])  # English is always supported
        
        for key in self.MODEL_MAP:
            if isinstance(key, tuple):
                languages.add(key[0])
                languages.add(key[1])
        
        return sorted(list(languages))
    
    async def batch_translate(
        self,
        texts: List[str],
        target_language: str,
        source_language: Optional[str] = None
    ) -> List[TranslationResult]:
        """
        Translate multiple texts efficiently.
        
        Hugging Face models support batch processing natively.
        """
        if not texts:
            return []
        
        try:
            # Auto-detect source language from first text if not provided
            if not source_language:
                source_language, _ = await self.detect_language(texts[0])
                if source_language == "unknown":
                    source_language = "en"
            
            # Get appropriate model
            model_name = self._get_model_for_pair(source_language, target_language)
            translator = self._get_pipeline(model_name)
            
            # Batch translate
            results = translator(texts, max_length=512)
            
            # Convert to TranslationResult objects
            translation_results = []
            
            for i, (text, result) in enumerate(zip(texts, results)):
                if result and 'translation_text' in result:
                    translated_text = result['translation_text']
                else:
                    translated_text = f"[{target_language}]{text}"
                
                translation_results.append(TranslationResult(
                    source_text=text,
                    translated_text=translated_text,
                    source_language=source_language,
                    target_language=target_language,
                    confidence=0.85,
                    metadata={
                        'service': 'huggingface',
                        'model': model_name,
                        'device': self.device,
                        'batch_index': i,
                        'timestamp': datetime.now().isoformat()
                    }
                ))
            
            return translation_results
            
        except Exception as e:
            logger.error(f"Batch translation error: {e}")
            # Fallback to sequential translation
            return await super().batch_translate(texts, target_language, source_language)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded models."""
        return {
            'service': 'huggingface',
            'device': self.device,
            'cache_dir': self.cache_dir,
            'loaded_models': list(self._pipelines.keys()),
            'available_pairs': len(self.MODEL_MAP),
            'memory_usage': self._estimate_memory_usage()
        }
    
    def _estimate_memory_usage(self) -> str:
        """Estimate memory usage of loaded models."""
        if not self._pipelines:
            return "0 MB"
        
        # Rough estimate: ~500MB per model
        mb_used = len(self._pipelines) * 500
        
        if mb_used < 1024:
            return f"{mb_used} MB"
        else:
            return f"{mb_used / 1024:.1f} GB"
    
    def clear_models(self):
        """Clear loaded models from memory."""
        self._pipelines.clear()
        self._lang_detector = None
        
        # Force garbage collection
        import gc
        gc.collect()
        
        if self.device == "cuda":
            torch.cuda.empty_cache()
        
        logger.info("Cleared all loaded models from memory")