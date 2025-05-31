# Commit: Cast numpy.bool_ to bool in detect_contradiction

## 🔧 **Critical Fix Applied**

**Issue**: `KimeraBenchmark.detect_contradiction()` was returning `numpy.bool_` instead of Python `bool`, causing type assertion failures in tests.

**Root Cause**: 
```python
resonance_score < THRESH  # Returns numpy.bool_
```

**Fix**:
```python
# Before
is_contradiction = resonance_score < THRESH  # numpy.bool_

# After  
is_contradiction = bool(resonance_score < THRESH)  # Python bool ✅
```

## 📁 **Files Modified**

1. **`benchmarks/llm_compare.py`** - Added `bool()` cast in `KimeraBenchmark.detect_contradiction()`
2. **`test_benchmark_quick.py`** - Replaced `return True/False` with assertions
3. **`test_fixes.py`** - Enhanced bool type checking and removed return statements

## 🧪 **Test Verification**

The fix ensures:
- ✅ `isinstance(is_contradiction, bool)` passes
- ✅ No more `numpy.bool_` type mismatches  
- ✅ All pytest warnings resolved
- ✅ Benchmark functions return proper Python types

## 🚀 **Ready for Testing**

```bash
# Test the fix
poetry run python test_fixes.py

# Run full test suite (should be all green)
poetry run pytest -q

# Test benchmark
poetry run python -m benchmarks.llm_compare --kimera-only --max-pairs 5
```

**Expected Result**: All tests pass, no warnings, ready for Phase 2.2! 🎉