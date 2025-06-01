#!/usr/bin/env python3
"""
Run the final test to verify all fixes are working.
"""

import subprocess
import sys

def run_test():
    """Run the final status test."""
    print("🚀 Running final status test...")
    try:
        result = subprocess.run([sys.executable, "test_final_status.py"], 
                              capture_output=True, text=True, timeout=30)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"Return code: {result.returncode}")
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ Test timed out")
        return False
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        return False

if __name__ == "__main__":
    success = run_test()
    if success:
        print("🎉 Final test passed!")
    else:
        print("❌ Final test failed!")
    sys.exit(0 if success else 1)