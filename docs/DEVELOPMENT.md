# Kimera Development Guide

## Overview

Kimera is a lattice-based semantic storage system that uses EchoForms to represent and store semantic relationships between concepts. This guide covers development practices, testing, and maintenance procedures.

## Project Structure

```
kimera/
├── src/kimera/           # Core library code
│   ├── echoform.py      # EchoForm data structure
│   ├── storage.py       # DuckDB persistent storage
│   ├── geoid.py         # Geographic/semantic identifiers
│   └── cls.py           # Core lattice system
├── tests/               # Test suite
├── scripts/             # Utility scripts
└── docs/               # Documentation
```

## Development Setup

### Prerequisites

- Python 3.8+
- DuckDB (installed via pip)
- pytest for testing
- hypothesis for property-based testing

### Installation

```bash
# Clone repository
git clone <repository-url>
cd kimera

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest hypothesis sentence-transformers
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_echoform.py

# Run with verbose output
pytest -v

# Run fuzz tests
python tests/fuzz_echoform.py
```

### Test Categories

1. **Unit Tests** (`tests/test_*.py`)
   - Test individual components
   - Fast execution
   - High coverage

2. **Integration Tests** (`tests/test_*_integration.py`)
   - Test component interactions
   - Database operations
   - End-to-end workflows

3. **Fuzz Tests** (`tests/fuzz_*.py`)
   - Property-based testing with Hypothesis
   - Random data generation
   - Edge case discovery

4. **Performance Tests** (`scripts/soak_*.py`)
   - Load testing
   - Performance benchmarking
   - Resource usage monitoring

### Precision Testing

The project uses `math.isclose()` for floating-point comparisons with appropriate tolerances:

```python
import math

# For intensity values (relative tolerance)
assert math.isclose(actual, expected, rel_tol=1e-9)

# For accumulated values (absolute tolerance)
assert math.isclose(actual, expected, abs_tol=1e-10)
```

## Storage System

### DuckDB Backend

Kimera uses DuckDB for persistent storage of EchoForms:

- **Database**: `kimera_lattice.db` (default)
- **Schema**: Single `echoforms` table with JSON blob storage
- **Indexes**: On `updated_at`, `domain` for performance

### Storage Metrics

The storage system includes built-in performance monitoring:

```python
from kimera.storage import get_storage_metrics, reset_storage_metrics

# Get current metrics
metrics = get_storage_metrics()
print(f"Store operations: {metrics['store_form_count']}")
print(f"Average store time: {metrics['store_form'] / metrics['store_form_count']:.3f}s")

# Reset metrics
reset_storage_metrics()
```

Tracked operations:
- `store_form`: EchoForm storage
- `fetch_form`: EchoForm retrieval
- `list_forms`: Form listing queries
- `get_form_count`: Count queries
- `prune_old_forms`: Cleanup operations
- `apply_time_decay`: Decay operations

## Performance Testing

### Soak Testing

Run extended load tests to verify system stability:

```bash
# Full soak test (100k operations)
python scripts/soak_lattice.py

# Quick test (500 operations)
python scripts/soak_lattice.py --dry-run

# Custom size
python scripts/soak_lattice.py --pairs 50000
```

The soak test measures:
- Text generation performance
- GeoID creation speed
- Lattice resolution throughput
- Database storage efficiency
- Memory usage patterns

### Performance Targets

- **Lattice Resolution**: >50 QPS for new forms, >100 QPS for cached forms
- **Storage**: <100 bytes per form on average
- **Memory**: Stable usage over extended runs

## Code Quality

### Style Guidelines

- Follow PEP 8 for Python code style
- Use type hints where appropriate
- Document public APIs with docstrings
- Keep functions focused and testable

### Unicode Safety

All text processing must be Unicode-safe:

```python
# Good: Explicit encoding
text.encode('utf-8')

# Good: Unicode normalization
import unicodedata
normalized = unicodedata.normalize('NFC', text)

# Avoid: Assuming ASCII
text.encode()  # May fail on Unicode
```

### Error Handling

- Use specific exception types
- Provide meaningful error messages
- Log errors with context
- Fail fast on configuration errors

## Continuous Integration

### GitHub Actions

The CI pipeline runs on every push and PR:

1. **Lint**: Code style checks
2. **Test**: Full test suite
3. **Coverage**: Test coverage reporting
4. **Performance**: Basic performance checks

### Local CI Simulation

```bash
# Run linting
flake8 src/ tests/

# Run tests with coverage
pytest --cov=kimera --cov-report=html

# Run performance checks
python scripts/soak_lattice.py --dry-run
```

## Debugging

### Common Issues

1. **DuckDB Lock Errors**
   - Ensure proper connection cleanup
   - Use context managers for transactions
   - Check for concurrent access

2. **Precision Errors**
   - Use `math.isclose()` for comparisons
   - Consider floating-point accumulation
   - Test with edge cases

3. **Memory Leaks**
   - Close database connections
   - Clear form caches periodically
   - Monitor long-running processes

### Debug Tools

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Storage metrics
from kimera.storage import get_storage_metrics
print(get_storage_metrics())

# Form inspection
form = storage.fetch_form("anchor")
print(f"Terms: {len(form.terms)}")
print(f"Intensity: {form.intensity_sum()}")
```

## Release Process

### Version Management

- Use semantic versioning (MAJOR.MINOR.PATCH)
- Update version in `pyproject.toml`
- Tag releases in git

### Pre-Release Checklist

1. ✅ All tests pass
2. ✅ Performance tests pass
3. ✅ Documentation updated
4. ✅ Dependencies locked
5. ✅ Unicode safety verified
6. ✅ CI pipeline green

### Hardening Checklist (0.7.x)

- [x] **Dependency Locking**: DuckDB pinned in pyproject.toml
- [x] **Precision Tests**: Using math.isclose() with proper tolerances
- [x] **Unicode Safety**: No unsafe Unicode operations found
- [x] **Fuzz Tests**: Hypothesis-based testing for EchoForm
- [x] **Soak Tests**: Load testing for lattice storage
- [x] **Metrics Hook**: Storage performance monitoring
- [x] **CI Hardening**: Fixed duplicate configuration
- [x] **Documentation**: Development guide created

## Contributing

### Pull Request Process

1. Create feature branch from `main`
2. Implement changes with tests
3. Run full test suite locally
4. Update documentation if needed
5. Submit PR with clear description

### Code Review

- Focus on correctness and performance
- Verify test coverage
- Check for Unicode safety
- Review error handling
- Validate documentation

## Troubleshooting

### Common Commands

```bash
# Reset development environment
rm -f kimera_lattice.db *.db
pip install -e .

# Run specific test category
pytest tests/test_storage.py -v

# Performance profiling
python -m cProfile scripts/soak_lattice.py --dry-run

# Database inspection
sqlite3 kimera_lattice.db ".schema"
```

### Getting Help

- Check existing tests for usage examples
- Review docstrings in source code
- Run soak tests to verify system health
- Check CI logs for detailed error information

---

*Last updated: 0.7.x hardening sprint*