#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

def run_basic_p0():
    try:
        result = subprocess.run([
            sys.executable, "test_basic_p0.py"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        print("=== Basic P0 Test Output ===")
        print(result.stdout)
        
        if result.stderr:
            print("=== Errors ===")
            print(result.stderr)
        
        print(f"=== Return Code: {result.returncode} ===")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = run_basic_p0()
    print(f"\nBasic P0 test {'passed' if success else 'failed'}")
    
    if success:
        print("\n🚀 Ready to run full P0 tests!")
        print("Next steps:")
        print("1. python test_migration_dev.py")
        print("2. python run_p0_tests.py")
    else:
        print("\n💥 Fix basic issues before proceeding to full P0 tests")