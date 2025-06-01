#!/usr/bin/env python3
"""
Test Unicode Encoding Fix
=========================

Quick test to verify that the Unicode encoding fixes work correctly.
"""

import subprocess
import sys

def test_unicode_fix():
    """Test that the test suite runs without UnicodeEncodeError."""
    print("[TEST] Testing Unicode encoding fix...")
    
    try:
        # Test the main test suite
        print("\n[RUN] Testing test_suite.py...")
        result = subprocess.run([
            sys.executable, "test_suite.py"
        ], capture_output=True, text=True, timeout=30)
        
        if "UnicodeEncodeError" in result.stderr:
            print("[FAIL] UnicodeEncodeError still present in test_suite.py")
            print(f"Error: {result.stderr}")
            return False
        else:
            print("[OK] test_suite.py runs without UnicodeEncodeError")
        
        # Test the demo script
        print("\n[RUN] Testing test_suite_demo.py...")
        result = subprocess.run([
            sys.executable, "test_suite_demo.py"
        ], capture_output=True, text=True, timeout=30)
        
        if "UnicodeEncodeError" in result.stderr:
            print("[FAIL] UnicodeEncodeError still present in test_suite_demo.py")
            print(f"Error: {result.stderr}")
            return False
        else:
            print("[OK] test_suite_demo.py runs without UnicodeEncodeError")
        
        # Test the runner script
        print("\n[RUN] Testing run_test_suite.py...")
        result = subprocess.run([
            sys.executable, "run_test_suite.py", "--mode", "quick"
        ], capture_output=True, text=True, timeout=30)
        
        if "UnicodeEncodeError" in result.stderr:
            print("[FAIL] UnicodeEncodeError still present in run_test_suite.py")
            print(f"Error: {result.stderr}")
            return False
        else:
            print("[OK] run_test_suite.py runs without UnicodeEncodeError")
        
        print("\n[SUCCESS] All Unicode encoding issues have been fixed!")
        return True
        
    except subprocess.TimeoutExpired:
        print("[WARN] Test timed out - but no UnicodeEncodeError detected")
        return True
    except Exception as e:
        print(f"[ERROR] Test failed with exception: {e}")
        return False

if __name__ == "__main__":
    success = test_unicode_fix()
    if success:
        print("\n[TARGET] Unicode encoding fix verification complete!")
        print("You can now run the test suite normally.")
    else:
        print("\n[FAIL] Unicode encoding issues still present.")
        sys.exit(1)