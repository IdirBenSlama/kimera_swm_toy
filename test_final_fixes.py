#!/usr/bin/env python3
"""
Test the final fixes we just applied
"""
import sys
import os

# Add src to path
sys.path.insert(0, 'src')

def test_safe_console():
    """Test that safe console works"""
    print("Testing safe console...")
    try:
        from kimera.utils.safe_console import puts
        puts("[TEST] Safe console test with emojis: 🚀 ✅ ❌")
        puts("[PASS] Safe console works")
        return True
    except Exception as e:
        print(f"[FAIL] Safe console failed: {e}")
        return False

def test_storage_rowcount():
    """Test that storage returns proper row counts"""
    print("Testing storage row count...")
    try:
        from kimera.utils.safe_console import puts
        from conftest import fresh_duckdb_path
        from kimera.storage import LatticeStorage
        from kimera.echoform import EchoForm
        
        db_path = fresh_duckdb_path()
        storage = LatticeStorage(db_path)
        
        # Add some forms
        for i in range(3):
            form = EchoForm(f"test_{i}")
            form.add_term(f"symbol_{i}", role="test", intensity=1.0)
            storage.store_form(form)
        
        # Test prune (should return proper count, not -1)
        count = storage.prune_old_forms(older_than_seconds=3600)
        
        storage.close()
        if os.path.exists(db_path):
            os.remove(db_path)
        
        puts(f"[PASS] Storage row count works, deleted {count} forms")
        return count >= 0  # Should not be -1
        
    except Exception as e:
        print(f"[FAIL] Storage row count test failed: {e}")
        return False

def test_imports():
    """Test all critical imports"""
    print("Testing imports...")
    try:
        from kimera.utils.safe_console import puts
        
        # Test all critical imports
        from conftest import fresh_duckdb_path
        from kimera.storage import LatticeStorage
        from kimera.echoform import EchoForm
        from kimera import reactor_mp
        
        puts("[PASS] All imports successful")
        return True
    except Exception as e:
        print(f"[FAIL] Import test failed: {e}")
        return False

def main():
    """Run final fix tests"""
    print("=" * 50)
    print("FINAL FIXES TEST")
    print("=" * 50)
    
    tests = [
        test_safe_console,
        test_storage_rowcount,
        test_imports,
    ]
    
    results = []
    for test in tests:
        success = test()
        results.append(success)
        print()
    
    passed = sum(results)
    total = len(results)
    
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("[SUCCESS] All final fixes working!")
        return True
    else:
        print("[ERROR] Some final fixes need work")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)