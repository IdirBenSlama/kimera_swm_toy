#!/usr/bin/env python3
import subprocess
import sys
import os

# Set up environment
env = os.environ.copy()
env['PYTHONPATH'] = 'src'

def run_test(test_name, command):
    print(f"\n{'='*60}")
    print(f"🧪 Running {test_name}...")
    print('='*60)
    
    result = subprocess.run(command, capture_output=True, text=True, env=env)
    
    print("STDOUT:")
    print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    print(f"Return code: {result.returncode}")
    
    if result.returncode == 0:
        print(f"✅ {test_name} PASSED!")
        return True
    else:
        print(f"❌ {test_name} FAILED!")
        return False

def main():
    print("🚀 Running all original unit tests to verify API compatibility fixes...")
    
    tests = [
        ("EchoForm Core Tests", [sys.executable, 'tests/unit/test_echoform_core.py']),
        ("Identity Tests", [sys.executable, 'tests/unit/test_identity.py']),
        ("Storage Tests", [sys.executable, '-m', 'pytest', 'tests/unit/test_storage.py', '-v']),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, command in tests:
        if run_test(test_name, command):
            passed += 1
    
    print(f"\n{'='*60}")
    print(f"📊 FINAL RESULTS: {passed}/{total} test suites passed")
    print('='*60)
    
    if passed == total:
        print("🎉 ALL UNIT TESTS PASSED!")
        print("✅ API compatibility fixes are working correctly!")
        return True
    else:
        print(f"❌ {total - passed} test suite(s) failed")
        print("🔧 Some issues still need to be resolved")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)