#!/usr/bin/env python3
"""Run quick verification to check system status."""

import subprocess
import sys
import os

def run_test(script_name):
    """Run a test script and return the result."""
    print(f"\n🧪 Running {script_name}")
    print("-" * 40)
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(f"Return code: {result.returncode}")
        
        if result.stdout:
            print("Output:")
            print(result.stdout)
        
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ Test timed out")
        return False
    except Exception as e:
        print(f"❌ Error running test: {e}")
        return False

def main():
    """Run verification tests."""
    print("🚀 QUICK VERIFICATION TEST")
    print("=" * 50)
    
    # Test files to run
    test_files = [
        "test_verification_runner.py",
        "test_import_fixes.py",
        "test_system_quick.py"
    ]
    
    results = []
    
    for test_file in test_files:
        if os.path.exists(test_file):
            success = run_test(test_file)
            results.append((test_file, success))
        else:
            print(f"⚠️ Test file not found: {test_file}")
            results.append((test_file, False))
    
    print("\n" + "=" * 50)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_file, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {test_file}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 ALL VERIFICATION TESTS PASSED!")
    else:
        print(f"\n⚠️ {len(results) - passed} test(s) failed")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)