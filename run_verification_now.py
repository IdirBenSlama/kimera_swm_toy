#!/usr/bin/env python3
"""Run the verification tests as requested by the user."""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and return the result."""
    print(f"\n🧪 {description}")
    print("=" * 60)
    
    try:
        # Run the command with shell=True for Python execution
        result = subprocess.run(
            cmd, 
            shell=True,
            capture_output=True, 
            text=True, 
            timeout=60,
            cwd=os.getcwd()
        )
        
        print(f"Command: {cmd}")
        print(f"Return code: {result.returncode}")
        
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print(f"❌ Command timed out: {cmd}")
        return False
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

def main():
    """Run all verification tests."""
    print("🚀 RUNNING VERIFICATION TESTS AS REQUESTED")
    print("=" * 60)
    
    # Check if test files exist first
    test_files = [
        "test_import_fixes.py",
        "run_tests.py", 
        "verify_import_fixes.py"
    ]
    
    print("📋 Checking test files...")
    for test_file in test_files:
        exists = os.path.exists(test_file)
        status = "✅" if exists else "❌"
        print(f"{status} {test_file}")
    
    tests = [
        ("python test_import_fixes.py", "Test Import Fixes"),
        ("python run_tests.py", "Run All Tests"),
        ("python verify_import_fixes.py", "Comprehensive Verification")
    ]
    
    results = []
    
    for cmd, description in tests:
        success = run_command(cmd, description)
        results.append((description, success))
    
    print("\n" + "=" * 60)
    print("📊 VERIFICATION RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    for description, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {description}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 ALL VERIFICATION TESTS PASSED!")
        print("✅ Import path fixes are working correctly")
        print("✅ System is ready for production")
    else:
        print(f"\n⚠️  {len(results) - passed} test(s) failed")
        print("❌ Some issues need to be addressed")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)