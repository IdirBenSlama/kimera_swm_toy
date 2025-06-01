#!/usr/bin/env python3
"""
Run the P0 verification suite
"""

import subprocess
import sys
import os
from pathlib import Path

def run_verification():
    """Run the P0 verification script"""
    print("🚀 Running P0 Verification Suite")
    print("=" * 50)
    
    # Change to the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    try:
        # Run the verification script
        result = subprocess.run([
            sys.executable, "verify_p0_fixes.py"
        ], capture_output=True, text=True, timeout=300)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"Exit code: {result.returncode}")
        return result.returncode
        
    except subprocess.TimeoutExpired:
        print("❌ Verification timed out after 5 minutes")
        return 1
    except Exception as e:
        print(f"❌ Failed to run verification: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run_verification())