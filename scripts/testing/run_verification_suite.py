#!/usr/bin/env python3
"""
Comprehensive verification test suite
"""
import subprocess
import sys
import os

def run_verification_suite():
    """Run comprehensive verification suite"""
    print("🔍 RUNNING VERIFICATION SUITE")
    print("=" * 40)
    
    verification_tests = [
        "run_verification.py",
        "run_complete_verification.py",
        "run_all_verifications.py",
        "quick_verification_test.py",
        "final_verification.py"
    ]
    
    results = []
    for test in verification_tests:
        # Check multiple locations
        test_paths = [test, f"scripts/{test}", f"scripts/verification/{test}"]
        test_found = False
        
        for path in test_paths:
            if os.path.exists(path):
                print(f"🔍 Running {test}...")
                try:
                    result = subprocess.run([sys.executable, path], 
                                          capture_output=True, text=True, timeout=60)
                    if result.returncode == 0:
                        print(f"✅ {test} PASSED")
                        results.append((test, "PASSED"))
                    else:
                        print(f"❌ {test} FAILED")
                        if result.stderr:
                            print(f"   Error: {result.stderr[:100]}...")
                        results.append((test, "FAILED"))
                    test_found = True
                    break
                except subprocess.TimeoutExpired:
                    print(f"⏰ {test} TIMEOUT")
                    results.append((test, "TIMEOUT"))
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
    total = len([r for r in results if r[1] not in ["NOT_FOUND"]])
    
    print(f"\n📊 VERIFICATION SUITE SUMMARY:")
    print(f"  Tests run: {total}")
    print(f"  Passed: {passed}")
    print(f"  Success rate: {(passed/total*100) if total > 0 else 0:.1f}%")
    
    status_counts = {}
    for _, status in results:
        status_counts[status] = status_counts.get(status, 0) + 1
    
    for status, count in status_counts.items():
        if status != "NOT_FOUND":
            emoji = {"PASSED": "✅", "FAILED": "❌", "ERROR": "💥", "TIMEOUT": "⏰"}.get(status, "❓")
            print(f"  {emoji} {status}: {count}")
    
    return passed == total if total > 0 else False

if __name__ == "__main__":
    success = run_verification_suite()
    sys.exit(0 if success else 1)