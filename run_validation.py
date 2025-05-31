#!/usr/bin/env python3
"""
Run validation to see the exact error
"""
import subprocess
import sys

def run_validation():
    """Run the validation script and capture output"""
    try:
        result = subprocess.run([sys.executable, "validate_v071.py"], 
                              capture_output=True, text=True, timeout=60)
        
        print("STDOUT:")
        print(result.stdout)
        print("\nSTDERR:")
        print(result.stderr)
        print(f"\nReturn code: {result.returncode}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running validation: {e}")
        return False

if __name__ == "__main__":
    run_validation()