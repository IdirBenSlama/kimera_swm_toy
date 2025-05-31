# Phase 2.1 Fixes Applied

## 🔧 Issues Fixed

### 1. **`init_geoid() got an unexpected keyword argument 'raw'`** ✅

**Problem**: The benchmark code was calling `init_geoid(text, lang, layers, raw=text)` but the function signature only accepted 3 parameters.

**Fix**: Updated `src/kimera/geoid.py`:
```python
# Before
def init_geoid(text: str, lang: str, layers: List[str]) -> Geoid:

# After  
def init_geoid(text: str, lang: str, layers: List[str], *, raw: str | None = None) -> Geoid:
    if raw is None:
        raw = text
```

**Result**: Now accepts optional `raw` parameter while maintaining backward compatibility.

### 2. **`ModuleNotFoundError: No module named 'numpy'` and `'psutil'`** ✅

**Problem**: Scripts were run with system Python instead of Poetry's virtual environment.

**Fix**: 
- Updated all script docstrings with proper Poetry commands
- Added clear instructions in README
- Created `test_fixes.py` to verify everything works

**Usage**:
```bash
# Always use Poetry
poetry run python test_fixes.py
poetry run python run_validation.py
poetry run python test_streaming_benchmark.py

# Or activate shell once
poetry shell
python test_fixes.py
```

### 3. **PyTest return value warnings** ✅

**Problem**: Test functions were returning `True/False` instead of using assertions.

**Fix**: Updated `test_quick.py`:
```python
# Before
def test_something():
    try:
        # ... test code ...
        return True
    except:
        return False

# After
def test_something():
    try:
        # ... test code ...
        assert True  # Test passed
    except Exception as e:
        assert False, f"Test failed: {e}"
```

### 4. **KimeraBenchmark raw parameter consistency** ✅

**Problem**: KimeraBenchmark was calling `init_geoid()` without the `raw` parameter.

**Fix**: Updated `benchmarks/llm_compare.py`:
```python
# Before
geoid1 = init_geoid(text1, "en", ["benchmark"])

# After
geoid1 = init_geoid(text1, "en", ["benchmark"], raw=text1)
```

## 🧪 Verification

### New Test File: `test_fixes.py`
Comprehensive test to verify all fixes:
- ✅ `init_geoid` accepts `raw` parameter
- ✅ `init_geoid` defaults `raw` to `text` when not provided
- ✅ `KimeraBenchmark.detect_contradiction` works with text inputs
- ✅ Streaming functions import successfully

### Updated Documentation
- ✅ All scripts now have Poetry usage instructions
- ✅ README updated with proper command examples
- ✅ Clear error prevention guidance

## 🚀 Next Steps

### Immediate Testing
```bash
# 1. Test the fixes
poetry run python test_fixes.py

# 2. Run full test suite
poetry run pytest -q

# 3. Test small benchmark
poetry run python -m benchmarks.llm_compare --kimera-only --max-pairs 5
```

### Ready for Phase 2.2
With these fixes, the foundation is solid for:
- **Multiprocessing**: Parallel Kimera geoid computation
- **Async API calls**: Concurrent OpenAI requests  
- **Persistent caching**: Embedding and resonance caches

## 📋 Command Sequence Summary

```bash
# Install/update dependencies
poetry lock
poetry install

# Test fixes
poetry run python test_fixes.py

# Run full test suite
poetry run pytest -q

# Test benchmark (with API key if available)
export OPENAI_API_KEY="sk-..."  # or $env:OPENAI_API_KEY = "sk-..." in PowerShell
poetry run python -m benchmarks.llm_compare data/toy_contradictions.csv --model gpt-4o-mini --max-pairs 5

# Test Kimera-only mode (no API key needed)
poetry run python -m benchmarks.llm_compare --kimera-only --max-pairs 10
```

**Expected Result**: All tests pass, benchmark runs successfully, ready for Phase 2.2! 🎉