# TEST SUITE README

A comprehensive testing framework for the Kimera SWM Toy Repository that addresses real issues while filtering out phantom errors and non-critical warnings.

## Overview

This test suite provides systematic testing for the Kimera project, focusing on:

- **Import validation** - Ensuring all modules can be imported correctly
- **Functionality testing** - Verifying core components work as expected
- **Integration testing** - Testing component interactions
- **Performance validation** - Ensuring acceptable performance characteristics

## Test Organization

### Directory Structure
```
tests/
├── unit/                    # Unit tests for individual modules
│   ├── test_identity.py     # Identity system tests
│   ├── test_storage.py      # Storage layer tests
│   └── test_entropy.py      # Entropy generation tests
├── integration/             # Integration tests
│   ├── test_cls_integration.py
│   ├── test_scar_functionality.py
│   └── test_vault_integration.py
├── functional/              # End-to-end tests
│   ├── test_cli_benchmark.py
│   └── test_migration_script.py
└── conftest.py             # Shared test fixtures
```

## Test Categories

### 1. Unit Tests
Test individual components in isolation:
- Identity creation and manipulation
- Storage operations
- Entropy generation
- Reactor functionality

### 2. Integration Tests
Test component interactions:
- CLS workflow integration
- Storage and identity integration
- Vault and SCAR operations
- Multiprocessing coordination

### 3. Functional Tests
Test complete workflows:
- CLI operations
- Migration scripts
- Benchmark execution
- End-to-end scenarios

## Running Tests

### Quick Test Run
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test category
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v
python -m pytest tests/functional/ -v
```

### Detailed Test Execution
```bash
# Run with coverage
python -m pytest tests/ --cov=src/kimera --cov-report=html

# Run specific test file
python -m pytest tests/unit/test_identity.py -v

# Run tests matching pattern
python -m pytest tests/ -k "test_storage" -v
```

### Test Fixtures

The test suite uses shared fixtures defined in `conftest.py`:

```python
@pytest.fixture
def fresh_duckdb_path():
    """Provide a clean DuckDB path for testing"""
    test_db = "test_kimera.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    yield test_db
    if os.path.exists(test_db):
        os.remove(test_db)

@pytest.fixture
def sample_identity():
    """Provide a sample identity for testing"""
    return Identity(
        content="test content",
        metadata={"test": True}
    )
```

## Test Validation Criteria

### Import Tests
- ✅ All modules import without errors
- ✅ No circular import dependencies
- ✅ Proper module initialization

### Functionality Tests
- ✅ Core operations work correctly
- ✅ Error handling functions properly
- ✅ Edge cases are handled

### Integration Tests
- ✅ Components work together correctly
- ✅ Data flows properly between modules
- ✅ Concurrent operations are safe

### Performance Tests
- ✅ Operations complete within acceptable time
- ✅ Memory usage stays within bounds
- ✅ Concurrent operations scale properly

## Test Data Management

### Test Databases
- Use temporary databases for testing
- Clean up test data after each test
- Isolate tests from each other

### Sample Data
- Provide consistent test data sets
- Use fixtures for reusable test data
- Mock external dependencies

## Continuous Integration

### GitHub Actions
The test suite integrates with GitHub Actions for automated testing:

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python -m pytest tests/ -v
```

## Test Maintenance

### Adding New Tests
1. Identify the appropriate test category (unit/integration/functional)
2. Create test file following naming convention `test_*.py`
3. Use appropriate fixtures and test patterns
4. Ensure tests are isolated and repeatable

### Test Quality Guidelines
- **Clear test names** that describe what is being tested
- **Isolated tests** that don't depend on other tests
- **Comprehensive coverage** of both success and failure cases
- **Fast execution** to enable frequent testing

### Debugging Failed Tests
```bash
# Run with verbose output
python -m pytest tests/test_failing.py -v -s

# Run with debugger
python -m pytest tests/test_failing.py --pdb

# Run with detailed output
python -m pytest tests/test_failing.py -vvv
```

## Performance Benchmarking

### Benchmark Tests
The test suite includes performance benchmarks:
- Storage operation timing
- Memory usage monitoring
- Concurrent operation scaling
- Large dataset handling

### Running Benchmarks
```bash
# Run performance tests
python -m pytest tests/functional/test_performance.py -v

# Generate performance report
python scripts/run_benchmark.py
```

## Test Reporting

### Coverage Reports
```bash
# Generate HTML coverage report
python -m pytest tests/ --cov=src/kimera --cov-report=html

# View coverage in terminal
python -m pytest tests/ --cov=src/kimera --cov-report=term
```

### Test Results
- All tests should pass in CI
- Coverage should be above 80%
- Performance tests should meet benchmarks
- No critical warnings or errors

## Troubleshooting

### Common Issues
1. **Import errors** - Check Python path and module structure
2. **Database conflicts** - Ensure test isolation and cleanup
3. **Timing issues** - Use appropriate timeouts and retries
4. **Resource leaks** - Verify proper cleanup in fixtures

### Debug Tools
```python
# Enable debug logging in tests
import logging
logging.basicConfig(level=logging.DEBUG)

# Use pytest debugging features
pytest.set_trace()  # Set breakpoint in test
```

The test suite provides comprehensive validation of the Kimera system and ensures reliable operation across all components.