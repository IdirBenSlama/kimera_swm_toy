#!/usr/bin/env python3
"""
Comprehensive test runner for Kimera-SWM v0.7.0
Handles all the issues mentioned in the zero-fog recap.
"""

import sys
import os
import subprocess
from pathlib import Path

def print_header(title):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def run_command(cmd, description, capture_output=False):
    """Run a command and return success status."""
    print(f"\n[RUNNING] {description}")
    print(f"[CMD] {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    
    try:
        if capture_output:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                encoding='utf-8', 
                errors='replace'
            )
            print(result.stdout)
            if result.stderr:
                print(f"[STDERR] {result.stderr}")
            return result.returncode == 0
        else:
            result = subprocess.run(cmd, encoding='utf-8', errors='replace')
            return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] Command failed: {e}")
        return False

def check_dependencies():
    """Check if all required dependencies are available."""
    print_header("DEPENDENCY CHECK")
    
    required = ["pandas", "numpy", "matplotlib", "pytest", "pyyaml"]
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"[OK] {package}")
        except ImportError:
            missing.append(package)
            print(f"[MISSING] {package}")
    
    if missing:
        print(f"\n[ERROR] Missing packages: {', '.join(missing)}")
        print("Run: poetry install")
        return False
    
    print("\n[OK] All dependencies available")
    return True

def run_safe_demo():
    """Run the safe metrics demo."""
    print_header("SAFE METRICS DEMO")
    
    if not Path("demo_metrics_safe.py").exists():
        print("[ERROR] demo_metrics_safe.py not found")
        return False
    
    return run_command([sys.executable, "demo_metrics_safe.py"], "Safe metrics demo")

def run_pytest():
    """Run the test suite."""
    print_header("PYTEST SUITE")
    
    return run_command([
        sys.executable, "-m", "pytest", 
        "-v", "--tb=short", "-x"
    ], "Full test suite")

def run_benchmark():
    """Run the benchmark with proper command structure."""
    print_header("BENCHMARK WITH METRICS")
    
    # Check for API key
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key or api_key.startswith("sk-proj-"):
        print("[INFO] No valid API key found. Running Kimera-only mode.")
        cmd = [
            sys.executable, "-m", "benchmarks.llm_compare",
            "data/contradictions_2k.csv",
            "--max-pairs", "500",
            "--stats",
            "--no-cache",
            "--kimera-only"
        ]
    else:
        print("[INFO] API key found. Running full comparison.")
        cmd = [
            sys.executable, "-m", "benchmarks.llm_compare",
            "data/contradictions_2k.csv", 
            "--max-pairs", "500",
            "--stats",
            "--no-cache",
            "--async", "8",
            "--mp", "4"
        ]
    
    return run_command(cmd, "Benchmark with comprehensive metrics")

def check_generated_files():
    """Check what files were generated."""
    print_header("GENERATED FILES CHECK")
    
    expected_files = [
        "kimera_metrics_demo.png",
        "kimera_metrics_demo.yaml", 
        "benchmark_results.csv",
        "metrics.yaml",
        "roc.png"
    ]
    
    found = []
    missing = []
    
    for file in expected_files:
        if Path(file).exists():
            size = Path(file).stat().st_size
            print(f"[OK] {file} ({size} bytes)")
            found.append(file)
        else:
            print(f"[MISSING] {file}")
            missing.append(file)
    
    print(f"\n[SUMMARY] Found {len(found)}/{len(expected_files)} expected files")
    return len(found) > 0

def main():
    """Main test runner."""
    print("Kimera-SWM v0.7.0 - Comprehensive Test Runner")
    print("Addresses all issues from zero-fog recap")
    
    # Check if we're in the right directory
    if not Path("src/kimera").exists():
        print("\n[ERROR] Not in Kimera project root directory")
        print("Please run from the project root where src/kimera exists")
        return 1
    
    success_count = 0
    total_tests = 4
    
    # 1. Check dependencies
    if check_dependencies():
        success_count += 1
    
    # 2. Run safe demo (no API key needed)
    if run_safe_demo():
        success_count += 1
    
    # 3. Run pytest
    if run_pytest():
        success_count += 1
    
    # 4. Run benchmark
    if run_benchmark():
        success_count += 1
    
    # Check generated files
    check_generated_files()
    
    # Final summary
    print_header("FINAL SUMMARY")
    print(f"Completed {success_count}/{total_tests} test phases successfully")
    
    if success_count == total_tests:
        print("\n[SUCCESS] All tests passed! Kimera-SWM v0.7.0 is ready.")
        print("\nNext steps:")
        print("1. Review generated metrics.yaml for performance insights")
        print("2. Check roc.png for visual performance comparison")
        print("3. Proceed to error-bucket dashboard or threshold tuning")
        return 0
    else:
        print(f"\n[PARTIAL] {total_tests - success_count} phases failed")
        print("Check the output above for specific issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())