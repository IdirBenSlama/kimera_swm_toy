# 🧪 Negation Fix Experiment Commands

## Quick Test (Copy-Paste Ready)

### 1. Validate Fixes
```bash
python test_fixes.py
```

### 2. Focused Experiment (Recommended First)
```bash
python focused_experiment.py
```

### 3. PowerShell Full Experiment (Windows)
```powershell
# Open PowerShell in project directory
.\run_negation_experiment.ps1
```

### 4. Manual Commands (Cross-platform)

**Baseline (negation fix OFF):**
```bash
# Linux/Mac
KIMERA_NEGATION_FIX=0 python -m benchmarks.llm_compare data/mixed_contradictions.csv --max-pairs 500 --kimera-only --outfile baseline.csv --no-emoji

# Windows PowerShell
Remove-Item Env:KIMERA_NEGATION_FIX -ErrorAction SilentlyContinue
python -m benchmarks.llm_compare data/mixed_contradictions.csv --max-pairs 500 --kimera-only --outfile baseline.csv --no-emoji
```

**Negation Fix (negation fix ON):**
```bash
# Linux/Mac  
KIMERA_NEGATION_FIX=1 python -m benchmarks.llm_compare data/mixed_contradictions.csv --max-pairs 500 --kimera-only --outfile negfix.csv --no-emoji

# Windows PowerShell
$Env:KIMERA_NEGATION_FIX = "1"
python -m benchmarks.llm_compare data/mixed_contradictions.csv --max-pairs 500 --kimera-only --outfile negfix.csv --no-emoji
```

**Compare Results:**
```bash
python compare_results.py baseline.csv negfix.csv
```

## Expected Results

### Focused Experiment
- Negation cases should show **lower scores** when negation fix is ON
- Non-negation cases should show **similar scores**

### Full Benchmark
- **AUROC/F1 improvement** with non-overlapping confidence intervals
- **Better contradiction detection** on negation patterns
- **No regression** on other cases

## Success Indicators

✅ **Significant improvement**: Non-overlapping CIs for AUROC/F1  
✅ **Directional improvement**: Lower scores for negation mismatches  
✅ **No regression**: Similar/better performance on non-negation cases

## Next Error Buckets (After Success)

1. **Numeric contradictions** ("100°C" vs "50°C")
2. **Temporal mismatches** ("will go" vs "went") 
3. **Semantic antonyms** ("hot" vs "cold")

## Troubleshooting

**Import errors**: Run `python validate_setup.py`  
**Emoji crashes**: Ensure `--no-emoji` flag is used  
**Environment variables**: Use platform-specific syntax above