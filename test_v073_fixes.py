#!/usr/bin/env python3
"""
Test the v0.7.3 fixes before committing
"""
import sys
import subprocess

def safe_print(message):
    """Safe print function that handles Unicode issues on Windows"""
    try:
        print(message)
    except UnicodeEncodeError:
        # Fallback: replace problematic characters
        safe_message = message.encode('ascii', 'replace').decode('ascii')
        print(safe_message)

def run_test(script_name):
    """Run a test script and return success status"""
    safe_print(f"\nRunning {script_name}...")
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            safe_print(f"✅ {script_name} passed")
            return True
        else:
            safe_print(f"❌ {script_name} failed:")
            safe_print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        safe_print(f"❌ {script_name} timed out")
        return False
    except Exception as e:
        safe_print(f"❌ {script_name} crashed: {e}")
        return False

def main():
    """Test all the fixed scripts"""
    safe_print("Testing v0.7.3 fixes...")
    safe_print("=" * 30)
    
    tests = [
        "quick_test_phase192.py",
        "validate_v073.py"
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if run_test(test):
            passed += 1
    
    safe_print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        safe_print("\n🎉 All fixes working! Ready to commit v0.7.3")
        return True
    else:
        safe_print(f"\n❌ {total - passed} test(s) failed. Fix before committing.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)