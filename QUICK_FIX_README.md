# Kimera-SWM Quick Fix Guide

## The Issues You Hit

1. **"No module named 'pandas' / 'matplotlib'"** - Dependencies declared in `pyproject.toml` but not installed
2. **PowerShell line continuation error** - The `\` character at end of line doesn't work in PowerShell

## Quick Solutions

### Option 1: Automated Fix (Recommended)
```bash
python setup_and_run.py
```
This script will:
- Check all dependencies
- Install missing packages via Poetry
- Run validation tests
- Execute a quick benchmark
- Show you the results

### Option 2: Manual Fix
```bash
# 1. Install missing dependencies
poetry install

# 2. Run validation (should show 6/6 green)
python validate_all_green.py

# 3. Run benchmark (single line, no continuation issues)
poetry run python -m benchmarks.llm_compare data/toy_contradictions.csv --max-pairs 20 --stats --kimera-only
```

### Option 3: Windows Users
Use the batch file instead of PowerShell:
```cmd
run_benchmark.bat
```

Or use the fixed PowerShell script:
```powershell
.\run_benchmark_fixed.ps1
```

## What Should Happen

1. **Dependencies install** - pandas, matplotlib, etc. get properly installed
2. **Validation passes** - All 6 tests should be green
3. **Benchmark runs** - Processes 20 pairs from toy dataset
4. **Files generated**:
   - `benchmark_results.csv` - Raw results
   - `metrics.yaml` - AUROC/PR-AUC stats
   - `roc.png` - ROC curve visualization

## Next Steps After Success

1. **Open `tools/explorer.html`** in your browser
2. **Load `benchmark_results.csv`**
3. **Check "Only disagreements"** to see where Kimera fails
4. **Analyze failure patterns** - Look for:
   - Negation handling issues
   - Temporal reasoning failures
   - Numeric comparison problems
   - Language-specific issues

## If Still Having Issues

### Check Poetry Installation
```bash
poetry --version
```
If not found, install from: https://python-poetry.org/docs/#installation

### Check Python Version
```bash
python --version
```
Should be 3.9-3.11 (3.12+ not supported yet)

### Manual Dependency Check
```bash
python quick_dependency_check.py
```

### Force Reinstall
```bash
poetry lock
poetry install --no-cache
```

## The Big Picture

You're at **Phase 2.4 complete** with:
- ✅ Persistent embedding cache
- ✅ In-memory resonance cache  
- ✅ Metrics & visualization tools
- ✅ Benchmark infrastructure

The next meaningful work is **empirical analysis** - look at those disagreement patterns and design targeted algorithm improvements based on what you find.