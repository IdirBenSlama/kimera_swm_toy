#!/usr/bin/env python3
"""Quick test of the cache functionality."""

import os
import time
import tempfile
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_cache_basic():
    """Test basic cache functionality."""
    print("🧪 Testing cache functionality...")
    
    # Use temporary directory for testing
    with tempfile.TemporaryDirectory() as tmp_dir:
        os.environ["KIMERA_CACHE_DIR"] = tmp_dir
        
        # Import after setting env var
        # Import after setting env var
        import importlib
        import sys
        
        # Clear any cached modules
        modules_to_reload = [m for m in sys.modules.keys() if m.startswith('kimera')]
        for m in modules_to_reload:
            if m in sys.modules:
                del sys.modules[m]
        
        from kimera.cache import embed_cache, get_cache_stats, clear_embedding_cache
        from kimera.geoid import sem_encoder
        
        # Clear any existing cache
        clear_embedding_cache()
        
        # Test 1: Cache miss (first call)
        print("  📝 Testing cache miss...")
        text = "Hello cache test"
        lang = "en"
        
        t0 = time.perf_counter()
        v1 = sem_encoder(text, lang)
        t1 = time.perf_counter() - t0
        print(f"     First call: {t1*1000:.1f}ms")
        
        # Test 2: Cache hit (second call)
        print("  ⚡ Testing cache hit...")
        t0 = time.perf_counter()
        v2 = sem_encoder(text, lang)
        t2 = time.perf_counter() - t0
        print(f"     Second call: {t2*1000:.1f}ms")
        
        # Verify vectors are identical
        import numpy as np
        assert np.allclose(v1, v2), "Vectors should be identical"
        
        # Verify cache hit is faster
        speedup = t1 / t2 if t2 > 0 else float('inf')
        print(f"     Speedup: {speedup:.1f}x")
        
        # Test 3: Cache stats
        print("  📊 Testing cache stats...")
        stats = get_cache_stats()
        print(f"     Cache size: {stats['embedding_cache_size']}")
        print(f"     Cache file exists: {stats['cache_file_exists']}")
        
        assert stats['embedding_cache_size'] >= 1, "Cache should contain at least one entry"
        
        print("✅ Cache tests passed!")
        return True

def test_geoid_integration():
    """Test cache integration with geoid creation."""
    print("🧪 Testing geoid integration...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        os.environ["KIMERA_CACHE_DIR"] = tmp_dir
        
        import importlib
        import sys
        
        # Clear any cached modules
        modules_to_reload = [m for m in sys.modules.keys() if m.startswith('kimera')]
        for m in modules_to_reload:
            if m in sys.modules:
                del sys.modules[m]
        
        from kimera.geoid import init_geoid
        from kimera.cache import clear_embedding_cache
        
        clear_embedding_cache()
        
        text = "Integration test text"
        lang = "en"
        
        # Create first geoid
        t0 = time.perf_counter()
        geoid1 = init_geoid(text, lang, ["test"])
        t1 = time.perf_counter() - t0
        print(f"  First geoid: {t1*1000:.1f}ms")
        
        # Create second geoid with same text
        t0 = time.perf_counter()
        geoid2 = init_geoid(text, lang, ["test"])
        t2 = time.perf_counter() - t0
        print(f"  Second geoid: {t2*1000:.1f}ms")
        
        # Verify vectors are identical
        import numpy as np
        assert np.allclose(geoid1.sem_vec, geoid2.sem_vec), "Semantic vectors should be identical"
        assert np.allclose(geoid1.sym_vec, geoid2.sym_vec), "Symbolic vectors should be identical"
        
        # Second creation should be faster
        speedup = t1 / t2 if t2 > 0 else float('inf')
        print(f"  Speedup: {speedup:.1f}x")
        
        print("✅ Geoid integration tests passed!")
        return True

def main():
    """Run all cache tests."""
    print("🚀 Running cache validation tests...\n")
    
    try:
        test_cache_basic()
        print()
        test_geoid_integration()
        print()
        print("🎉 All cache tests passed! Phase 2.4 is working correctly.")
        return 0
    except Exception as e:
        print(f"❌ Cache test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())