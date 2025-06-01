#!/usr/bin/env python3
"""Run status check and show results."""

import subprocess
import sys

def main():
    """Run the status check."""
    print("🚀 RUNNING STATUS CHECK")
    print("=" * 50)
    
    try:
        result = subprocess.run(
            [sys.executable, "check_current_status.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print("STDOUT:")
        if result.stdout:
            print(result.stdout)
        
        print("\nSTDERR:")
        if result.stderr:
            print(result.stderr)
        
        print(f"\nReturn code: {result.returncode}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running status check: {e}")
        return False

if __name__ == "__main__":
    main()