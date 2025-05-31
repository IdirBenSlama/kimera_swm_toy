#!/usr/bin/env python3
"""Quick test to verify metrics implementation works."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_basic_import():
    """Test that metrics module imports correctly."""
    try:
        from kimera.metrics import roc_stats, pr_stats, bootstrap_ci
        print("✅ Metrics module imports successfully")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic metric computation."""
    try:
        import numpy as np
        from kimera.metrics import roc_stats, pr_stats
        
        # Perfect classifier test
        y_true = np.array([0, 0, 1, 1])
        y_score = np.array([0.1, 0.2, 0.8, 0.9])
        
        roc = roc_stats(y_true, y_score)
        pr = pr_stats(y_true, y_score)
        
        assert abs(roc["auroc"] - 1.0) < 1e-6, f"Expected AUROC=1.0, got {roc['auroc']}"
        assert abs(pr["aupr"] - 1.0) < 1e-6, f"Expected AUPR=1.0, got {pr['aupr']}"
        
        print("✅ Basic functionality test passed")
        return True
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def main():
    print("🧪 Quick Metrics Test - Kimera-SWM v0.7.0")
    print("=" * 45)
    
    tests = [
        test_basic_import,
        test_basic_functionality
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    if all(results):
        print("\n🎉 All quick tests passed!")
        print("Metrics infrastructure is ready for use.")
        print("\nTry: python demo_metrics.py")
        return True
    else:
        print(f"\n❌ {len(results) - sum(results)} test(s) failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)