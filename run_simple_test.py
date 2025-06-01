#!/usr/bin/env python3
"""
Run a simple test to check current functionality
"""
import sys
import os
sys.path.insert(0, 'src')

def run_echoform_test():
    """Run the EchoForm test"""
    try:
        print("=== Running EchoForm Test ===")
        exec(open('tests/unit/test_echoform_core.py').read())
        return True
    except Exception as e:
        print(f"EchoForm test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_identity_test():
    """Run the Identity test"""
    try:
        print("\n=== Running Identity Test ===")
        exec(open('tests/unit/test_identity.py').read())
        return True
    except Exception as e:
        print(f"Identity test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== Running Simple Tests ===")
    
    echoform_ok = run_echoform_test()
    identity_ok = run_identity_test()
    
    print(f"\n=== Results ===")
    print(f"EchoForm: {'PASS' if echoform_ok else 'FAIL'}")
    print(f"Identity: {'PASS' if identity_ok else 'FAIL'}")
    
    if echoform_ok and identity_ok:
        print("\n[PASS] All tests passed!")
    else:
        print("\n[FAIL] Some tests failed")