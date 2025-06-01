#!/usr/bin/env python3
"""Run quick status check to see current system state."""

import subprocess
import sys
import os

def main():
    """Run the quick status verification."""
    print("🚀 Running Quick Status Check")
    print("=" * 40)
    
    try:
        # Run the quick status verification
        result = subprocess.run([
            sys.executable, "quick_status_verification.py"
        ], text=True, timeout=30)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"\nReturn code: {result.returncode}")
        
        return result.returncode
        
    except Exception as e:
        print(f"❌ Error running status check: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())