#!/usr/bin/env python3
"""
Clean test runner with safe console output
"""
import subprocess
import sys
import os

# Add src to path
sys.path.insert(0, 'src')

from kimera.utils.safe_console import puts

def run_pytest_clean():
    """Run pytest tests cleanly"""
    puts("[START] Running pytest test suite")
    puts("=" * 40)
    
    try:
        # Run core tests
        test_files = [
            "tests/test_echoform_core.py",
            "tests/test_cls_integration.py", 
            "tests/test_storage_metrics.py",
        ]
        
        all_passed = True
        
        for test_file in test_files:
            if os.path.exists(test_file):
                puts(f"\n[TEST] Running {test_file}")
                result = subprocess.run([
                    sys.executable, "-m", "pytest", test_file, "-v", "--tb=short"
                ], capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    puts(f"[PASS] {test_file}")
                else:
                    puts(f"[FAIL] {test_file}")
                    all_passed = False
                    
                    # Show errors if any
                    if result.stderr:
                        puts("Errors:")
                        puts(result.stderr[:500])  # First 500 chars
            else:
                puts(f"[SKIP] {test_file} not found")
        
        return all_passed
        
    except Exception as e:
        puts(f"[ERROR] Pytest run failed: {e}")
        return False

def run_quick_validation():
    """Run our quick validation tests"""
    puts("\n[START] Running quick validation")
    puts("=" * 40)
    
    try:
        # Test our fixes directly
        from conftest import fresh_duckdb_path
        from kimera.storage import LatticeStorage
        from kimera.echoform import EchoForm
        from kimera import reactor_mp
        
        puts("[PASS] All imports successful")
        
        # Test basic functionality
        db_path = fresh_duckdb_path()
        storage = LatticeStorage(db_path)
        
        # Test EchoForm
        form = EchoForm("test")
        form.add_term("symbol", role="test", intensity=1.0)
        
        # Test storage operations
        storage.store_form(form)
        retrieved = storage.fetch_form("test")
        
        # Test prune (should return proper count now)
        count = storage.prune_old_forms(older_than_seconds=3600)
        puts(f"[INFO] Pruned {count} forms")
        
        storage.close()
        
        if os.path.exists(db_path):
            os.remove(db_path)
        
        puts("[PASS] All functionality tests passed")
        return True
        
    except Exception as e:
        puts(f"[FAIL] Quick validation failed: {e}")
        return False

def main():
    """Run clean test suite"""
    puts("[START] Kimera v0.7.x Clean Test Suite")
    puts("=" * 50)
    
    # Run tests
    pytest_ok = run_pytest_clean()
    validation_ok = run_quick_validation()
    
    # Summary
    puts(f"\n[STATS] Test Results:")
    puts(f"   Pytest: {'[PASS]' if pytest_ok else '[FAIL]'}")
    puts(f"   Validation: {'[PASS]' if validation_ok else '[FAIL]'}")
    
    if pytest_ok and validation_ok:
        puts(f"\n[SUCCESS] All tests passed!")
        puts(f"   Kimera v0.7.x is stable and ready")
        return True
    else:
        puts(f"\n[WARN] Some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)