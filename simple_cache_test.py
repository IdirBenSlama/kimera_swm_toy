#!/usr/bin/env python3
"""Simple cache test."""

import sys
from pathlib import Path
import tempfile
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Set cache dir to temp
with tempfile.TemporaryDirectory() as tmp_dir:
    os.environ["KIMERA_CACHE_DIR"] = tmp_dir
    
    from kimera.cache import embed_cache, get_cache_stats
    import numpy as np
    
    print("Testing basic cache operations...")
    
    # Test basic set/get
    text = "test text"
    lang = "en"
    vec = np.array([1.0, 2.0, 3.0])
    
    # Set
    embed_cache.set(lang, text, vec)
    print(f"Set vector: {vec}")
    
    # Get
    cached_vec = embed_cache.get(lang, text)
    print(f"Got vector: {cached_vec}")
    
    # Check if they match
    if cached_vec is not None and np.allclose(vec, cached_vec):
        print("✅ Cache test passed!")
    else:
        print("❌ Cache test failed!")
    
    # Check stats
    stats = get_cache_stats()
    print(f"Cache stats: {stats}")