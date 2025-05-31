#!/usr/bin/env python3
"""
Quick test to verify the bootstrap_ci fix and core functionality.
"""

def test_imports():
    """Test critical imports."""
    print("Testing imports...")
    try:
        import pandas as pd
        print("✅ pandas imported")
        
        import matplotlib.pyplot as plt
        print("✅ matplotlib imported")
        
        from kimera.metrics import roc_stats, pr_stats, bootstrap_ci
        print("✅ kimera.metrics imported")
        
        from kimera.geoid import Geoid
        print("✅ kimera.geoid imported")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_bootstrap_ci():
    """Test bootstrap_ci with correct signature."""
    print("\nTesting bootstrap_ci...")
    try:
        from kimera.metrics import roc_stats, bootstrap_ci
        import numpy as np
        
        # Create test data
        y_true = np.array([1, 0, 1, 1, 0, 1, 0, 0, 1, 0])
        y_scores = np.array([0.9, 0.1, 0.8, 0.7, 0.2, 0.85, 0.15, 0.3, 0.75, 0.25])
        
        # Test bootstrap with correct signature
        auroc_fn = lambda yt, ys: roc_stats(yt, ys)["auroc"]
        ci_lower, ci_upper = bootstrap_ci(auroc_fn, y_true, y_scores, n=50, seed=42)
        
        print(f"✅ Bootstrap CI: [{ci_lower:.3f}, {ci_upper:.3f}]")
        return True
        
    except Exception as e:
        print(f"❌ Bootstrap test failed: {e}")
        return False

def test_core_engine():
    """Test core Kimera engine."""
    print("\nTesting core engine...")
    try:
        from kimera.geoid import Geoid
        
        # Quick engine test
        engine = Geoid()
        result = engine.compare("The sky is blue", "The sky is not blue")
        
        print(f"✅ Core engine works: contradiction score = {result:.3f}")
        return True
        
    except Exception as e:
        print(f"❌ Core engine test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🔍 QUICK VALIDATION TEST")
    print("=" * 40)
    
    tests = [
        ("Imports", test_imports),
        ("Bootstrap CI", test_bootstrap_ci), 
        ("Core Engine", test_core_engine)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ {name} test crashed: {e}")
            results.append(False)
    
    print("\n" + "=" * 40)
    print("SUMMARY")
    print("=" * 40)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 ALL TESTS PASSED ({passed}/{total})")
        print("✅ Ready for full validation!")
    else:
        print(f"⚠️  SOME TESTS FAILED ({passed}/{total})")
    
    return passed == total

if __name__ == "__main__":
    main()