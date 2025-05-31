#!/usr/bin/env python3
"""
Complete setup and benchmark runner for Kimera-SWM.
Addresses dependency issues and provides clear next steps.
"""

import subprocess
import sys
import os
import importlib
from pathlib import Path

def print_header(title):
    """Print section header."""
    print(f"\n{'='*50}")
    print(f" {title}")
    print('='*50)

def check_dependency(name, module_name=None):
    """Check if a dependency can be imported."""
    if module_name is None:
        module_name = name
    
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

def run_command(cmd, description, timeout=300):
    """Run a command and report results."""
    print(f"\n[INFO] {description}")
    print(f"[CMD] {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.returncode == 0:
            print(f"[OK] {description} completed successfully")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"[ERROR] {description} failed:")
            if result.stderr:
                print(result.stderr)
            if result.stdout:
                print(result.stdout)
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

def check_dependencies():
    """Check critical dependencies."""
    print_header("CHECKING DEPENDENCIES")
    
    critical_deps = [
        ("pandas", "pandas"),
        ("matplotlib", "matplotlib.pyplot"),
        ("numpy", "numpy"),
        ("scikit-learn", "sklearn"),
        ("sentence-transformers", "sentence_transformers"),
    ]
    
    missing = []
    for name, module in critical_deps:
        if check_dependency(name, module):
            print(f"[OK] {name}")
        else:
            print(f"[MISSING] {name}")
            missing.append(name)
    
    return missing

def install_dependencies():
    """Install missing dependencies."""
    print_header("INSTALLING DEPENDENCIES")
    
    if not check_poetry():
        print("\nPlease install Poetry first:")
        print("https://python-poetry.org/docs/#installation")
        return False
    
    # Update lock file first, then install
    success = True
    success &= run_command(["poetry", "lock"], "Updating poetry.lock file")
    success &= run_command(["poetry", "install"], "Installing all dependencies")
    
    return success

def run_validation():
    """Run the validation script."""
    print_header("RUNNING VALIDATION")
    
    if not Path("validate_all_green.py").exists():
        print("[ERROR] validate_all_green.py not found")
        return False
    
    return run_command([sys.executable, "validate_all_green.py"], "Running validation tests")

def run_benchmark():
    """Run a quick benchmark."""
    print_header("RUNNING BENCHMARK")
    
    # Check for data file
    data_file = Path("data/toy_contradictions.csv")
    if not data_file.exists():
        print(f"[ERROR] Dataset not found: {data_file}")
        return False
    
    # Build command
    cmd = [
        "poetry", "run", "python", "-m", "benchmarks.llm_compare",
        str(data_file),
        "--max-pairs", "20",
        "--stats",
        "--kimera-only"
    ]
    
    return run_command(cmd, "Running benchmark", timeout=600)

def main():
    print("Kimera-SWM Complete Setup and Benchmark Runner")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("src/kimera").exists():
        print("[ERROR] Not in Kimera project root directory")
        print("Please run from the project root where src/kimera exists")
        return 1
    
    # Step 1: Check dependencies
    missing = check_dependencies()
    
    # Step 2: Install if needed
    if missing:
        print(f"\n[INFO] Missing dependencies: {', '.join(missing)}")
        if not install_dependencies():
            print("[ERROR] Failed to install dependencies")
            return 1
    else:
        print("\n[INFO] All critical dependencies found")
    
    # Step 3: Run validation
    if not run_validation():
        print("[WARNING] Validation had issues, but continuing...")
    
    # Step 4: Run benchmark
    if run_benchmark():
        print_header("SUCCESS!")
        print("Benchmark completed successfully!")
        print("\nGenerated files:")
        
        files_to_check = ["benchmark_results.csv", "metrics.yaml", "roc.png"]
        for file_path in files_to_check:
            if Path(file_path).exists():
                size = Path(file_path).stat().st_size
                print(f"  [OK] {file_path} ({size} bytes)")
            else:
                print(f"  [MISSING] {file_path}")
        
        print("\nNext steps:")
        print("1. Open tools/explorer.html in your browser")
        print("2. Load benchmark_results.csv")
        print("3. Check 'Only disagreements' to see failure patterns")
        print("4. Analyze patterns to design next algorithm improvements")
        
        return 0
    else:
        print_header("BENCHMARK FAILED")
        print("Please check the error messages above")
        print("\nTroubleshooting:")
        print("1. Ensure all dependencies are installed: poetry install")
        print("2. Check that data/toy_contradictions.csv exists")
        print("3. Try running manually: poetry run python -m benchmarks.llm_compare data/toy_contradictions.csv --max-pairs 5 --kimera-only")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())