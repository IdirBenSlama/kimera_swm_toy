#!/usr/bin/env python3
"""Verify cache functionality works."""

import sys
import os
import tempfile
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """Test cache functionality."""
    print("🧪 Verifying cache functionality...")
    
    # Use temporary directory
    with tempfile.TemporaryDirectory() as tmp_dir:
        os.environ["KIMERA_CACHE_DIR"] = tmp_dir
        print(f"Using cache dir: {tmp_dir}")
        
        # Import after setting env var
        from kimera.cache import embed_cache, get_cache_stats, clear_embedding_cache
        from kimera.geoid import sem_encoder
        
        # Clear cache
        clear_embedding_cache()
        
        # Test basic functionality
        text = "Hello cache test"
        lang = "en"
        
        print("Testing cache miss (first call)...")
        t0 = time.perf_counter()
        v1 = sem_encoder(text, lang)
        t1 = time.perf_counter() - t0
        print(f"  First call: {t1*1000:.1f}ms, vector shape: {v1.shape}")
        
        print("Testing cache hit (second call)...")
        t0 = time.perf_counter()
        v2 = sem_encoder(text, lang)
        t2 = time.perf_counter() - t0
        print(f"  Second call: {t2*1000:.1f}ms, vector shape: {v2.shape}")
        
        # Check if vectors match
        import numpy as np
        if np.allclose(v1, v2):
            print("✅ Vectors match!")
        else:
            print("❌ Vectors don't match!")
            return False
        
        # Check speedup
        if t2 < t1:
            speedup = t1 / t2 if t2 > 0 else float('inf')
            print(f"✅ Cache speedup: {speedup:.1f}x")
        else:
            print("⚠️  No speedup detected (might be normal in some environments)")
        
        # Check cache stats
        stats = get_cache_stats()
        print(f"Cache stats: {stats}")
        
        if stats['embedding_cache_size'] >= 1:
            print("✅ Cache contains embeddings!")
        else:
            print("❌ Cache is empty!")
            return False
        
        print("🎉 Cache verification successful!")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)