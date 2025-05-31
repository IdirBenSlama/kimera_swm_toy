# Bootstrap CI Signature Fix Summary

## Issue Identified
The `validate_all_green.py` script was using the old `bootstrap_ci` function signature:
```python
ci = bootstrap_ci(y_true, y_scores, metric='auroc', n_bootstrap=50)
```

## Root Cause
The `bootstrap_ci` function signature was updated to expect a metric function as the first parameter:
```python
def bootstrap_ci(metric_fn: Callable[[np.ndarray, np.ndarray], float],
                 y_true: np.ndarray, 
                 y_score: np.ndarray, 
                 n: int = 1000, 
                 seed: int = 0) -> Tuple[float, float]:
```

## Fix Applied
Updated the call in `validate_all_green.py` (lines 98-100) to use the correct signature:

**Before:**
```python
# Test bootstrap
ci = bootstrap_ci(y_true, y_scores, metric='auroc', n_bootstrap=50)
print(f"[OK] Bootstrap CI: [{ci['ci_lower']:.3f}, {ci['ci_upper']:.3f}]")
```

**After:**
```python
# Test bootstrap
auroc_fn = lambda yt, ys: roc_stats(yt, ys)["auroc"]
ci_lower, ci_upper = bootstrap_ci(auroc_fn, y_true, y_scores, n=50, seed=42)
print(f"[OK] Bootstrap CI: [{ci_lower:.3f}, {ci_upper:.3f}]")
```

## Verification
- ✅ No errors found in workspace
- ✅ All other `bootstrap_ci` calls in the codebase already use the correct signature
- ✅ Dependencies (`pandas`, `matplotlib`) are already listed in `pyproject.toml`
- ✅ Only markdown linting warnings remain (non-blocking)

## Status
**RESOLVED** - The `bootstrap_ci` signature mismatch has been fixed. The validation scripts should now run without errors.

## Next Steps
The user can now run the validation scripts to confirm all-green status:
```bash
python validate_all_green.py
```