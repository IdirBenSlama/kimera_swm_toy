#!/usr/bin/env python3
"""
Quick test runner for rapid validation
"""
import subprocess
import sys
import os

def run_quick_test():
    """Run quick validation tests"""
    print("🚀 RUNNING QUICK TESTS")
    print("=" * 30)
    
    quick_tests = [
        "test_basic_quick.py",
        "test_quick_run.py", 
        "test_system_quick.py",
        "minimal_test.py",
        "simple_test.py"
    ]
    
    results = []
    for test in quick_tests:
        # Check in current directory and tests directory
        test_paths = [test, f"tests/{test}", f"tests/archive/{test}"]
        test_found = False
        
        for path in test_paths:
            if os.path.exists(path):
                print(f"🧪 Running {test}...")
                try:
                    result = subprocess.run([sys.executable, path], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"✅ {test} PASSED")
                        results.append((test, "PASSED"))
                    else:
                        print(f"❌ {test} FAILED")
                        results.append((test, "FAILED"))
                    test_found = True
                    break
                except Exception as e:
                    print(f"❌ {test} ERROR: {e}")
                    results.append((test, "ERROR"))
                    test_found = True
                    break
        
        if not test_found:
            print(f"⚠️ {test} not found")
            results.append((test, "NOT_FOUND"))
    
    # Summary
    passed = sum(1 for _, status in results if status == "PASSED")
    total = len([r for r in results if r[1] != "NOT_FOUND"])
    
    print(f"\n📊 QUICK TEST SUMMARY:")
    print(f"  Tests run: {total}")
    print(f"  Passed: {passed}")
    print(f"  Success rate: {(passed/total*100) if total > 0 else 0:.1f}%")
    
    for test, status in results:
        if status != "NOT_FOUND":
            emoji = "✅" if status == "PASSED" else "❌"
            print(f"  {emoji} {test}")
    
    return passed == total if total > 0 else False

if __name__ == "__main__":
    success = run_quick_test()
    sys.exit(0 if success else 1)