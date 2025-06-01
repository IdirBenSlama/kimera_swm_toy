#!/usr/bin/env python3
"""Run all tests to verify the import fixes."""

import subprocess
import sys
import os

def run_test(test_file):
    """Run a single test file."""
    print(f"🧪 Running {test_file}...")
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"  ✅ {test_file} passed")
            if result.stdout:
                print(f"     Output: {result.stdout.strip()}")
            return True
        else:
            print(f"  ❌ {test_file} failed")
            if result.stderr:
                print(f"     Error: {result.stderr.strip()}")
            if result.stdout:
                print(f"     Output: {result.stdout.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"  ⏰ {test_file} timed out")
        return False
    except Exception as e:
        print(f"  ❌ Error running {test_file}: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Running all tests to verify import fixes...\n")
    
    tests = [
        'test_import_fixes.py',
        'test_system_quick.py',
        'test_vault_and_scar.py'
    ]
    
    passed = 0
    for test in tests:
        if os.path.exists(test):
            if run_test(test):
                passed += 1
            print()
        else:
            print(f"⚠️  Test file {test} not found")
    
    print(f"📊 Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Import fixes are working correctly!")
        return True
    else:
        print("⚠️  Some tests failed - check the output above")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)