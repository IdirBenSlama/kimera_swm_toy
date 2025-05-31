#!/usr/bin/env python3
"""
Comprehensive test script to validate all v0.7.3 fixes including pytest
"""
import subprocess
import sys

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
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, timeout=60)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Test timed out"
    except Exception as e:
        return False, "", str(e)

def run_pytest():
    """Run pytest and return success status"""
    try:
        result = subprocess.run([sys.executable, "-m", "pytest", "-q", "tests/"], 
                              capture_output=True, text=True, timeout=120)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Pytest timed out"
    except Exception as e:
        return False, "", str(e)

def main():
    safe_print("Comprehensive v0.7.3 Testing...")
    safe_print("=" * 35)
    
    # Test individual scripts
    scripts = [
        "quick_test_phase192.py",
        "validate_v073.py"
    ]
    
    passed = 0
    total = len(scripts) + 1  # +1 for pytest
    
    for script in scripts:
        safe_print(f"\nRunning {script}...")
        success, stdout, stderr = run_test(script)
        
        if success:
            safe_print(f"✅ {script} passed")
            passed += 1
        else:
            safe_print(f"❌ {script} failed:")
            if stderr:
                safe_print(stderr)
            if stdout:
                safe_print(stdout)
    
    # Test pytest
    safe_print(f"\nRunning pytest tests...")
    success, stdout, stderr = run_pytest()
    
    if success:
        safe_print(f"✅ pytest passed")
        passed += 1
    else:
        safe_print(f"❌ pytest failed:")
        if stderr:
            safe_print(stderr)
        if stdout:
            safe_print(stdout)
    
    safe_print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        safe_print("\n🎉 All fixes working! Ready to commit v0.7.3")
        safe_print("\nNext steps:")
        safe_print("  1. python commit_v073.py")
        safe_print("  2. powershell -ExecutionPolicy Bypass -File push_v073.ps1")
        return True
    else:
        safe_print(f"\n❌ {total - passed} test(s) failed. Fix before committing.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)