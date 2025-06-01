#!/usr/bin/env python3
"""
Test Suite Demonstration for Kimera SWM Toy Repository
=====================================================

This script demonstrates the comprehensive test suite and shows
how it addresses the real issues while filtering out phantom errors.
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime


def run_command(command, description):
    """Run a command and display results."""
    print(f"\n🔧 {description}")
    print("-" * 60)
    
    try:
        result = subprocess.run(
            command.split() if isinstance(command, str) else command,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(f"Command: {command}")
        print(f"Return code: {result.returncode}")
        
        if result.stdout:
            print("Output:")
            print(result.stdout)
        
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("⏰ Command timed out")
        return False
    except Exception as e:
        print(f"💥 Error running command: {e}")
        return False


def main():
    """Demonstrate the test suite."""
    print("[TARGET] KIMERA TEST SUITE DEMONSTRATION")
    print("=" * 80)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Directory: {Path.cwd()}")
    
    # Check if test files exist
    test_files = [
        "test_suite.py",
        "run_test_suite.py",
        "test_config.py",
        "setup_tests.py",
        "TEST_SUITE_README.md"
    ]
    
    print("\n📁 Test Suite Files:")
    all_present = True
    for test_file in test_files:
        if Path(test_file).exists():
            print(f"   [OK] {test_file}")
        else:
            print(f"   ❌ {test_file} - missing")
            all_present = False
    
    if not all_present:
        print("\n⚠️  Some test files are missing. Cannot proceed with demo.")
        return 1
    
    # Demonstrate different test modes
    demos = [
        ("python quick_test_validation.py", "Quick Validation"),
        ("python run_test_suite.py --mode env", "Environment Check"),
        ("python run_test_suite.py --mode quick", "Quick Tests"),
        ("python setup_tests.py", "Setup and Validation")
    ]
    
    results = []
    for command, description in demos:
        success = run_command(command, description)
        results.append((description, success))
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 DEMONSTRATION SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = "[OK] PASSED" if success else "[FAIL] FAILED"
        print(f"   {status}: {description}")
    
    print(f"\n[TARGET] Success Rate: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL DEMONSTRATIONS SUCCESSFUL!")
        print("\nThe test suite is working correctly and ready for use.")
        print("\nNext steps:")
        print("1. Run: python run_test_suite.py --mode full")
        print("2. Integrate with CI/CD pipeline")
        print("3. Add new tests as functionality grows")
    else:
        print("\n⚠️  SOME DEMONSTRATIONS FAILED")
        print("Check the output above for specific issues.")
    
    print("\n📚 Documentation:")
    print("   • Read TEST_SUITE_README.md for complete usage guide")
    print("   • Check test_config.py for configuration options")
    print("   • Use run_test_suite.py for different test modes")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())