#!/usr/bin/env python3
"""
Simple test runner to check our fixes
"""
import sys
import os

# Add src to path
sys.path.insert(0, 'src')

from kimera.utils.safe_console import puts

def test_conftest():
    """Test conftest import"""
    puts("Testing conftest import...")
    try:
        from conftest import fresh_duckdb_path
        path = fresh_duckdb_path()
        puts(f"[PASS] conftest works, path: {path}")
        return True
    except Exception as e:
        puts(f"[FAIL] conftest failed: {e}")
        return False

def test_storage():
    """Test storage close"""
    puts("Testing storage close...")
    try:
        from kimera.storage import LatticeStorage
        from conftest import fresh_duckdb_path
        
        db_path = fresh_duckdb_path()
        storage = LatticeStorage(db_path)
        storage.close()
        
        if os.path.exists(db_path):
            os.remove(db_path)
        
        puts("[PASS] Storage close works")
        return True
    except Exception as e:
        puts(f"[FAIL] Storage test failed: {e}")
        return False

def test_echoform():
    """Test EchoForm add_term"""
    puts("Testing EchoForm add_term...")
    try:
        from kimera.echoform import EchoForm
        
        form = EchoForm("test")
        form.add_term("symbol1", role="test", intensity=1.0)
        form.add_term("symbol2", "test2", 0.5)  # legacy order
        
        puts(f"[PASS] EchoForm works, {len(form.terms)} terms")
        return True
    except Exception as e:
        puts(f"[FAIL] EchoForm test failed: {e}")
        return False

def test_reactor_mp():
    """Test reactor_mp import"""
    puts("Testing reactor_mp import...")
    try:
        from kimera import reactor_mp
        puts("[PASS] reactor_mp imports")
        return True
    except Exception as e:
        puts(f"[FAIL] reactor_mp failed: {e}")
        return False

def main():
    """Run all tests"""
    puts("[TEST] Simple Test Runner")
    puts("=" * 30)
    
    tests = [test_conftest, test_storage, test_echoform, test_reactor_mp]
    results = []
    
    for test in tests:
        success = test()
        results.append(success)
        puts("")
    
    passed = sum(results)
    total = len(results)
    
    puts(f"Results: {passed}/{total} passed")
    
    if passed == total:
        puts("[SUCCESS] All fixes working!")
    else:
        puts("[ERROR] Some fixes need work")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)