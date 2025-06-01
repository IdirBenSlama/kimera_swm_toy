#!/usr/bin/env python3
import subprocess
import sys
import os

def run_test(name, script):
    print(f"\n{'='*50}")
    print(f"🧪 {name}")
    print('='*50)
    
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    
    print("STDOUT:")
    print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    success = result.returncode == 0
    print(f"Result: {'✅ PASSED' if success else '❌ FAILED'}")
    return success

def main():
    print("🚀 FINAL TEST RUN - Verifying all API compatibility fixes")
    
    tests = [
        ("Quick Verification", "quick_verify.py"),
        ("EchoForm Unit Tests", "test_echoform_only.py"),
        ("Identity Unit Tests", "test_identity_only.py"),
    ]
    
    passed = 0
    total = len(tests)
    
    for name, script in tests:
        if run_test(name, script):
            passed += 1
    
    # Also try running the original test files directly
    print(f"\n{'='*50}")
    print("🧪 Running Original Test Files")
    print('='*50)
    
    env = os.environ.copy()
    env['PYTHONPATH'] = 'src'
    
    original_tests = [
        "tests/unit/test_echoform_core.py",
        "tests/unit/test_identity.py"
    ]
    
    for test_file in original_tests:
        print(f"\nRunning {test_file}...")
        result = subprocess.run([sys.executable, test_file], capture_output=True, text=True, env=env)
        
        if result.returncode == 0:
            print(f"✅ {test_file} PASSED")
            passed += 1
        else:
            print(f"❌ {test_file} FAILED")
            if result.stdout:
                print("STDOUT:", result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
        
        total += 1
    
    print(f"\n{'='*60}")
    print(f"📊 FINAL RESULTS: {passed}/{total} tests passed")
    print('='*60)
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("✅ API compatibility fixes are working perfectly!")
        print("✅ Original unit tests now pass without modification!")
        print("✅ The API drift issue has been completely resolved!")
    else:
        print(f"❌ {total - passed} test(s) failed")
        print("🔧 Some issues may still need attention")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)