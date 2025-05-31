#!/usr/bin/env python3
"""
Quick test to verify the bootstrap_ci fix works.
"""

def test_bootstrap_fix():
    """Test that bootstrap_ci works with the new signature."""
    try:
        from kimera.metrics import roc_stats, bootstrap_ci
        import numpy as np
        
        # Create test data
        y_true = np.array([1, 0, 1, 1, 0, 1, 0, 0, 1, 0])
        y_scores = np.array([0.9, 0.1, 0.8, 0.7, 0.2, 0.85, 0.15, 0.3, 0.75, 0.25])
        
        # Test bootstrap with correct signature
        auroc_fn = lambda yt, ys: roc_stats(yt, ys)["auroc"]
        ci_lower, ci_upper = bootstrap_ci(auroc_fn, y_true, y_scores, n=50, seed=42)
        
        print(f"[SUCCESS] Bootstrap CI: [{ci_lower:.3f}, {ci_upper:.3f}]")
        return True
        
    except Exception as e:
        print(f"[FAIL] Bootstrap test failed: {e}")
        return False

if __name__ == "__main__":
    test_bootstrap_fix()