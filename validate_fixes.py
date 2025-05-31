#!/usr/bin/env python3
"""
Quick validation script to verify all fixes are working.
Tests the specific issues mentioned in the zero-fog recap.
"""

import sys
import os
from pathlib import Path

def test_unicode_fixes():
    """Test that Unicode emojis have been replaced."""
    print("Testing Unicode fixes...")
    
    if not Path("demo_metrics_safe.py").exists():
        print("  [SKIP] demo_metrics_safe.py not found")
        return True
    
    with open("demo_metrics_safe.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for problematic Unicode characters
    problematic = ["🎯", "📦", "✅", "❌", "📂", "🔬", "📊", "🔄", "📈", "📄", "🎉", "🔐"]
    found_unicode = []
    
    for emoji in problematic:
        if emoji in content:
            found_unicode.append(emoji)
    
    if found_unicode:
        print(f"  [ERROR] Still contains Unicode: {found_unicode}")
        return False
    else:
        print("  [OK] No problematic Unicode characters found")
        return True

def test_pandas_import():
    """Test that pandas can be imported."""
    print("Testing pandas import...")
    
    try:
        import pandas as pd
        print("  [OK] pandas imported successfully")
        return True
    except ImportError:
        print("  [ERROR] pandas not available")
        print("  Run: poetry add pandas")
        return False

def test_pytest_markers():
    """Test that pytest async markers are present."""
    print("Testing pytest async markers...")
    
    test_file = "tests/test_openai_async.py"
    if not Path(test_file).exists():
        print(f"  [SKIP] {test_file} not found")
        return True
    
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "pytestmark = pytest.mark.asyncio" in content:
        print("  [OK] Async marker found")
        return True
    else:
        print("  [ERROR] Async marker missing")
        return False

def test_data_files():
    """Test that required data files exist."""
    print("Testing data files...")
    
    required_files = [
        "data/toy_contradictions.csv",
        "data/contradictions_2k.csv"
    ]
    
    all_found = True
    for file in required_files:
        if Path(file).exists():
            print(f"  [OK] {file}")
        else:
            print(f"  [MISSING] {file}")
            all_found = False
    
    return all_found

def test_core_imports():
    """Test that core Kimera modules can be imported."""
    print("Testing core imports...")
    
    try:
        sys.path.insert(0, str(Path("src")))
        from kimera.metrics import roc_stats, pr_stats, bootstrap_ci
        from kimera.geoid import Geoid
        print("  [OK] Core modules imported successfully")
        return True
    except ImportError as e:
        print(f"  [ERROR] Import failed: {e}")
        return False

def test_benchmark_module():
    """Test that benchmark module can be imported."""
    print("Testing benchmark module...")
    
    try:
        sys.path.insert(0, str(Path("benchmarks")))
        from benchmarks.llm_compare import main
        print("  [OK] Benchmark module imported successfully")
        return True
    except ImportError as e:
        print(f"  [ERROR] Benchmark import failed: {e}")
        return False

def main():
    """Run all validation tests."""
    print("Kimera-SWM v0.7.0 - Fix Validation")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("src/kimera").exists():
        print("[ERROR] Not in Kimera project root directory")
        return 1
    
    tests = [
        test_unicode_fixes,
        test_pandas_import,
        test_pytest_markers,
        test_data_files,
        test_core_imports,
        test_benchmark_module
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"  [ERROR] Test failed with exception: {e}")
            print()
    
    print("=" * 40)
    print(f"Validation Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[SUCCESS] All fixes validated successfully!")
        print("\nReady to run:")
        print("1. python demo_metrics_safe.py")
        print("2. python run_all_tests.py")
        print("3. poetry run pytest")
        print("4. PowerShell: .\\run_benchmark.ps1")
        return 0
    else:
        print(f"\n[PARTIAL] {total - passed} tests failed")
        print("Check the output above for specific issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())