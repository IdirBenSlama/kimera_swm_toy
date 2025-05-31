#!/usr/bin/env python3
"""
Quick setup script to install missing dependencies for Kimera-SWM v0.7.0
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and report success/failure."""
    print(f"[INFO] {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"[OK] {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description} failed:")
        print(f"  Command: {cmd}")
        print(f"  Error: {e.stderr}")
        return False

def main():
    """Install missing dependencies."""
    print("Kimera-SWM v0.7.0 - Dependency Setup")
    print("=" * 40)
    
    # Check if we're in a Poetry project
    if not Path("pyproject.toml").exists():
        print("[ERROR] Not in a Poetry project directory")
        print("Please run from the project root where pyproject.toml exists")
        return 1
    
    # Install missing packages
    commands = [
        ("poetry add pandas matplotlib", "Installing pandas and matplotlib"),
        ("poetry add --group dev pytest-asyncio", "Installing pytest-asyncio for dev"),
        ("poetry lock --no-update", "Updating lock file"),
        ("poetry install", "Installing all dependencies")
    ]
    
    success_count = 0
    for cmd, desc in commands:
        if run_command(cmd, desc):
            success_count += 1
        print()
    
    print("=" * 40)
    print(f"Setup Results: {success_count}/{len(commands)} commands succeeded")
    
    if success_count == len(commands):
        print("\n[SUCCESS] All dependencies installed!")
        print("\nNext steps:")
        print("1. Test the pipeline: python test_pipeline_fix.py")
        print("2. Run metrics demo: python demo_metrics_safe.py")
        print("3. Try a benchmark: poetry run python -m benchmarks.llm_compare data/toy_contradictions.csv --kimera-only")
        print("4. Explore results: open tools/explorer.html")
        return 0
    else:
        print(f"\n[ERROR] {len(commands) - success_count} commands failed")
        print("Try running the failed commands manually")
        return 1

if __name__ == "__main__":
    sys.exit(main())