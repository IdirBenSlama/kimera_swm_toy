#!/usr/bin/env python3
"""
Runner for simple identity test
"""

import subprocess
import sys

def main():
    """Run the simple identity test"""
    try:
        result = subprocess.run([
            sys.executable, "simple_identity_test.py"
        ], capture_output=True, text=True, timeout=30)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"Return code: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ Test completed successfully!")
        else:
            print("❌ Test failed!")
            
    except subprocess.TimeoutExpired:
        print("❌ Test timed out!")
    except Exception as e:
        print(f"❌ Error running test: {e}")

if __name__ == "__main__":
    main()