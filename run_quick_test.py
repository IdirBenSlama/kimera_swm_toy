#!/usr/bin/env python3
"""
Quick test runner to verify our fixes work
"""
import subprocess
import sys
import os

def run_test(script_name):
    """Run a test script and return success status"""
    print(f"\n{'='*50}")
    print(f"🧪 Running {script_name}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, timeout=60)
        
        print(f"Exit code: {result.returncode}")
        
        if result.stdout:
            print("\nOutput:")
            print(result.stdout)
        
        if result.stderr:
            print("\nErrors:")
            print(result.stderr)
        
        success = result.returncode == 0
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"\n{status}")
        
        return success
        
    except subprocess.TimeoutExpired:
        print("❌ TIMEOUT")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Run quick tests"""
    print("🚀 Quick Test Runner")
    
    # Test our fixes
    tests = [
        "test_quick_fixes.py",
        "quick_test_phase193.py", 
        "test_basic_functionality.py",
    ]
    
    results = []
    for test in tests:
        if os.path.exists(test):
            success = run_test(test)
            results.append((test, success))
        else:
            print(f"⚠️  Test file {test} not found, skipping")
            results.append((test, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 SUMMARY")
    print(f"{'='*50}")
    
    passed = 0
    for test, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {test}")
        if success:
            passed += 1
    
    total = len(results)
    print(f"\nPassed: {passed}/{total}")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)