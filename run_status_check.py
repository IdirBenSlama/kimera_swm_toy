#!/usr/bin/env python3
"""
Run the status check and capture output
"""
import subprocess
import sys

def main():
    """Run the status check"""
    try:
        print("Running comprehensive status check...")
        result = subprocess.run([sys.executable, 'test_suite_status.py'], 
                              capture_output=True, text=True, timeout=60)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)
        
        print(f"\nReturn code: {result.returncode}")
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("Status check timed out")
        return False
    except Exception as e:
        print(f"Error running status check: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)