#!/usr/bin/env python3
"""Test the timing assertion fix."""

import sys
import os
import tempfile
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_timing_assertion():
    """Test that the new timing assertion is robust."""
    print("🧪 Testing robust timing assertion...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        os.environ["KIMERA_CACHE_DIR"] = tmp_dir
        
        # Clear any cached modules
        import sys
        modules_to_clear = [m for m in sys.modules.keys() if m.startswith('kimera')]
        for m in modules_to_clear:
            if m in sys.modules:
                del sys.modules[m]
        
        from kimera.cache import clear_embedding_cache
        from kimera.geoid import sem_encoder
        
        clear_embedding_cache()
        
        text = "Timing test text"
        lang = "en"
        
        # First call (cache miss)
        print("  First call (cache miss)...")
        t0 = time.perf_counter()
        v1 = sem_encoder(text, lang)
        t1 = time.perf_counter() - t0
        print(f"    Time: {t1*1000:.1f}ms")
        
        # Second call (cache hit)
        print("  Second call (cache hit)...")
        t0 = time.perf_counter()
        v2 = sem_encoder(text, lang)
        t2 = time.perf_counter() - t0
        print(f"    Time: {t2*1000:.1f}ms")
        
        # Calculate speedup
        speedup = t1 / t2 if t2 > 0 else float('inf')
        print(f"  Speedup: {speedup:.2f}×")
        
        # Test the assertion logic
        assertion_passes = speedup >= 1.5
        print(f"  Assertion (≥1.5×): {'✅ PASS' if assertion_passes else '❌ FAIL'}")
        
        # Verify vectors match
        import numpy as np
        vectors_match = np.allclose(v1, v2)
        print(f"  Vectors match: {'✅ PASS' if vectors_match else '❌ FAIL'}")
        
        return assertion_passes and vectors_match

def main():
    """Run timing test."""
    print("🚀 Testing timing assertion robustness...")
    
    success = test_timing_assertion()
    
    if success:
        print("\n🎉 Timing assertion fix working correctly!")
        print("Cache provides measurable speedup with robust testing.")
        return 0
    else:
        print("\n❌ Timing assertion still needs adjustment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())