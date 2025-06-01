#!/usr/bin/env python3
"""
Setup script for Kimera Test Suite
==================================

This script sets up the test environment and validates the test suite.
"""

import os
import sys
import stat
from pathlib import Path


def make_executable(file_path):
    """Make a file executable."""
    try:
        current_permissions = os.stat(file_path).st_mode
        os.chmod(file_path, current_permissions | stat.S_IEXEC)
        print(f"[OK] Made {file_path} executable")
        return True
    except Exception as e:
        print(f"❌ Failed to make {file_path} executable: {e}")
        return False


def validate_test_files():
    """Validate that test files are properly structured."""
    test_files = [
        "test_suite.py",
        "run_test_suite.py", 
        "test_config.py",
        "setup_tests.py"
    ]
    
    print("🔍 Validating test files...")
    
    all_valid = True
    for test_file in test_files:
        if Path(test_file).exists():
            try:
                # Check syntax
                with open(test_file, 'r', encoding='utf-8') as f:
                    compile(f.read(), test_file, 'exec')
                print(f"[OK] {test_file} - syntax OK")
            except SyntaxError as e:
                print(f"❌ {test_file} - syntax error: {e}")
                all_valid = False
            except Exception as e:
                print(f"⚠️  {test_file} - warning: {e}")
        else:
            print(f"❌ {test_file} - not found")
            all_valid = False
    
    return all_valid


def check_dependencies():
    """Check for required dependencies."""
    print("📦 Checking dependencies...")
    
    # Check for optional dependencies
    optional_deps = {
        "yaml": "PyYAML (for CI configuration validation)",
        "pytest": "pytest (for advanced testing features)"
    }
    
    available = []
    missing = []
    
    for module, description in optional_deps.items():
        try:
            __import__(module)
            available.append(f"[OK] {module} - {description}")
        except ImportError:
            missing.append(f"⚠️  {module} - {description}")
    
    print("\nAvailable optional dependencies:")
    for dep in available:
        print(f"  {dep}")
    
    if missing:
        print("\nMissing optional dependencies:")
        for dep in missing:
            print(f"  {dep}")
        print("\nNote: Tests will work without these, but some features may be limited.")
    
    return True


def create_test_summary():
    """Create a summary of available tests."""
    print("📋 Test Summary:")
    print("=" * 50)
    
    test_info = {
        "test_suite.py": "Comprehensive test suite with all categories",
        "run_test_suite.py": "Test runner with multiple execution modes",
        "test_config.py": "Configuration and constants",
        "setup_tests.py": "This setup and validation script"
    }
    
    # Check for legacy test files
    legacy_tests = [
        "test_import_fixes.py",
        "test_system_quick.py", 
        "test_vault_and_scar.py",
        "basic_import_test.py"
    ]
    
    print("Core Test Suite:")
    for test_file, description in test_info.items():
        status = "[OK]" if Path(test_file).exists() else "[FAIL]"
        print(f"  {status} {test_file} - {description}")
    
    print("\nLegacy/Additional Tests:")
    for test_file in legacy_tests:
        status = "[OK]" if Path(test_file).exists() else "[WARN]"
        print(f"  {status} {test_file}")
    
    print("\nUsage:")
    print("  python run_test_suite.py --mode full    # Run all tests")
    print("  python run_test_suite.py --mode quick   # Run quick tests")
    print("  python run_test_suite.py --mode ci      # Simulate CI")
    print("  python run_test_suite.py --mode env     # Check environment")


def main():
    """Main setup function."""
    print("[RUN] KIMERA TEST SUITE SETUP")
    print("=" * 50)
    
    success = True
    
    # Make test files executable
    executable_files = ["test_suite.py", "run_test_suite.py", "setup_tests.py"]
    for file_path in executable_files:
        if Path(file_path).exists():
            make_executable(file_path)
    
    # Validate test files
    if not validate_test_files():
        success = False
    
    # Check dependencies
    check_dependencies()
    
    # Create summary
    create_test_summary()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 TEST SUITE SETUP COMPLETE!")
        print("\nNext steps:")
        print("1. Run: python run_test_suite.py --mode env")
        print("2. Run: python run_test_suite.py --mode quick")
        print("3. Run: python run_test_suite.py --mode full")
    else:
        print("⚠️  SETUP COMPLETED WITH WARNINGS")
        print("Check the output above for specific issues.")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())