#!/usr/bin/env python3
"""
Run EchoForm tests to verify implementation
"""
import subprocess
import sys

def run_test(test_file):
    """Run a specific test file"""
    print(f"\n🧪 Running {test_file}...")
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ {test_file} passed")
            print(result.stdout)
            return True
        else:
            print(f"❌ {test_file} failed")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print(f"⏰ {test_file} timed out")
        return False
    except Exception as e:
        print(f"💥 Error running {test_file}: {e}")
        return False

def main():
    """Run all EchoForm tests"""
    print("🚀 Running EchoForm Test Suite")
    print("=" * 35)
    
    tests = [
        "tests/test_echoform_core.py",
        "tests/test_echoform_flow.py"
    ]
    
    passed = 0
    for test in tests:
        if run_test(test):
            passed += 1
    
    print(f"\n📊 Final Results: {passed}/{len(tests)} test files passed")
    
    if passed == len(tests):
        print("🎉 All EchoForm tests passed! Ready for CLS integration.")
        return 0
    else:
        print("❌ Some tests failed. Check output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())