#!/usr/bin/env python3
"""Demo of cache functionality."""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """Demo cache functionality."""
    print("🚀 Kimera Cache Demo")
    print("=" * 50)
    
    from kimera.cache import get_cache_stats, clear_embedding_cache
    from kimera.geoid import init_geoid
    
    # Clear cache for clean demo
    clear_embedding_cache()
    
    # Show initial cache stats
    stats = get_cache_stats()
    print(f"Initial cache stats:")
    print(f"  Cache directory: {stats['cache_dir']}")
    print(f"  Embedding cache size: {stats['embedding_cache_size']}")
    print(f"  Resonance cache size: {stats['resonance_cache_size']}")
    print()
    
    # Create some geoids
    texts = [
        "The quick brown fox jumps over the lazy dog",
        "Machine learning is transforming the world",
        "Cache systems improve performance significantly"
    ]
    
    print("Creating geoids (first time - cache miss)...")
    geoids = []
    total_time_1 = 0
    
    for i, text in enumerate(texts):
        t0 = time.perf_counter()
        geoid = init_geoid(text, "en", ["demo"])
        t1 = time.perf_counter() - t0
        total_time_1 += t1
        geoids.append(geoid)
        print(f"  Geoid {i+1}: {t1*1000:.1f}ms")
    
    print(f"Total time (first run): {total_time_1*1000:.1f}ms")
    print()
    
    # Show cache stats after first run
    stats = get_cache_stats()
    print(f"Cache stats after first run:")
    print(f"  Embedding cache size: {stats['embedding_cache_size']}")
    print(f"  Cache file exists: {stats['cache_file_exists']}")
    if stats['cache_file_exists']:
        print(f"  Cache file size: {stats['cache_file_size_mb']:.3f} MB")
    print()
    
    # Create same geoids again (cache hit)
    print("Creating same geoids again (cache hit)...")
    total_time_2 = 0
    
    for i, text in enumerate(texts):
        t0 = time.perf_counter()
        geoid = init_geoid(text, "en", ["demo"])
        t1 = time.perf_counter() - t0
        total_time_2 += t1
        print(f"  Geoid {i+1}: {t1*1000:.1f}ms")
    
    print(f"Total time (second run): {total_time_2*1000:.1f}ms")
    
    # Calculate speedup
    if total_time_2 > 0:
        speedup = total_time_1 / total_time_2
        print(f"🚀 Speedup: {speedup:.1f}x faster!")
    
    print()
    print("✅ Cache demo completed successfully!")

if __name__ == "__main__":
    main()