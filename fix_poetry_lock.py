#!/usr/bin/env python3
"""
Fix the poetry.lock sync issue and install dependencies.
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and show output."""
    print(f"\n[INFO] {description}")
    print(f"[CMD] {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, text=True, timeout=300)
        if result.returncode == 0:
            print(f"[OK] {description} completed successfully")
            return True
        else:
            print(f"[ERROR] {description} failed with exit code {result.returncode}")
            return False
    except subprocess.TimeoutExpired:
        print(f"[ERROR] {description} timed out")
        return False
    except Exception as e:
        print(f"[ERROR] {description} failed: {e}")
        return False

def main():
    print("Fixing Poetry Lock File and Installing Dependencies")
    print("=" * 55)
    
    # Check if we're in the right directory
    if not Path("src/kimera").exists():
        print("[ERROR] Not in Kimera project root directory")
        print("Please run from the project root where src/kimera exists")
        return 1
    
    # Step 1: Update lock file
    if not run_command(["poetry", "lock"], "Updating poetry.lock file"):
        print("\n[ERROR] Failed to update poetry.lock")
        print("This usually means there's an issue with pyproject.toml")
        return 1
    
    # Step 2: Install dependencies
    if not run_command(["poetry", "install"], "Installing dependencies"):
        print("\n[ERROR] Failed to install dependencies")
        return 1
    
    print("\n" + "=" * 55)
    print("[SUCCESS] Dependencies installed successfully!")
    print("\nNext steps:")
    print("1. Run validation: python validate_all_green.py")
    print("2. Run benchmark: python setup_and_run.py")
    print("   OR manually: poetry run python -m benchmarks.llm_compare data/toy_contradictions.csv --max-pairs 20 --stats --kimera-only")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())