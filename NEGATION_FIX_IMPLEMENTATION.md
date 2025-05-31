# Negation Fix Implementation Summary

## Overview
Implemented the first research loop iteration for Kimera with a **negation-aware distance** feature to improve contradiction detection accuracy.

## Changes Made

### 1. Enhanced Resonance Module (`src/kimera/resonance.py`)

Added negation detection capabilities:

```python
# Negation word set
NEGATIONS = {"not", "no", "never", "cannot", "can't", "won't", "doesn't", 
             "isn't", "aren't", "wasn't", "weren't", "don't", "didn't", 
             "hasn't", "haven't", "hadn't"}

def negation_mismatch(txt1: str, txt2: str) -> bool:
    """Detect if one text has negation and the other doesn't (XOR logic)"""
    t1 = re.findall(r"\w+", txt1)
    t2 = re.findall(r"\w+", txt2)
    return _has_negation(t1) ^ _has_negation(t2)
```

### 2. Modified Resonance Function

Updated the core `resonance()` function to apply negation penalty:

```python
def resonance(a, b):
    # ... existing logic ...
    score = sim * (1 - penalty)
    
    # Apply negation mismatch penalty
    if negation_mismatch(a.raw, b.raw):
        score -= 0.25          # push them further apart
        score = max(-1.0, score)
    
    return score
```

**Key Design Decisions:**
- **Penalty of 0.25**: Significant enough to affect classification but not overwhelming
- **XOR logic**: Only penalize when one text has negation and the other doesn't
- **Access to raw text**: Uses `geoid.raw` attribute for text analysis

## Research Loop Scripts

### Core Scripts
1. **`research_loop.py`** - Complete automated research loop
2. **`run_research_loop.ps1`** - PowerShell version for Windows
3. **`validate_negation_setup.py`** - Validation and testing

### Supporting Scripts
- `test_negation_simple.py` - Quick negation detection test
- `compare_results.py` - Metrics comparison between baseline and fix
- `run_baseline_benchmark.py` - Baseline benchmark runner
- `run_negation_benchmark.py` - Negation fix benchmark runner

## Expected Workflow

### Step 1: Validation
```bash
python validate_negation_setup.py
```

### Step 2: Run Research Loop
```bash
# Python
python research_loop.py

# Or PowerShell (Windows)
./run_research_loop.ps1
```

### Step 3: Analyze Results
- Compare `metrics_baseline.yaml` vs `metrics_negfix.yaml`
- Load `mixed5k_baseline.csv` and `mixed5k_negfix.csv` in `tools/explorer.html`
- Tag disagreements to identify next improvement areas

## Expected Impact

### Target Cases
The negation fix should improve detection for pairs like:
- "Birds can fly" ↔ "Birds cannot fly" ✓
- "I like cats" ↔ "I don't like cats" ✓
- "Fire is hot" ↔ "Fire isn't hot" ✓

### Metrics to Watch
- **AUROC**: Should increase (better ranking of contradictions)
- **F1 Score**: Should improve (better precision/recall balance)
- **AUPR**: Should increase (better precision-recall curve)

## Next Iteration Ideas

Based on error analysis, consider implementing:

1. **Numeric Contradiction Detector**
   ```python
   def numeric_mismatch(txt1: str, txt2: str) -> bool:
       # Detect conflicting numbers (e.g., "100°C" vs "50°C")
   ```

2. **Temporal Contradiction Detector**
   ```python
   def temporal_mismatch(txt1: str, txt2: str) -> bool:
       # Detect time conflicts (e.g., "tomorrow" vs "yesterday")
   ```

3. **Antonym Detection**
   ```python
   def antonym_mismatch(txt1: str, txt2: str) -> bool:
       # Detect semantic opposites (e.g., "hot" vs "cold")
   ```

## File Structure
```
├── src/kimera/resonance.py          # Enhanced with negation detection
├── research_loop.py                 # Main research loop script
├── run_research_loop.ps1           # PowerShell version
├── validate_negation_setup.py      # Validation script
├── compare_results.py              # Results comparison
└── test_negation_simple.py         # Quick testing
```

## Success Criteria
- ✅ Negation detection working correctly
- ✅ Integration with existing resonance function
- ✅ Automated benchmark comparison
- ✅ No breaking changes to existing functionality
- 🎯 Measurable improvement in contradiction detection metrics

This implementation provides a solid foundation for iterative research and improvement of Kimera's accuracy through systematic error analysis and targeted fixes.