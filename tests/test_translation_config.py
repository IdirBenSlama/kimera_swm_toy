"""
Tests for translation configuration system
"""

import pytest
import json
import tempfile
from pathlib import Path
import os

from src.kimera.linguistics.translation_config import (
    TranslationConfig, TranslationServiceManager,
    get_global_config, set_global_config
)


class TestTranslationConfig:
    """Test TranslationConfig class"""
    
    def test_default_config(self):
        """Test default configuration values"""
        config = TranslationConfig()
        
        assert config.default_service == 'mock'
        assert config.fallback_service == 'mock'
        assert config.enable_cache is True
        assert config.cache_ttl == 86400
        assert config.batch_size == 50
        assert config.quality_threshold == 0.8
    
    def test_config_from_dict(self):
        """Test creating config from dictionary"""
        config = TranslationConfig(
            default_service='deepl',
            fallback_service='google',
            enable_cache=False,
            quality_threshold=0.9
        )
        
        assert config.default_service == 'deepl'
        assert config.fallback_service == 'google'
        assert config.enable_cache is False
        assert config.quality_threshold == 0.9
    
    def test_service_specific_config(self):
        """Test service-specific configurations"""
        config = TranslationConfig()
        
        # Google config
        assert 'credentials_path' in config.google_config
        assert 'project_id' in config.google_config
        
        # DeepL config
        assert 'api_key' in config.deepl_config
        assert config.deepl_config['api_type'] == 'free'
        
        # HuggingFace config
        assert 'model_name' in config.huggingface_config
        assert config.huggingface_config['device'] == 'cpu'
    
    def test_save_and_load_config(self):
        """Test saving and loading configuration from file"""
        config = TranslationConfig(
            default_service='deepl',
            fallback_service='google',
            batch_size=100,
            quality_threshold=0.85,
            preferred_variants={'en': 'en-GB', 'es': 'es-MX'}
        )
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            config_path = f.name
        
        try:
            config.to_file(config_path)
            
            # Load from file
            loaded_config = TranslationConfig.from_file(config_path)
            
            assert loaded_config.default_service == 'deepl'
            assert loaded_config.fallback_service == 'google'
            assert loaded_config.batch_size == 100
            assert loaded_config.quality_threshold == 0.85
            assert loaded_config.preferred_variants['en'] == 'en-GB'
            assert loaded_config.preferred_variants['es'] == 'es-MX'
            
        finally:
            Path(config_path).unlink(missing_ok=True)
    
    def test_load_from_nonexistent_file(self):
        """Test loading from non-existent file returns default config"""
        config = TranslationConfig.from_file('nonexistent.json')
        
        assert config.default_service == 'mock'  # Should use defaults
        assert config.enable_cache is True
    
    def test_from_env(self, monkeypatch):
        """Test loading configuration from environment variables"""
        # Set environment variables
        monkeypatch.setenv('KIMERA_TRANSLATION_SERVICE', 'google')
        monkeypatch.setenv('KIMERA_TRANSLATION_CACHE', 'false')
        monkeypatch.setenv('GOOGLE_APPLICATION_CREDENTIALS', '/path/to/creds.json')
        monkeypatch.setenv('DEEPL_API_KEY', 'test-api-key')
        monkeypatch.setenv('DEEPL_API_TYPE', 'pro')
        
        config = TranslationConfig.from_env()
        
        assert config.default_service == 'google'
        assert config.enable_cache is False
        assert config.google_config['credentials_path'] == '/path/to/creds.json'
        assert config.deepl_config['api_key'] == 'test-api-key'
        assert config.deepl_config['api_type'] == 'pro'
    
    def test_get_service_config(self):
        """Test getting service-specific configuration"""
        config = TranslationConfig()
        config.google_config['project_id'] = 'test-project'
        config.deepl_config['api_key'] = 'test-key'
        
        google_cfg = config.get_service_config('google')
        assert google_cfg['project_id'] == 'test-project'
        
        deepl_cfg = config.get_service_config('deepl')
        assert deepl_cfg['api_key'] == 'test-key'
        
        unknown_cfg = config.get_service_config('unknown')
        assert unknown_cfg == {}


