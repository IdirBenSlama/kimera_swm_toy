"""Tests for embedding and resonance cache functionality."""

import time
import shutil
import os
import numpy as np
import tempfile
from pathlib import Path

import pytest

from kimera.cache import embed_cache, resonance_cache, get_cache_stats, clear_embedding_cache
from kimera.geoid import sem_encoder, sym_encoder


class TestEmbeddingCache:
    """Test embedding cache functionality."""
    
    def test_cache_roundtrip(self, tmp_path):
        """Test that cache stores and retrieves embeddings correctly."""
        # Set temporary cache directory
        os.environ["KIMERA_CACHE_DIR"] = str(tmp_path)
        
        # Clear any existing cache
        clear_embedding_cache()
        
        # First call should miss cache and encode
        text = "Hello cache test"
        lang = "en"
        
        t0 = time.perf_counter()
        v1 = sem_encoder(text, lang)
        t1 = time.perf_counter() - t0
        
        # Second call should hit cache and be much faster
        t0 = time.perf_counter()
        v2 = sem_encoder(text, lang)
        t2 = time.perf_counter() - t0
        
        # Verify vectors are identical
        assert np.allclose(v1, v2), "Cached vector should match original"
        
        # Second call should be faster (cache hit)
        speedup = t1 / t2 if t2 > 0 else float('inf')
        assert speedup >= 1.5, f"Expected ≥1.5× speedup, got {speedup:.2f}×"
        
        # Verify cache stats
        stats = get_cache_stats()
        assert stats["embedding_cache_size"] >= 1, "Cache should contain at least one embedding"
    
    def test_cache_persistence(self, tmp_path):
        """Test that cache persists across sessions."""
        # Set temporary cache directory
        os.environ["KIMERA_CACHE_DIR"] = str(tmp_path)
        
        # Clear any existing cache
        clear_embedding_cache()
        
        text = "Persistence test"
        lang = "en"
        
        # First encoding
        v1 = sem_encoder(text, lang)
        
        # Simulate new session by creating new cache instance
        from kimera.cache import EmbeddingCache
        new_cache = EmbeddingCache()
        
        # Should find the cached embedding
        cached_vec = new_cache.get(lang, text)
        assert cached_vec is not None, "Cache should persist across sessions"
        assert np.allclose(v1, cached_vec), "Persisted vector should match original"
    
    def test_cache_different_languages(self, tmp_path):
        """Test that cache handles different languages correctly."""
        os.environ["KIMERA_CACHE_DIR"] = str(tmp_path)
        clear_embedding_cache()
        
        text = "Hello world"
        
        # Encode same text in different languages
        v_en = sem_encoder(text, "en")
        v_fr = sem_encoder(text, "fr")
        
        # Verify both are cached with different keys
        assert embed_cache.get("en", text) is not None, "English should be cached"
        assert embed_cache.get("fr", text) is not None, "French should be cached"
        
        # Verify cache keying works correctly (same language returns same object)
        v_en_cached = embed_cache.get("en", text)
        assert np.allclose(v_en, v_en_cached), "Cached English vector should match"
        
        # Verify both language variants are cached
        stats = get_cache_stats()
        assert stats["embedding_cache_size"] >= 2, "Should cache both language variants"
    
    def test_cache_stats(self, tmp_path):
        """Test cache statistics functionality."""
        os.environ["KIMERA_CACHE_DIR"] = str(tmp_path)
        clear_embedding_cache()
        
        # Initial stats
        stats = get_cache_stats()
        assert stats["embedding_cache_size"] == 0
        assert not stats["cache_file_exists"]
        
        # Add some embeddings
        sem_encoder("test1", "en")
        sem_encoder("test2", "en")
        
        # Check updated stats
        stats = get_cache_stats()
        assert stats["embedding_cache_size"] == 2
        assert stats["cache_file_exists"]
        assert stats["cache_file_size_mb"] > 0


class TestResonanceCache:
    """Test resonance cache functionality."""
    
    def test_resonance_cache_basic(self):
        """Test basic resonance cache operations."""
        resonance_cache.clear()
        
        gid1 = "test-gid-1"
        gid2 = "test-gid-2"
        value = 0.75
        
        # Initially empty
        assert resonance_cache.get(gid1, gid2) is None
        
        # Store value
        resonance_cache.set(gid1, gid2, value)
        
        # Retrieve value
        cached_value = resonance_cache.get(gid1, gid2)
        assert cached_value == value
        
        # Order shouldn't matter
        cached_value2 = resonance_cache.get(gid2, gid1)
        assert cached_value2 == value
    
    def test_resonance_cache_clear(self):
        """Test clearing resonance cache."""
        resonance_cache.clear()
        
        # Add some values
        resonance_cache.set("gid1", "gid2", 0.5)
        resonance_cache.set("gid3", "gid4", 0.8)
        
        # Verify they exist
        assert resonance_cache.get("gid1", "gid2") == 0.5
        assert resonance_cache.get("gid3", "gid4") == 0.8
        
        # Clear cache
        resonance_cache.clear()
        
        # Verify they're gone
        assert resonance_cache.get("gid1", "gid2") is None
        assert resonance_cache.get("gid3", "gid4") is None


class TestCacheIntegration:
    """Test cache integration with geoid operations."""
    
    def test_geoid_encoding_uses_cache(self, tmp_path):
        """Test that geoid encoding uses the cache."""
        os.environ["KIMERA_CACHE_DIR"] = str(tmp_path)
        clear_embedding_cache()
        
        from kimera.geoid import init_geoid
        
        text = "Integration test text"
        lang = "en"
        
        # Create first geoid
        t0 = time.perf_counter()
        geoid1 = init_geoid(text, lang, ["test"])
        t1 = time.perf_counter() - t0
        
        # Create second geoid with same text
        t0 = time.perf_counter()
        geoid2 = init_geoid(text, lang, ["test"])
        t2 = time.perf_counter() - t0
        
        # Vectors should be identical
        assert np.allclose(geoid1.sem_vec, geoid2.sem_vec)
        assert np.allclose(geoid1.sym_vec, geoid2.sym_vec)
        
        # Second creation should be faster (cache hit)
        speedup = t1 / t2 if t2 > 0 else float('inf')
        assert speedup >= 1.5, f"Expected ≥1.5× speedup, got {speedup:.2f}×"
    
    def test_cache_disabled_mode(self, tmp_path):
        """Test that cache can be disabled."""
        # Set cache to a temporary directory that we'll delete
        temp_cache_dir = tmp_path / "temp_cache"
        os.environ["KIMERA_CACHE_DIR"] = str(temp_cache_dir)
        
        # Create and immediately remove cache directory to simulate disabled cache
        temp_cache_dir.mkdir()
        shutil.rmtree(temp_cache_dir)
        
        # Should still work without cache (graceful degradation)
        v1 = sem_encoder("test without cache", "en")
        v2 = sem_encoder("test without cache", "en")
        
        # Vectors should still be identical (same input)
        assert np.allclose(v1, v2)


def test_cache_environment_variable():
    """Test that cache respects KIMERA_CACHE_DIR environment variable."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        os.environ["KIMERA_CACHE_DIR"] = tmp_dir
        
        # Import after setting env var
        from kimera.cache import get_cache_dir
        
        assert str(get_cache_dir()) == tmp_dir


if __name__ == "__main__":
    pytest.main([__file__])