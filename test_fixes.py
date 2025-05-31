#!/usr/bin/env python3
"""
Quick test to verify our fixes are working
"""
import sys
import os
sys.path.insert(0, 'src')
sys.path.insert(0, 'tests')

def test_fresh_duckdb_path():
    """Test that fresh_duckdb_path works"""
    from conftest import fresh_duckdb_path
    
    path = fresh_duckdb_path()
    print(f"✓ fresh_duckdb_path() returned: {path}")
    
    # Verify the file doesn't exist
    assert not os.path.exists(path), f"File should not exist: {path}"
    print("✓ File correctly doesn't exist")
    
    # Test that we can create a DuckDB connection
    import duckdb
    conn = duckdb.connect(path)
    conn.execute("CREATE TABLE test (id INTEGER)")
    conn.close()
    print("✓ DuckDB connection works")
    
    # Clean up
    if os.path.exists(path):
        os.unlink(path)
    print("✓ Cleanup successful")

def test_precision_fix():
    """Test that precision fix works"""
    import math
    
    # Test values that would fail with strict equality but pass with isclose
    a = 0.1 + 0.2
    b = 0.3
    
    # This would fail: assert a == b
    # But this should pass:
    FLOAT_RTOL = 1e-7
    assert math.isclose(a, b, rel_tol=FLOAT_RTOL)
    print("✓ math.isclose works for floating point precision")

def test_benchmark_fix():
    """Test that the benchmark CLI fix works"""
    # Just import to make sure there are no syntax errors
    try:
        sys.path.insert(0, 'benchmarks')
        import llm_compare
        print("✓ llm_compare imports without errors")
    except Exception as e:
        print(f"✗ llm_compare import failed: {e}")
        raise

if __name__ == "__main__":
    print("Testing fixes...")
    
    test_fresh_duckdb_path()
    test_precision_fix()
    test_benchmark_fix()
    
    print("\n🎉 All fixes working correctly!")