#!/usr/bin/env python3
"""
Simple test runner to verify our fixes.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_encoding():
    """Test encoding fix."""
    print("🔧 Testing encoding fix...")
    try:
        from kimera.utils.safe_console import safe_print
        safe_print("✅ Encoding test: Hello 👋 World 🌍")
        return True
    except Exception as e:
        print(f"❌ Encoding test failed: {e}")
        return False

def test_imports():
    """Test core imports."""
    print("🔧 Testing core imports...")
    try:
        from kimera.geoid import init_geoid
        from kimera.metrics import roc_stats, bootstrap_ci
        
        # Test basic functionality
        geoid = init_geoid("test", "en", ["test"])
        print(f"✅ Core imports work, geoid: {geoid.gid[:12]}...")
        return True
    except Exception as e:
        print(f"❌ Core imports failed: {e}")
        return False

def test_bootstrap():
    """Test bootstrap CI fix."""
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

def main():
    """Run all tests."""
    print("🎯 Quick Status Check")
    print("=" * 30)
    
    tests = [test_imports, test_encoding, test_bootstrap]
    passed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            print()
    
    print("=" * 30)
    print(f"📊 Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ Critical issues resolved:")
        print("  - Unicode encoding fixed")
        print("  - Bootstrap CI signature fixed")
        print("  - Core functionality working")
        print("\n📋 Next steps:")
        print("  1. Run: python validate_all_green.py")
        print("  2. Run: poetry run pytest -q")
        return True
    else:
        print("⚠️  Some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)