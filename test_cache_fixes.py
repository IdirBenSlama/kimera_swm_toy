#!/usr/bin/env python3
"""Test the cache fixes."""

import sys
import os
import tempfile
import numpy as np
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_persistence_fix():
    """Test that persistence actually works with the new implementation."""
    print("🧪 Testing cache persistence fix...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        os.environ["KIMERA_CACHE_DIR"] = tmp_dir
        
        # Clear any cached modules
        import sys
        modules_to_clear = [m for m in sys.modules.keys() if m.startswith('kimera')]
        for m in modules_to_clear:
            if m in sys.modules:
                del sys.modules[m]
        
        from kimera.cache import embed_cache, clear_embedding_cache
        from kimera.geoid import sem_encoder
        
        clear_embedding_cache()
        
        text = "Persistence test"
        lang = "en"
        
        # First encoding
        print("  Encoding first time...")
        v1 = sem_encoder(text, lang)
        print(f"  Vector shape: {v1.shape}")
        
        # Check cache files exist
        cache_dir = Path(tmp_dir)
        pkl_files = list(cache_dir.glob("*.pkl"))
        print(f"  Cache files created: {len(pkl_files)}")
        
        # Create new cache instance (simulate new session)
        from kimera.cache import EmbeddingCache
        new_cache = EmbeddingCache()
        
        # Should find the cached embedding
        cached_vec = new_cache.get(lang, text)
        print(f"  Cached vector found: {cached_vec is not None}")
        
        if cached_vec is not None:
            print(f"  Cached vector shape: {cached_vec.shape}")
            match = np.allclose(v1, cached_vec)
            print(f"  Vectors match: {match}")
            return match
        else:
            return False

def test_language_keying():
    """Test that language keying works correctly."""
    print("\n🧪 Testing language keying fix...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        os.environ["KIMERA_CACHE_DIR"] = tmp_dir
        
        # Clear any cached modules
        import sys
        modules_to_clear = [m for m in sys.modules.keys() if m.startswith('kimera')]
        for m in modules_to_clear:
            if m in sys.modules:
                del sys.modules[m]
        
        from kimera.cache import embed_cache, clear_embedding_cache, get_cache_stats
        from kimera.geoid import sem_encoder
        
        clear_embedding_cache()
        
        text = "Hello world"
        
        # Encode in different languages
        print("  Encoding in English...")
        v_en = sem_encoder(text, "en")
        
        print("  Encoding in French...")
        v_fr = sem_encoder(text, "fr")
        
        # Check cache entries
        en_cached = embed_cache.get("en", text)
        fr_cached = embed_cache.get("fr", text)
        
        print(f"  English cached: {en_cached is not None}")
        print(f"  French cached: {fr_cached is not None}")
        
        # Check cache stats
        stats = get_cache_stats()
        print(f"  Cache size: {stats['embedding_cache_size']}")
        
        # Verify keying works
        if en_cached is not None and fr_cached is not None:
            en_match = np.allclose(v_en, en_cached)
            fr_match = np.allclose(v_fr, fr_cached)
            print(f"  English key match: {en_match}")
            print(f"  French key match: {fr_match}")
            return en_match and fr_match and stats['embedding_cache_size'] >= 2
        
        return False

def main():
    """Run cache fix tests."""
    print("🚀 Testing cache fixes...")
    
    success1 = test_persistence_fix()
    success2 = test_language_keying()
    
    print(f"\n📊 Results:")
    print(f"  Persistence fix: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"  Language keying fix: {'✅ PASS' if success2 else '❌ FAIL'}")
    
    if success1 and success2:
        print("\n🎉 All cache fixes working correctly!")
        return 0
    else:
        print("\n❌ Some fixes still need work.")
        return 1

if __name__ == "__main__":
    sys.exit(main())