# Test Suite Documentation

## Overview

The Kimera SWM test suite provides comprehensive coverage of all system components with unit, integration, and functional tests.

## Test Structure

### Unit Tests (`tests/unit/`)

#### `test_identity.py`
- **Purpose**: Test SCAR identity generation and validation
- **Coverage**: Identity class methods, hash stability, collision handling
- **Key Tests**:
  - SCAR generation consistency
  - Hash stability across runs
  - Content normalization
  - Error handling

#### `test_storage.py`
- **Purpose**: Test storage layer operations
- **Coverage**: DuckDB operations, metrics collection, query optimization
- **Key Tests**:
  - Database connection management
  - CRUD operations
  - Query performance
  - Metrics tracking

#### `test_echoform_core.py`
- **Purpose**: Test EchoForm core functionality
- **Coverage**: Memory management, observability, error handling
- **Key Tests**:
  - Memory optimization
  - Performance monitoring
  - Error recovery
  - Resource cleanup

### Integration Tests (`tests/integration/`)

#### `test_cls_integration.py`
- **Purpose**: Test CLS system integration
- **Coverage**: Lattice storage, time-decay weighting, SCAR integration
- **Key Tests**:
  - End-to-end CLS workflow
  - SCAR-based storage
  - Time decay calculations
  - Performance benchmarks

#### `test_scar_functionality.py`
- **Purpose**: Test SCAR system integration
- **Coverage**: Cross-system SCAR usage, relationship tracking
- **Key Tests**:
  - SCAR generation and storage
  - Cross-reference validation
  - Relationship queries
  - System integration

### Functional Tests (`tests/functional/`)

#### End-to-End Scenarios
- **Purpose**: Test complete system workflows
- **Coverage**: Real-world usage patterns
- **Key Tests**:
  - Full data processing pipeline
  - Multi-component interactions
  - Performance under load
  - Error recovery scenarios

## Test Execution

### Running All Tests
```bash
# Run complete test suite
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src/kimera --cov-report=html

# Run specific test categories
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v
python -m pytest tests/functional/ -v
```

### Running Individual Tests
```bash
# Run specific test file
python -m pytest tests/unit/test_identity.py -v

# Run specific test method
python -m pytest tests/unit/test_identity.py::test_scar_generation -v

# Run with detailed output
python -m pytest tests/unit/test_identity.py -v -s
```

### Test Configuration
```bash
# Run with specific markers
python -m pytest -m "not slow" tests/

# Run with parallel execution
python -m pytest -n auto tests/

# Run with specific verbosity
python -m pytest tests/ -v --tb=short
```

## Test Data and Fixtures

### Fixtures (`conftest.py`)
- **Database fixtures**: Temporary test databases
- **Sample data**: Consistent test data across tests
- **Mock objects**: Isolated component testing
- **Configuration**: Test-specific settings

### Test Data Management
- **Isolation**: Each test uses fresh data
- **Cleanup**: Automatic cleanup after tests
- **Consistency**: Reproducible test conditions
- **Performance**: Optimized test data loading

## Performance Testing

### Benchmarks
- **SCAR Generation**: < 10ms per operation
- **Storage Operations**: < 100ms per query
- **Memory Usage**: < 1GB for test datasets
- **Test Execution**: < 30 seconds full suite

### Load Testing
- **Concurrent Operations**: Multi-threaded testing
- **Large Datasets**: Scalability verification
- **Memory Pressure**: Resource limit testing
- **Long-Running**: Stability over time

## Test Quality Metrics

### Coverage Targets
- **Line Coverage**: > 95%
- **Branch Coverage**: > 90%
- **Function Coverage**: 100%
- **Class Coverage**: 100%

### Quality Gates
- **All Tests Pass**: 100% success rate
- **No Flaky Tests**: Consistent results
- **Fast Execution**: < 30 seconds
- **Clear Failures**: Descriptive error messages

## Continuous Integration

### CI Pipeline
- **Automated Execution**: On every commit
- **Multiple Environments**: Python 3.8, 3.9, 3.10, 3.11
- **Coverage Reporting**: Automatic coverage analysis
- **Failure Notifications**: Immediate feedback

### Quality Checks
- **Static Analysis**: Code quality verification
- **Security Scanning**: Vulnerability detection
- **Performance Regression**: Benchmark comparison
- **Documentation**: Test documentation updates

## Test Development Guidelines

### Writing New Tests
1. **Follow AAA Pattern**: Arrange, Act, Assert
2. **Use Descriptive Names**: Clear test purpose
3. **Single Responsibility**: One concept per test
4. **Proper Fixtures**: Reusable test setup
5. **Good Coverage**: Test edge cases

### Test Maintenance
- **Regular Review**: Keep tests current
- **Refactor When Needed**: Maintain clarity
- **Update Documentation**: Keep guides current
- **Monitor Performance**: Watch test execution time

## Debugging Tests

### Common Issues
- **Import Errors**: Check module paths
- **Database Issues**: Verify test database setup
- **Timing Issues**: Use proper synchronization
- **Resource Cleanup**: Ensure proper teardown

### Debugging Tools
```bash
# Run with debugger
python -m pytest tests/unit/test_identity.py --pdb

# Verbose output
python -m pytest tests/ -v -s

# Show local variables on failure
python -m pytest tests/ --tb=long

# Run specific failing test
python -m pytest tests/unit/test_identity.py::test_failing_case -v
```

## Test Environment Setup

### Dependencies
```bash
# Install test dependencies
pip install pytest pytest-cov pytest-mock pytest-xdist

# Install development dependencies
pip install -e .[dev]
```

### Configuration Files
- **`pytest.ini`**: Pytest configuration
- **`conftest.py`**: Shared fixtures
- **`.coveragerc`**: Coverage configuration
- **`tox.ini`**: Multi-environment testing

### Environment Variables
```bash
# Test database configuration
export KIMERA_TEST_DB_PATH="./test_data/test.db"
export KIMERA_TEST_LOG_LEVEL="DEBUG"
export KIMERA_TEST_TIMEOUT="30"
```

## Test Results and Reporting

### Coverage Reports
- **HTML Report**: Detailed coverage analysis
- **Console Output**: Quick coverage summary
- **CI Integration**: Automated coverage tracking
- **Trend Analysis**: Coverage over time

### Test Reports
- **JUnit XML**: CI/CD integration
- **HTML Reports**: Detailed test results
- **Performance Reports**: Benchmark tracking
- **Failure Analysis**: Error categorization

## Conclusion

The Kimera SWM test suite provides comprehensive, reliable testing that ensures system quality and stability. With automated execution, detailed reporting, and continuous monitoring, the test suite supports confident development and deployment.

**Key Benefits:**
- ✅ Comprehensive coverage across all components
- ✅ Fast, reliable execution
- ✅ Clear failure reporting
- ✅ Automated CI/CD integration
- ✅ Performance monitoring
- ✅ Quality assurance

The test suite is an integral part of the development process, providing confidence in system reliability and supporting rapid, safe iteration.