#!/usr/bin/env python3
"""
Validate the current state of the codebase
"""
import sys
import os
sys.path.insert(0, 'src')

def run_test_file(test_file):
    """Run a test file and return success status"""
    try:
        print(f"\n=== Running {test_file} ===")
        with open(test_file, 'r') as f:
            code = f.read()
        
        # Execute the test file
        exec(code, {'__name__': '__main__'})
        return True
    except Exception as e:
        print(f"[FAIL] {test_file} failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main validation function"""
    print("=== Validating Current State ===")
    
    # Test files to run
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
    print(f"\n=== Validation Results ===")
    passed = 0
    total = 0
    for test_file, success in results.items():
        status = "PASS" if success else "FAIL"
        print(f"{status}: {test_file}")
        if success:
            passed += 1
        total += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("[PASS] All tests passed!")
        return True
    else:
        print("[FAIL] Some tests failed")
        return False

if __name__ == "__main__":
    main()