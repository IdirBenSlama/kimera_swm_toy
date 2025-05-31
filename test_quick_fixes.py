#!/usr/bin/env python3
"""
Quick test to verify the v0.7.x stabilization fixes
"""
import sys
import os
sys.path.insert(0, 'src')

from kimera.utils.safe_console import puts

def test_conftest_import():
    """Test that conftest.py can be imported from root"""
    puts("Testing conftest import...")
    try:
        from conftest import fresh_duckdb_path
        path = fresh_duckdb_path()
        puts(f"[PASS] conftest import works, got path: {path}")
        return True
    except Exception as e:
        puts(f"[FAIL] conftest import failed: {e}")
        return False

def test_storage_close():
    """Test that storage.close() works properly"""
    puts("Testing storage close...")
    try:
        from kimera.storage import LatticeStorage
        from conftest import fresh_duckdb_path
        
        db_path = fresh_duckdb_path()
        storage = LatticeStorage(db_path)
        storage.close()
        
        # Try to remove the file (should work now)
        if os.path.exists(db_path):
            os.remove(db_path)
        
        puts("[PASS] Storage close and file removal works")
        return True
    except Exception as e:
        puts(f"[FAIL] Storage close test failed: {e}")
        return False

def test_echoform_add_term():
    """Test that EchoForm.add_term backward compatibility works"""
    puts("Testing EchoForm add_term...")
    try:
        from kimera.echoform import EchoForm
        
        form = EchoForm("test")
        
        # Test new signature
        form.add_term("symbol1", role="test_role", intensity=1.0)
        
        # Test backward compatibility (legacy order)
        form.add_term("symbol2", "test_role2", 0.5)
        
        puts(f"[PASS] EchoForm add_term works, form has {len(form.terms)} terms")
        return True
    except Exception as e:
        puts(f"[FAIL] EchoForm add_term test failed: {e}")
        return False

def test_prune_old_forms():
    """Test that prune_old_forms dual parameters work"""
    puts("Testing prune_old_forms...")
    try:
        from kimera.storage import LatticeStorage
        from conftest import fresh_duckdb_path
        
        db_path = fresh_duckdb_path()
        storage = LatticeStorage(db_path)
        
        # Test both parameter styles
        count1 = storage.prune_old_forms(older_than_seconds=3600)
        count2 = storage.prune_old_forms(older_than_days=1)
        
        storage.close()
        if os.path.exists(db_path):
            os.remove(db_path)
        
        puts(f"[PASS] prune_old_forms works, deleted {count1}, {count2} forms")
        return True
    except Exception as e:
        puts(f"[FAIL] prune_old_forms test failed: {e}")
        return False

def test_multiprocessing_guard():
    """Test that multiprocessing guard is in place"""
    puts("Testing multiprocessing guard...")
    try:
        from kimera import reactor_mp
        puts("[PASS] reactor_mp imports without error")
        return True
    except Exception as e:
        puts(f"[FAIL] reactor_mp import failed: {e}")
        return False

def main():
    """Run all quick fix tests"""
    puts("[TEST] Quick Fixes Validation")
    puts("=" * 30)
    
    tests = [
        test_conftest_import,
        test_storage_close,
        test_echoform_add_term,
        test_prune_old_forms,
        test_multiprocessing_guard,
    ]
    
    results = []
    for test in tests:
        success = test()
        results.append(success)
        puts("")
    
    passed = sum(results)
    total = len(results)
    
    puts(f"[STATS] Results: {passed}/{total} tests passed")
    
    if passed == total:
        puts("[SUCCESS] All quick fixes are working!")
        return True
    else:
        puts("[ERROR] Some fixes need more work.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)