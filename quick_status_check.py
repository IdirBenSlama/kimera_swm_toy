#!/usr/bin/env python3
"""
Quick status check to verify critical fixes.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Quick status check."""
    print("🎯 Quick Status Check")
    print("=" * 30)
    
    # Test 1: Core imports
    print("🔧 Testing core imports...")
    try:
        from kimera.geoid import init_geoid
        print("✅ Geoid import successful")
        
        from kimera.metrics import roc_stats, bootstrap_ci
        print("✅ Metrics import successful")
        
        # Test basic functionality
        geoid = init_geoid("test", "en", ["test"])
        print(f"✅ Geoid creation works: {geoid.gid[:12]}...")
        
    except Exception as e:
        print(f"❌ Core imports failed: {e}")
        return False
    
    print()
    
    # Test 2: Encoding
    print("🔧 Testing encoding fix...")
    try:
        from kimera.utils.safe_console import safe_print
        safe_print("✅ Encoding test: Hello 👋 World 🌍")
        print("✅ Safe console works")
    except Exception as e:
        print(f"❌ Encoding test failed: {e}")
        return False
    
    print()
    
    # Test 3: Bootstrap CI
    print("🔧 Testing bootstrap CI fix...")
    try:
        import numpy as np
        
        y_true = np.array([1, 0, 1, 1, 0])
        y_scores = np.array([0.9, 0.1, 0.8, 0.7, 0.2])
        
        auroc_fn = lambda yt, ys: roc_stats(yt, ys)["auroc"]
        ci_lower, ci_upper = bootstrap_ci(auroc_fn, y_true, y_scores, n=10, seed=42)
        
        print(f"✅ Bootstrap CI works: [{ci_lower:.3f}, {ci_upper:.3f}]")
        
    except Exception as e:
        print(f"❌ Bootstrap CI test failed: {e}")
        return False
    
    print()
    print("=" * 30)
    print("🎉 ALL CRITICAL FIXES VERIFIED!")
    print("\n✅ Status:")
    print("  - Unicode encoding: FIXED")
    print("  - Bootstrap CI signature: FIXED") 
    print("  - Core functionality: WORKING")
    print("\n📋 Ready for:")
    print("  1. python validate_all_green.py")
    print("  2. poetry run pytest -q")
    print("  3. Benchmark testing")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)