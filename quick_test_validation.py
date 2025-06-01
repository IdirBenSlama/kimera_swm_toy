#!/usr/bin/env python3
"""
Quick validation of the test suite setup
"""

import sys
from pathlib import Path

def main():
    print("🔍 Quick Test Suite Validation")
    print("=" * 40)
    
    # Check test files exist
    test_files = [
        "test_suite.py",
        "run_test_suite.py", 
        "test_config.py",
        "setup_tests.py",
        "TEST_SUITE_README.md"
    ]
    
    print("📁 Checking test files...")
    all_present = True
    for test_file in test_files:
        if Path(test_file).exists():
            print(f"[OK] {test_file}")
        else:
            print(f"❌ {test_file} - missing")
            all_present = False
    
    # Check basic syntax
    print("\n🔍 Checking Python syntax...")
    python_files = ["test_suite.py", "run_test_suite.py", "test_config.py", "setup_tests.py"]
    syntax_ok = True
    
    for py_file in python_files:
        if Path(py_file).exists():
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    compile(f.read(), py_file, 'exec')
                print(f"[OK] {py_file} - syntax OK")
            except SyntaxError as e:
                print(f"❌ {py_file} - syntax error: {e}")
                syntax_ok = False
        else:
            print(f"⏭️  {py_file} - not found")
    
    # Check repository structure
    print("\n🏗️  Checking repository structure...")
    required_dirs = ["src", "src/kimera", "vault", "vault/core", ".github/workflows"]
    structure_ok = True
    
    for directory in required_dirs:
        if Path(directory).exists():
            print(f"[OK] {directory}/")
        else:
            print(f"❌ {directory}/ - missing")
            structure_ok = False
    
    # Summary
    print("\n" + "=" * 40)
    if all_present and syntax_ok and structure_ok:
        print("🎉 TEST SUITE VALIDATION PASSED!")
        print("\nReady to run:")
        print("  python run_test_suite.py --mode env")
        print("  python run_test_suite.py --mode quick")
        return 0
    else:
        print("⚠️  VALIDATION ISSUES FOUND")
        if not all_present:
            print("  • Some test files are missing")
        if not syntax_ok:
            print("  • Syntax errors in test files")
        if not structure_ok:
            print("  • Repository structure issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())