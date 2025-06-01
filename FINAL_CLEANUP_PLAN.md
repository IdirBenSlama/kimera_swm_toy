# Final Repository Cleanup Plan

## Current Situation
The root directory still contains ~100+ files that should be organized:
- 50+ markdown status/summary files
- 30+ Python test files  
- 20+ Python utility scripts
- Various other development artifacts

## Cleanup Actions

### 1. Markdown Files
**Move to `docs/ARCHIVE/`:**
- All `*_STATUS*.md` files
- All `*_SUMMARY*.md` files
- All `*_COMPLETE*.md` files
- All `*_FIXES*.md` files
- All phase and implementation tracking files

**Move to `docs/`:**
- `SCAR_IMPLEMENTATION_GUIDE.md`
- `TEST_SUITE_README.md`
- `ASYNC_IMPLEMENTATION.md`

**Keep in root:**
- `README.md`
- `CHANGELOG.md`

### 2. Python Test Files
**Move to `tests/unit/`:**
- `test_basic_*.py`
- `test_simple_*.py`
- Individual module tests

**Move to `tests/integration/`:**
- `test_*_integration.py`
- `test_p0_*.py`
- `test_scar_*.py`
- `test_storage_*.py`

**Move to `tests/functional/`:**
- `test_suite*.py`
- End-to-end test files

### 3. Python Utility Scripts
**Move to `scripts/`:**
- All `run_*.py` files
- All `check_*.py` files
- All `fix_*.py` files
- All `verify_*.py` files
- All `validate_*.py` files
- All `setup_*.py` files
- All `demo_*.py` files
- All `execute_*.py` files
- All `quick_*.py` files

### 4. Keep in Root
**Essential files only:**
- `README.md`
- `CHANGELOG.md`
- `pyproject.toml`
- `poetry.lock`
- `conftest.py`

## Expected Result

```
kimera_swm_toy/
├── README.md                    # ✅ Main documentation
├── CHANGELOG.md                 # ✅ Version history
├── pyproject.toml              # ✅ Package config
├── poetry.lock                 # ✅ Dependencies
├── conftest.py                 # ✅ Test configuration
├── src/kimera/                 # ✅ Source code
├── tests/                      # ✅ Organized tests
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── functional/             # Functional tests
├── docs/                       # ✅ Documentation
│   ├── *.md                    # Implementation guides
│   └── ARCHIVE/                # Historical documents
├── scripts/                    # ✅ Utility scripts
├── vault/                      # ✅ Vault subsystem
└── .github/workflows/          # ✅ CI configuration
```

## Benefits
- **Clean root directory** - Only essential files visible
- **Organized development** - Clear separation of concerns
- **Easy navigation** - Logical file organization
- **Maintainable structure** - Scalable for future growth
- **Professional appearance** - Clean, organized repository

## Execution
Run the cleanup script:
```bash
python scripts/final_root_cleanup.py
```

This will automatically organize all files according to the plan above.