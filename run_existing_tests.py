#!/usr/bin/env python3
"""
Run existing unit tests
"""
import sys
import os
sys.path.insert(0, 'src')

def run_test_file(test_file):
    """Run a test file and capture results"""
    print(f"\n=== Running {test_file} ===")
    try:
        # Read and execute the test file
        with open(test_file, 'r') as f:
            code = f.read()
        
        # Create a clean namespace for the test
        test_globals = {
            '__name__': '__main__',
            '__file__': test_file
        }
        
        exec(code, test_globals)
        print(f"[PASS] {test_file} completed successfully")
        return True
    except Exception as e:
        print(f"[FAIL] {test_file} failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test runner"""
    print("=== Running Existing Unit Tests ===")
    
    test_files = [
        'tests/unit/test_echoform_core.py',
        'tests/unit/test_identity.py'
    ]
    
    results = {}
    for test_file in test_files:
        if os.path.exists(test_file):
            results[test_file] = run_test_file(test_file)
        else:
            print(f"[SKIP] {test_file} not found")
            results[test_file] = False
    
    # Summary
    print(f"\n=== Test Results ===")
    passed = sum(1 for success in results.values() if success)
    total = len(results)
    
    for test_file, success in results.items():
        status = "PASS" if success else "FAIL"
        print(f"{status}: {test_file}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[PASS] All tests passed!")
        return True
    else:
        print("\n[FAIL] Some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)