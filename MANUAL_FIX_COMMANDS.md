# Manual Fix Commands

## The Issue
Your `poetry.lock` file is out of sync with `pyproject.toml`. This happens when dependencies are added to the project file but the lock file hasn't been regenerated.

## Quick Fix (Run these commands in order)

```powershell
# 1. Update the lock file to match pyproject.toml
poetry lock

# 2. Install all dependencies
poetry install

# 3. Verify everything works
python validate_all_green.py

# 4. Run a quick benchmark
poetry run python -m benchmarks.llm_compare data/toy_contradictions.csv --max-pairs 20 --stats --kimera-only
```

## Alternative: Use the Fix Script

```powershell
python fix_poetry_lock.py
```

## What Each Command Does

1. **`poetry lock`** - Regenerates the lock file based on your pyproject.toml
2. **`poetry install`** - Installs all dependencies including pandas and matplotlib
3. **`python validate_all_green.py`** - Tests that everything is working (should show 6/6 green)
4. **`poetry run python -m benchmarks.llm_compare ...`** - Runs the actual benchmark

## Expected Output After Success

- `benchmark_results.csv` - Raw comparison data
- `metrics.yaml` - Performance statistics
- `roc.png` - ROC curve visualization

## If You Still Get Errors

### Clear Poetry Cache
```powershell
poetry cache clear --all pypi
poetry install
```

### Check Python Version
```powershell
python --version
```
Should be 3.9, 3.10, or 3.11 (3.12+ not supported yet)

### Nuclear Option - Fresh Install
```powershell
Remove-Item poetry.lock
poetry install
```