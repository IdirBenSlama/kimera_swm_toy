#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

def run_import_test():
    try:
        result = subprocess.run([
            sys.executable, "quick_import_test.py"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        print("=== Import Test Output ===")
        print(result.stdout)
        
        if result.stderr:
            print("=== Errors ===")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = run_import_test()
    print(f"Import test {'passed' if success else 'failed'}")