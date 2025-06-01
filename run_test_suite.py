#!/usr/bin/env python3
"""
Test Suite Runner for Kimera SWM Toy Repository
==============================================

This script runs the comprehensive test suite and provides additional
testing utilities for the Kimera project.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path
from datetime import datetime


def run_main_test_suite():
    """Run the main comprehensive test suite."""
    print("[RUN] Running Comprehensive Test Suite")
    print("=" * 60)
    
    try:
        result = subprocess.run([
            sys.executable, "test_suite.py"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running test suite: {e}")
        return False


def run_quick_tests():
    """Run quick validation tests."""
    print("⚡ Running Quick Tests")
    print("=" * 40)
    
    quick_tests = [
        "test_import_fixes.py",
        "test_system_quick.py",
        "basic_import_test.py"
    ]
    
    results = []
    for test in quick_tests:
        if Path(test).exists():
            print(f"\n🧪 Running {test}...")
            try:
                result = subprocess.run([
                    sys.executable, test
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    print(f"✅ {test} PASSED")
                    results.append((test, True, None))
                else:
                    print(f"❌ {test} FAILED")
                    print(f"   Output: {result.stdout}")
                    print(f"   Error: {result.stderr}")
                    results.append((test, False, result.stderr))
            except subprocess.TimeoutExpired:
                print(f"⏰ {test} TIMEOUT")
                results.append((test, False, "Timeout"))
            except Exception as e:
                print(f"💥 {test} ERROR: {e}")
                results.append((test, False, str(e)))
        else:
            print(f"⏭️  {test} not found, skipping")
            results.append((test, None, "File not found"))
    
    # Summary
    passed = sum(1 for _, success, _ in results if success is True)
    failed = sum(1 for _, success, _ in results if success is False)
    skipped = sum(1 for _, success, _ in results if success is None)
    
    print(f"\n📊 Quick Tests Summary:")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   ⏭️  Skipped: {skipped}")
    
    return failed == 0


def run_ci_simulation():
    """Simulate CI environment testing."""
    print("🔄 Simulating CI Environment")
    print("=" * 40)
    
    # Check if we can run the CI steps locally
    ci_steps = [
        ("Import Fix Test", "python test_import_fixes.py"),
        ("Quick System Test", "python test_system_quick.py"),
        ("Vault and SCAR Test", "python test_vault_and_scar.py")
    ]
    
    results = []
    for step_name, command in ci_steps:
        print(f"\n🔧 {step_name}...")
        try:
            result = subprocess.run(
                command.split(), 
                capture_output=True, 
                text=True, 
                timeout=60
            )
            
            if result.returncode == 0:
                print(f"✅ {step_name} PASSED")
                results.append((step_name, True))
            else:
                print(f"❌ {step_name} FAILED")
                print(f"   Command: {command}")
                print(f"   Output: {result.stdout}")
                print(f"   Error: {result.stderr}")
                results.append((step_name, False))
        except subprocess.TimeoutExpired:
            print(f"⏰ {step_name} TIMEOUT")
            results.append((step_name, False))
        except FileNotFoundError:
            print(f"📁 {step_name} - Test file not found")
            results.append((step_name, None))
        except Exception as e:
            print(f"💥 {step_name} ERROR: {e}")
            results.append((step_name, False))
    
    # Summary
    passed = sum(1 for _, success in results if success is True)
    failed = sum(1 for _, success in results if success is False)
    skipped = sum(1 for _, success in results if success is None)
    
    print(f"\n📊 CI Simulation Summary:")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   ⏭️  Skipped: {skipped}")
    
    return failed == 0


def check_environment():
    """Check the testing environment."""
    print("🔍 Environment Check")
    print("=" * 30)
    
    print(f"Python version: {sys.version}")
    print(f"Working directory: {Path.cwd()}")
    print(f"Python path: {sys.path[:3]}...")  # Show first 3 entries
    
    # Check for required directories
    required_dirs = ["src", "src/kimera", "vault", "vault/core", ".github/workflows"]
    missing_dirs = [d for d in required_dirs if not Path(d).exists()]
    
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
    else:
        print("✅ All required directories present")
    
    # Check for key files
    key_files = [
        "src/kimera/__init__.py",
        "src/kimera/identity.py", 
        "src/kimera/storage.py",
        "vault/core/vault.py",
        ".github/workflows/ci.yml"
    ]
    missing_files = [f for f in key_files if not Path(f).exists()]
    
    if missing_files:
        print(f"❌ Missing key files: {missing_files}")
        return False
    else:
        print("✅ All key files present")
    
    return True


def run_problem_analysis():
    """Analyze the current problems in the workspace."""
    print("🔍 Problem Analysis")
    print("=" * 30)
    
    # This would ideally use the problems tool, but we'll simulate it
    print("📋 Known Issue Categories:")
    print("   • Phantom CI file errors (can be ignored)")
    print("   • Markdown formatting warnings (non-critical)")
    print("   • Spelling warnings for 'Kimera', 'echoform' (expected)")
    print("   • Some unused import warnings (cleanup needed)")
    
    print("\n[TARGET] Focus Areas:")
    print("   • Functional testing of core components")
    print("   • Import path verification")
    print("   • Integration testing")
    print("   • CI workflow validation")
    
    return True


def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(description="Kimera Test Suite Runner")
    parser.add_argument("--mode", choices=["full", "quick", "ci", "env", "problems"], 
                       default="full", help="Test mode to run")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Verbose output")
    
    args = parser.parse_args()
    
    print("[TARGET] KIMERA TEST SUITE RUNNER")
    print("=" * 60)
    print(f"Mode: {args.mode}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    success = True
    
    if args.mode == "env":
        success = check_environment()
    elif args.mode == "problems":
        success = run_problem_analysis()
    elif args.mode == "quick":
        success = check_environment() and run_quick_tests()
    elif args.mode == "ci":
        success = check_environment() and run_ci_simulation()
    elif args.mode == "full":
        success = (check_environment() and 
                  run_main_test_suite() and 
                  run_quick_tests() and 
                  run_ci_simulation())
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("   The repository appears to be in good working condition.")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("   Check the output above for specific issues.")
    
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())