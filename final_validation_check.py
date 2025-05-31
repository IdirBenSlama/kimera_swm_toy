#!/usr/bin/env python3
"""
Final validation check to confirm all-green status.
"""

import sys
import traceback

def test_critical_imports():
    """Test all critical imports that were causing issues."""
    print("🔍 Testing critical imports...")
    
    try:
        # Test pandas and matplotlib (the missing dependencies)
        import pandas as pd
        print("✅ pandas imported successfully")
        
        import matplotlib.pyplot as plt
        print("✅ matplotlib imported successfully")
        
        # Test kimera modules
        from kimera.metrics import roc_stats, pr_stats, bootstrap_ci
        print("✅ kimera.metrics imported successfully")
        
        from kimera.geoid import Geoid
        print("✅ kimera.geoid imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_bootstrap_ci_signature():
    """Test the fixed bootstrap_ci signature."""
    print("\n🔧 Testing bootstrap_ci signature fix...")
    
    try:
        from kimera.metrics import roc_stats, bootstrap_ci
        import numpy as np
        
        # Create test data (same as in validate_all_green.py)
        y_true = np.array([1, 0, 1, 1, 0, 1, 0, 0, 1, 0])
        y_scores = np.array([0.9, 0.1, 0.8, 0.7, 0.2, 0.85, 0.15, 0.3, 0.75, 0.25])
        
        # Test the NEW signature (should work)
        auroc_fn = lambda yt, ys: roc_stats(yt, ys)["auroc"]
        ci_lower, ci_upper = bootstrap_ci(auroc_fn, y_true, y_scores, n=50, seed=42)
        
        print(f"✅ New signature works: CI = [{ci_lower:.3f}, {ci_upper:.3f}]")
        
        # Verify the old signature would fail (just for confirmation)
        try:
            # This should fail now
            old_result = bootstrap_ci(y_true, y_scores, metric='auroc', n_bootstrap=50)
            print("❌ Old signature still works - this shouldn't happen!")
            return False
        except TypeError:
            print("✅ Old signature correctly fails (as expected)")
        
        return True
        
    except Exception as e:
        print(f"❌ Bootstrap CI test failed: {e}")
        traceback.print_exc()
        return False

def test_validate_all_green_logic():
    """Test the specific logic from validate_all_green.py that was fixed."""
    print("\n🎯 Testing validate_all_green.py logic...")
    
    try:
        from kimera.metrics import roc_stats, pr_stats, bootstrap_ci
        import numpy as np
        
        # Replicate the exact test from validate_all_green.py
        y_true = np.array([1, 0, 1, 1, 0, 1, 0, 0, 1, 0])
        y_scores = np.array([0.9, 0.1, 0.8, 0.7, 0.2, 0.85, 0.15, 0.3, 0.75, 0.25])
        
        # Test ROC
        roc = roc_stats(y_true, y_scores)
        print(f"✅ ROC stats - AUROC: {roc['auroc']:.3f}")
        
        # Test PR
        pr = pr_stats(y_true, y_scores)
        print(f"✅ PR stats - AUPR: {pr['aupr']:.3f}")
        
        # Test bootstrap (the fixed part)
        auroc_fn = lambda yt, ys: roc_stats(yt, ys)["auroc"]
        ci_lower, ci_upper = bootstrap_ci(auroc_fn, y_true, y_scores, n=50, seed=42)
        print(f"✅ Bootstrap CI: [{ci_lower:.3f}, {ci_upper:.3f}]")
        
        return True
        
    except Exception as e:
        print(f"❌ Validation logic test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all validation checks."""
    print("🚀 FINAL VALIDATION CHECK")
    print("Verifying bootstrap_ci fix and all-green status")
    print("=" * 60)
    
    tests = [
        ("Critical Imports", test_critical_imports),
        ("Bootstrap CI Signature", test_bootstrap_ci_signature),
        ("Validate All Green Logic", test_validate_all_green_logic)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 40)
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("🏁 FINAL SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 ALL CHECKS PASSED ({passed}/{total})")
        print("\n✅ Kimera-SWM is ALL-GREEN!")
        print("\n🚀 Ready for next steps:")
        print("   1. Run: python validate_all_green.py")
        print("   2. Run benchmark: poetry run python -m benchmarks.llm_compare data/toy_contradictions.csv --max-pairs 20 --stats --kimera-only")
        print("   3. Open tools/explorer.html to analyze results")
        print("   4. Start error-bucket analysis for algorithmic improvements")
        
    else:
        print(f"⚠️  SOME CHECKS FAILED ({passed}/{total})")
        failed_tests = [name for (name, _), result in zip(tests, results) if not result]
        print(f"Failed tests: {', '.join(failed_tests)}")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)