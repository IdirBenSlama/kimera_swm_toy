#!/usr/bin/env python3
"""
Fix missing dependencies and prepare for benchmark.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and report results."""
    print(f"\n[INFO] {description}")
    print(f"[CMD] {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f"[OK] {description} completed successfully")
            return True
        else:
            print(f"[ERROR] {description} failed:")
            print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print(f"[ERROR] {description} timed out")
        return False
    except Exception as e:
        print(f"[ERROR] {description} failed: {e}")
        return False

def check_poetry():
    """Check if poetry is available."""
    try:
        result = subprocess.run(["poetry", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[OK] Poetry found: {result.stdout.strip()}")
            return True
        else:
            print("[ERROR] Poetry not found or not working")
            return False
    except FileNotFoundError:
        print("[ERROR] Poetry not found in PATH")
        return False

def main():
    print("Kimera-SWM Dependency Fixer")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("src/kimera").exists():
        print("[ERROR] Not in Kimera project root directory")
        print("Please run from the project root where src/kimera exists")
        return 1
    
    # Check poetry
    if not check_poetry():
        print("\nPlease install Poetry first:")
        print("https://python-poetry.org/docs/#installation")
        return 1
    
    # Install dependencies
    success = True
    
    # Update lock file and install
    success &= run_command(["poetry", "lock"], "Updating poetry.lock")
    success &= run_command(["poetry", "install"], "Installing dependencies")
    
    if success:
        print("\n" + "=" * 40)
        print("[SUCCESS] Dependencies should now be ready!")
        print("\nNext steps:")
        print("1. Run validation: python validate_all_green.py")
        print("2. Run benchmark: poetry run python -m benchmarks.llm_compare data/toy_contradictions.csv --max-pairs 20 --stats --kimera-only")
        print("3. Open tools/explorer.html to view results")
        return 0
    else:
        print("\n" + "=" * 40)
        print("[ERROR] Some dependency installation steps failed")
        print("Please check the error messages above")
        return 1

if __name__ == "__main__":
    sys.exit(main())