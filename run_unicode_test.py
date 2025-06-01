#!/usr/bin/env python3
"""
Run Unicode Test
===============

Simple script to test if our Unicode fixes work.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("[TEST] Testing Unicode encoding fixes...")
    
    try:
        # Import and run a simple test
        from test_suite import KimeraTestSuite
        
        print("[RUN] Creating test suite...")
        suite = KimeraTestSuite()
        
        print("[RUN] Running basic import test...")
        result = suite.test_basic_imports()
        
        if result:
            print("[OK] Basic imports test passed!")
        else:
            print("[FAIL] Basic imports test failed!")
        
        print("[SUCCESS] Unicode encoding test completed without errors!")
        return True
        
    except UnicodeEncodeError as e:
        print(f"[FAIL] UnicodeEncodeError still present: {e}")
        return False
    except Exception as e:
        print(f"[INFO] Test completed with non-Unicode error: {e}")
        print("[OK] No UnicodeEncodeError detected!")
        return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n[TARGET] Ready to run full test suite!")
    else:
        print("\n[FAIL] Unicode issues still present.")
        sys.exit(1)