class TestTranslationServiceManager:
    """Test TranslationServiceManager class"""
    
    @pytest.fixture
    def manager(self):
        """Create a manager with mock services"""
        config = TranslationConfig(
            default_service='mock',
            fallback_service='mock',
            enable_cache=False
        )
        return TranslationServiceManager(config)
    
    def test_manager_initialization(self, manager):
        """Test manager initializes with configured services"""
        assert manager.config is not None
        assert 'mock' in manager._services
        assert manager._primary_service is not None
    
    def test_list_services(self, manager):
        """Test listing available services"""
        services = manager.list_services()
        assert 'mock' in services
        assert isinstance(services, list)
    
    def test_get_service(self, manager):
        """Test getting specific service"""
        mock_service = manager.get_service('mock')
        assert mock_service is not None
        
        unknown_service = manager.get_service('unknown')
        assert unknown_service is None
    
    @pytest.mark.asyncio
    async def test_translate_with_manager(self, manager):
        """Test translation through manager"""
        result = await manager.translate("Hello", "es")
        
        assert result.source_text == "Hello"
        assert result.target_language == "es"
        assert result.translated_text  # Should have some translation
        assert result.confidence > 0
    
    @pytest.mark.asyncio
    async def test_translate_with_specific_service(self, manager):
        """Test translation with specific service selection"""
        result = await manager.translate(
            "Hello", 
            "es", 
            service='mock'
        )
        
        assert result.metadata.get('service') == 'mock'
    
    @pytest.mark.asyncio
    async def test_quality_threshold(self):
        """Test quality threshold handling"""
        # Create manager with high quality threshold
        config = TranslationConfig(
            default_service='mock',
            fallback_service='mock',
            quality_threshold=0.99  # Higher than mock's confidence
        )
        manager = TranslationServiceManager(config)
        
        # Should still return result even if below threshold
        result = await manager.translate("Hello", "es")
        assert result is not None
        assert result.translated_text
    
    @pytest.mark.asyncio
    async def test_get_usage_stats(self, manager):
        """Test getting usage statistics"""
        # Perform some translations
        await manager.translate("Hello", "es")
        await manager.translate("World", "fr")
        
        stats = await manager.get_usage_stats()
        
        assert isinstance(stats, dict)
        assert 'mock' in stats
        
        # If service has cache stats
        if 'total_requests' in stats['mock']:
            assert stats['mock']['total_requests'] >= 2


class TestGlobalConfig:
    """Test global configuration functions"""
    
    def test_get_global_config(self):
        """Test getting global configuration"""
        config = get_global_config()
        assert isinstance(config, TranslationConfig)
    
    def test_set_global_config(self):
        """Test setting global configuration"""
        custom_config = TranslationConfig(
            default_service='deepl',
            quality_threshold=0.95
        )
        
        set_global_config(custom_config)
        
        retrieved = get_global_config()
        assert retrieved.default_service == 'deepl'
        assert retrieved.quality_threshold == 0.95
        
        # Reset to default
        set_global_config(None)
    
    def test_global_config_from_env(self, monkeypatch):
        """Test global config loads from environment"""
        # Reset global config
        set_global_config(None)
        
        # Set environment variable
        monkeypatch.setenv('KIMERA_TRANSLATION_SERVICE', 'google')
        
        config = get_global_config()
        assert config.default_service == 'google'
    
    def test_global_config_from_file(self, monkeypatch):
        """Test global config loads from file"""
        # Reset global config
        set_global_config(None)
        
        # Create config file
        config = TranslationConfig(
            default_service='deepl',
            batch_size=200
        )
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            config_path = f.name
        
        try:
            config.to_file(config_path)
            
            # Set environment to point to config file
            monkeypatch.setenv('KIMERA_TRANSLATION_CONFIG', config_path)
            
            # Get global config (should load from file)
            loaded = get_global_config()
            assert loaded.default_service == 'deepl'
            assert loaded.batch_size == 200
            
        finally:
            Path(config_path).unlink(missing_ok=True)
            set_global_config(None)  # Reset


class TestConfigIntegration:
    """Test configuration integration with translation services"""
    
    @pytest.mark.asyncio
    async def test_manager_with_cache_config(self):
        """Test manager respects cache configuration"""
        config = TranslationConfig(
            default_service='mock',
            enable_cache=True,
            cache_ttl=3600
        )
        
        manager = TranslationServiceManager(config)
        
        # Translate same text twice
        text = "Caching test"
        result1 = await manager.translate(text, "es")
        result2 = await manager.translate(text, "es")
        
        # Should get same result (from cache)
        assert result1.translated_text == result2.translated_text
        
        # Check cache stats if available
        stats = await manager.get_usage_stats()
        if 'mock' in stats and 'hits' in stats['mock']:
            assert stats['mock']['hits'] > 0
    
    @pytest.mark.asyncio
    async def test_preferred_variants(self):
        """Test preferred language variants"""
        config = TranslationConfig(
            preferred_variants={
                'en': 'en-GB',
                'pt': 'pt-PT'
            }
        )
        
        # This would be used by services that support variants
        assert config.preferred_variants['en'] == 'en-GB'
        assert config.preferred_variants['pt'] == 'pt-PT'
    
    def test_advanced_options(self):
        """Test advanced configuration options"""
        config = TranslationConfig(
            batch_size=100,
            timeout=60,
            retry_count=5,
            retry_delay=2.0,
            use_alternatives=True,
            preserve_formatting=False
        )
        
        assert config.batch_size == 100
        assert config.timeout == 60
        assert config.retry_count == 5
        assert config.retry_delay == 2.0
        assert config.use_alternatives is True
        assert config.preserve_formatting is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])