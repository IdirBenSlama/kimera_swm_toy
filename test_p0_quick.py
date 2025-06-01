#!/usr/bin/env python3
"""
Quick P0 test - just run the simple test to verify basic functionality
"""

import subprocess
import sys
from pathlib import Path

def main():
    print("🚀 Quick P0 Test - Running Simple P0 Test")
    
    try:
        result = subprocess.run([
            sys.executable, "simple_p0_test.py"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        print("=== STDOUT ===")
        print(result.stdout)
        
        if result.stderr:
            print("=== STDERR ===")
            print(result.stderr)
        
        print(f"=== Return Code: {result.returncode} ===")
        
        if result.returncode == 0:
            print("\n✅ Simple P0 test PASSED!")
            print("🚀 Basic functionality is working")
            print("\nNext steps:")
            print("1. Run migration test: python run_migration_test.py")
            print("2. Run full P0 suite: python run_complete_p0_suite.py")
        else:
            print("\n❌ Simple P0 test FAILED!")
            print("💥 Basic functionality needs fixing")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)