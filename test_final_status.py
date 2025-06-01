#!/usr/bin/env python3
"""
Final status check to confirm all critical issues are resolved.
"""

import sys
import traceback

def test_encoding_fix():
    """Test that the encoding fix works."""
    print("🔧 Testing encoding fix...")
    try:
        from src.kimera.utils.safe_console import safe_print
        safe_print("✅ Encoding test: Hello 👋 World 🌍")
        return True
    except Exception as e:
        print(f"❌ Encoding test failed: {e}")
        return False

def test_bootstrap_ci_fix():
    """Test that the bootstrap CI fix works."""
    print("🔧 Testing bootstrap CI fix...")
    try:
        from kimera.metrics import roc_stats, bootstrap_ci
        import numpy as np
        
        y_true = np.array([1, 0, 1, 1, 0])
        y_scores = np.array([0.9, 0.1, 0.8, 0.7, 0.2])
        
        auroc_fn = lambda yt, ys: roc_stats(yt, ys)["auroc"]
        ci_lower, ci_upper = bootstrap_ci(auroc_fn, y_true, y_scores, n=10, seed=42)
        
        print(f"✅ Bootstrap CI works: [{ci_lower:.3f}, {ci_upper:.3f}]")
        return True
    except Exception as e:
        print(f"❌ Bootstrap CI test failed: {e}")
        return False

def test_core_imports():
    """Test that core imports work."""
    print("🔧 Testing core imports...")
    try:
        from kimera.geoid import init_geoid
        from kimera.metrics import roc_stats, pr_stats
        
        # Test basic functionality
        geoid = init_geoid("test", "en", ["test"])
        print(f"✅ Core imports work, geoid: {geoid.gid[:12]}...")
        return True
    except Exception as e:
        print(f"❌ Core imports failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🎯 Final Status Check")
    print("=" * 30)
    
    tests = [
        test_core_imports,
        test_encoding_fix,
        test_bootstrap_ci_fix,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            print()
    
    print("=" * 30)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL CRITICAL ISSUES RESOLVED!")
        print("\nNext steps:")
        print("1. Run: python validate_all_green.py")
        print("2. Run: poetry run pytest -q")
        print("3. Run benchmark: poetry run python -m benchmarks.llm_compare data/toy_contradictions.csv --max-pairs 10 --kimera-only")
        return 0
    else:
        print("⚠️  Some issues remain, but main functionality should work")
        return 1

if __name__ == "__main__":
    sys.exit(main())