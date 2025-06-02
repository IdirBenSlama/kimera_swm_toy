"""
Translation Service Configuration

This module provides configuration management for translation services,
including API keys, service selection, and advanced options.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class TranslationConfig:
    """Configuration for translation services"""
    
    # Service selection
    default_service: str = 'mock'
    fallback_service: str = 'mock'
    enable_cache: bool = True
    cache_ttl: int = 86400  # 24 hours
    
    # Service-specific configurations
    google_config: Dict[str, Any] = field(default_factory=lambda: {
        'credentials_path': None,
        'project_id': None,
    })
    
    deepl_config: Dict[str, Any] = field(default_factory=lambda: {
        'api_key': None,
        'api_type': 'free',  # 'free' or 'pro'
    })
    
    huggingface_config: Dict[str, Any] = field(default_factory=lambda: {
        'model_name': 'Helsinki-NLP/opus-mt-en-es',
        'device': 'cpu',  # 'cpu' or 'cuda'
        'cache_dir': None,
    })
    
    # Advanced options
    batch_size: int = 50  # Maximum texts per batch
    timeout: int = 30  # Request timeout in seconds
    retry_count: int = 3  # Number of retries on failure
    retry_delay: float = 1.0  # Delay between retries
    
    # Language preferences
    preferred_variants: Dict[str, str] = field(default_factory=lambda: {
        'en': 'en-US',  # Prefer US English
        'pt': 'pt-BR',  # Prefer Brazilian Portuguese
        'zh': 'zh-CN',  # Prefer Simplified Chinese
    })
    
    # Quality settings
    quality_threshold: float = 0.8  # Minimum confidence threshold
    use_alternatives: bool = False  # Request alternative translations
    preserve_formatting: bool = True  # Preserve text formatting
    
    @classmethod
    def from_file(cls, config_path: str) -> 'TranslationConfig':
        """Load configuration from JSON file"""
        path = Path(config_path)
        if not path.exists():
            logger.warning(f"Config file not found: {config_path}")
            return cls()
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return cls(**data)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return cls()
    
    @classmethod
    def from_env(cls) -> 'TranslationConfig':
        """Load configuration from environment variables"""
        config = cls()
        
        # Service selection
        config.default_service = os.getenv('KIMERA_TRANSLATION_SERVICE', 'mock')
        config.enable_cache = os.getenv('KIMERA_TRANSLATION_CACHE', 'true').lower() == 'true'
        
        # Google configuration
        config.google_config['credentials_path'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        config.google_config['project_id'] = os.getenv('GOOGLE_CLOUD_PROJECT')
        
        # DeepL configuration
        config.deepl_config['api_key'] = os.getenv('DEEPL_API_KEY')
        config.deepl_config['api_type'] = os.getenv('DEEPL_API_TYPE', 'free')
        
        # HuggingFace configuration
        config.huggingface_config['model_name'] = os.getenv(
            'HUGGINGFACE_MODEL', 
            'Helsinki-NLP/opus-mt-en-es'
        )
        config.huggingface_config['device'] = os.getenv('HUGGINGFACE_DEVICE', 'cpu')
        
        return config
    
    def to_file(self, config_path: str):
        """Save configuration to JSON file"""
        path = Path(config_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to dict
        data = {
            'default_service': self.default_service,
            'fallback_service': self.fallback_service,
            'enable_cache': self.enable_cache,
            'cache_ttl': self.cache_ttl,
            'google_config': self.google_config,
            'deepl_config': self.deepl_config,
            'huggingface_config': self.huggingface_config,
            'batch_size': self.batch_size,
            'timeout': self.timeout,
            'retry_count': self.retry_count,
            'retry_delay': self.retry_delay,
            'preferred_variants': self.preferred_variants,
            'quality_threshold': self.quality_threshold,
            'use_alternatives': self.use_alternatives,
            'preserve_formatting': self.preserve_formatting,
        }
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def get_service_config(self, service_type: str) -> Dict[str, Any]:
        """Get configuration for specific service"""
        if service_type == 'google':
            return self.google_config
        elif service_type == 'deepl':
            return self.deepl_config
        elif service_type == 'huggingface':
            return self.huggingface_config
        else:
            return {}


class TranslationServiceManager:
    """
    Manages translation services with fallback and quality control
    """
    
    def __init__(self, config: Optional[TranslationConfig] = None):
        """
        Initialize service manager
        
        Args:
            config: Translation configuration (uses defaults if None)
        """
        self.config = config or TranslationConfig.from_env()
        self._services = {}
        self._primary_service = None
        self._fallback_service = None
        
        # Initialize services
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize configured translation services"""
        # Import here to avoid circular imports
        from .translation_service import create_translation_service
        
        # Initialize primary service
        try:
            service_config = self.config.get_service_config(self.config.default_service)
            self._primary_service = create_translation_service(
                self.config.default_service,
                enable_cache=self.config.enable_cache,
                cache_ttl=self.config.cache_ttl,
                **service_config
            )
            self._services[self.config.default_service] = self._primary_service
            logger.info(f"Initialized primary service: {self.config.default_service}")
        except Exception as e:
            logger.error(f"Failed to initialize primary service: {e}")
        
        # Initialize fallback service if different
        if self.config.fallback_service != self.config.default_service:
            try:
                fallback_config = self.config.get_service_config(self.config.fallback_service)
                self._fallback_service = create_translation_service(
                    self.config.fallback_service,
                    enable_cache=self.config.enable_cache,
                    cache_ttl=self.config.cache_ttl,
                    **fallback_config
                )
                self._services[self.config.fallback_service] = self._fallback_service
                logger.info(f"Initialized fallback service: {self.config.fallback_service}")
            except Exception as e:
                logger.error(f"Failed to initialize fallback service: {e}")
        
        # Always have mock as ultimate fallback
        if 'mock' not in self._services:
            self._services['mock'] = create_translation_service(
                'mock',
                enable_cache=self.config.enable_cache
            )
    
    async def translate(
        self,
        text: str,
        target_language: str,
        source_language: Optional[str] = None,
        service: Optional[str] = None
    ):
        """
        Translate text with automatic fallback
        
        Args:
            text: Text to translate
            target_language: Target language code
            source_language: Source language code (auto-detect if None)
            service: Specific service to use (uses default if None)
        """
        # Select service
        if service and service in self._services:
            selected_service = self._services[service]
        else:
            selected_service = self._primary_service or self._services.get('mock')
        
        # Try primary service
        try:
            result = await selected_service.translate(text, target_language, source_language)
            
            # Check quality threshold
            if result.confidence >= self.config.quality_threshold:
                return result
            else:
                logger.warning(
                    f"Translation confidence {result.confidence} below threshold "
                    f"{self.config.quality_threshold}"
                )
        except Exception as e:
            logger.error(f"Primary translation failed: {e}")
        
        # Try fallback service
        if self._fallback_service and self._fallback_service != selected_service:
            try:
                logger.info("Using fallback translation service")
                result = await self._fallback_service.translate(
                    text, target_language, source_language
                )
                return result
            except Exception as e:
                logger.error(f"Fallback translation failed: {e}")
        
        # Ultimate fallback to mock
        if 'mock' in self._services:
            logger.warning("Using mock translation as last resort")
            return await self._services['mock'].translate(
                text, target_language, source_language
            )
        
        # If all else fails, return error result
        from .translation_service import TranslationResult
        return TranslationResult(
            source_text=text,
            translated_text=f"[{target_language}]{text}",
            source_language=source_language or "auto",
            target_language=target_language,
            confidence=0.0,
            metadata={'error': 'All translation services failed'}
        )
    
    def get_service(self, service_type: str):
        """Get specific translation service"""
        return self._services.get(service_type)
    
    def list_services(self) -> list:
        """List available translation services"""
        return list(self._services.keys())
    
    async def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics from all services"""
        stats = {}
        
        for name, service in self._services.items():
            if hasattr(service, 'get_usage_stats'):
                try:
                    stats[name] = service.get_usage_stats()
                except Exception as e:
                    stats[name] = {'error': str(e)}
            else:
                # Check if it's a cached service
                if hasattr(service, 'get_cache_stats'):
                    stats[name] = service.get_cache_stats()
        
        return stats


# Global configuration instance
_global_config = None


def get_global_config() -> TranslationConfig:
    """Get global translation configuration"""
    global _global_config
    if _global_config is None:
        # Try to load from file first
        config_path = os.getenv('KIMERA_TRANSLATION_CONFIG')
        if config_path and os.path.exists(config_path):
            _global_config = TranslationConfig.from_file(config_path)
        else:
            # Fall back to environment variables
            _global_config = TranslationConfig.from_env()
    
    return _global_config


def set_global_config(config: TranslationConfig):
    """Set global translation configuration"""
    global _global_config
    _global_config = config