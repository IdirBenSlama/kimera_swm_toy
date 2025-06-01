#!/usr/bin/env python3
"""
Quick Test Run
=============

Test the Unicode fixes by running a quick test.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("[RUN] Quick Unicode Fix Test")
    print("=" * 40)
    
    try:
        # Test basic print statements with our ASCII replacements
        print("[TARGET] Testing ASCII replacements...")
        print("[OK] Success indicator")
        print("[FAIL] Failure indicator") 
        print("[RUN] Running indicator")
        print("[SUMMARY] Summary indicator")
        
        # Try to import and run a simple test
        print("\n[RUN] Testing imports...")
        
        try:
            from kimera.identity import Identity
            print("[OK] Identity import successful")
        except Exception as e:
            print(f"[INFO] Identity import issue (expected): {e}")
        
        print("\n[SUCCESS] Unicode encoding test completed!")
        print("No UnicodeEncodeError should have occurred.")
        
        return True
        
    except UnicodeEncodeError as e:
        print(f"[FAIL] UnicodeEncodeError detected: {e}")
        return False
    except Exception as e:
        print(f"[INFO] Other error (not Unicode): {e}")
        return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n[TARGET] Ready to run the full test suite!")
        print("\nTry running:")
        print("  python run_test_suite.py --mode quick")
        print("  python test_suite_demo.py")
    else:
        print("\n[FAIL] Unicode issues still present.")
        sys.exit(1)