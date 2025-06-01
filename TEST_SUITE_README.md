# Kimera Test Suite

A comprehensive testing framework for the Kimera SWM Toy Repository that addresses real issues while filtering out phantom errors and non-critical warnings.

## Overview

This test suite provides systematic testing for the Kimera project, focusing on:

- **Import validation** - Ensuring all modules can be imported correctly
- **Functionality testing** - Verifying core components work as expected  
- **System testing** - Checking file structure and configuration
- **Integration testing** - Testing component interactions
- **CI validation** - Ensuring CI configuration is correct

## Quick Start

### Run All Tests
```bash
python run_test_suite.py --mode full
```

### Run Quick Tests Only
```bash
python run_test_suite.py --mode quick
```

### Simulate CI Environment
```bash
python run_test_suite.py --mode ci
```

### Check Environment
```bash
python run_test_suite.py --mode env
```

## Test Files

### Main Test Suite
- **`test_suite.py`** - Comprehensive test suite with all test categories
- **`run_test_suite.py`** - Test runner with multiple modes and utilities
- **`test_config.py`** - Configuration and constants for the test suite

### Legacy Test Files (if present)
- **`test_import_fixes.py`** - Import validation tests
- **`test_system_quick.py`** - Quick system tests
- **`test_vault_and_scar.py`** - Vault and SCAR functionality tests
- **`basic_import_test.py`** - Basic import verification

## Test Categories

### 📦 Import Tests
- **Basic Python Imports** - Standard library imports
- **Kimera Core Imports** - Core Kimera module imports
- **Vault Imports** - Vault module imports

### ⚙️ Functionality Tests  
- **Identity Creation** - Test identity creation functionality
- **Storage Functionality** - Test storage operations
- **Vault Functionality** - Test vault operations

### 🏗️ System Tests
- **File Structure** - Verify required files exist
- **Python Syntax** - Check syntax of core files
- **CI Configuration** - Validate CI YAML configuration

### 🔗 Integration Tests
- **End-to-End Workflow** - Test complete workflows
- **Module Compatibility** - Test module interactions

## Understanding Test Results

### Status Indicators
- ✅ **PASSED** - Test completed successfully
- ❌ **FAILED** - Test failed with an error
- ⏭️ **SKIPPED** - Test was skipped (with reason)
- 💥 **ERROR** - Test encountered an unexpected error
- ⏰ **TIMEOUT** - Test exceeded time limit

### Common Issues and Solutions

#### Import Errors
If you see import errors:
1. Check that you're running from the repository root
2. Verify the `src/` directory structure is correct
3. Ensure `__init__.py` files exist in module directories

#### Missing Files
If tests report missing files:
1. Check the repository structure matches expectations
2. Verify you have the complete repository checkout
3. Check if files were moved or renamed

#### CI Configuration Issues
If CI tests fail:
1. Verify `.github/workflows/ci.yml` exists and is valid YAML
2. Check that referenced test files exist
3. Ensure CI steps match available test scripts

## Ignoring Non-Critical Issues

The test suite is configured to ignore known non-critical issues:

### Phantom Errors
- References to non-existent CI files (`ci_new.yml`, `ci_clean.yml`, etc.)
- These are VSCode/editor artifacts and can be safely ignored

### Spelling Warnings
- Project-specific terms: "Kimera", "echoform", "duckdb"
- Technical terms: "ndarray", "isinstance", "conftest"
- These are expected and don't indicate real problems

### Markdown Formatting
- Missing blank lines around headings (MD022)
- Missing language specifications for code blocks (MD040)
- These are style issues, not functional problems

## Configuration

### Test Timeouts
- Quick tests: 30 seconds
- Integration tests: 60 seconds  
- Full test suite: 120 seconds

### Required Structure
The test suite expects this directory structure:
```
.
├── src/
│   └── kimera/
│       ├── __init__.py
│       ├── identity.py
│       ├── storage.py
│       └── reactor_mp.py
├── vault/
│   ├── __init__.py
│   └── core/
│       ├── __init__.py
│       └── vault.py
├── .github/
│   └── workflows/
│       └── ci.yml
└── test files...
```

## Advanced Usage

### Custom Test Configuration
Edit `test_config.py` to modify:
- Timeout values
- Required files and directories
- Ignore patterns for known issues
- Critical error patterns

### Adding New Tests
To add new tests to the main suite:

1. Add test methods to the appropriate test class in `test_suite.py`
2. Register the test in the `main()` function
3. Update `test_config.py` if needed

### Running Individual Test Categories
You can run specific test categories by modifying `test_suite.py` or creating custom test runners.

## Troubleshooting

### Common Problems

**"Module not found" errors**
- Ensure you're running from the repository root
- Check that `src/` is in the Python path
- Verify module structure is correct

**"File not found" errors**  
- Check that all required files exist
- Verify file paths in configuration
- Ensure proper repository checkout

**Timeout errors**
- Increase timeout values in `test_config.py`
- Check for infinite loops or blocking operations
- Verify test environment performance

### Getting Help

1. Run environment check: `python run_test_suite.py --mode env`
2. Check the test configuration in `test_config.py`
3. Review the detailed output from failed tests
4. Verify the repository structure matches expectations

## Integration with CI

The test suite is designed to work with the existing CI configuration. The CI workflow runs:

1. `test_import_fixes.py` - Import validation
2. `test_system_quick.py` - Quick system tests  
3. `test_vault_and_scar.py` - Vault and SCAR tests

You can simulate the CI environment locally:
```bash
python run_test_suite.py --mode ci
```

## Best Practices

1. **Run tests before committing** - Use quick mode for fast feedback
2. **Use full mode for releases** - Comprehensive testing before major changes
3. **Check environment first** - Verify setup before running tests
4. **Focus on real issues** - Ignore phantom errors and non-critical warnings
5. **Update tests with code changes** - Keep tests current with functionality

## Contributing

When adding new functionality:
1. Add corresponding tests to the appropriate category
2. Update `test_config.py` if new modules or files are required
3. Ensure tests pass in all modes
4. Document any new test patterns or configurations