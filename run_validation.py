#!/usr/bin/env python3
"""
Run the validation script and capture output
"""
import subprocess
import sys

def main():
    try:
        result = subprocess.run([sys.executable, "test_final_fixes.py"], 
                              capture_output=True, text=True, timeout=60)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)
        
        print(f"\nReturn code: {result.returncode}")
        
    except subprocess.TimeoutExpired:
        print("Validation script timed out")
    except Exception as e:
        print(f"Error running validation: {e}")

if __name__ == "__main__":
    main()