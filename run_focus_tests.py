#!/usr/bin/env python3
"""
Run the focus set of tests after applying v0.7.x stabilization patches
"""
import sys
import subprocess
import os

def run_test(test_name, test_path):
    """Run a single test and return success status"""
    print(f"\n{'='*60}")
    print(f"🧪 Running {test_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([
            sys.executable, test_path
        ], capture_output=True, text=True, timeout=60)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {test_name} PASSED")
            return True
        else:
            print(f"❌ {test_name} FAILED (exit code: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {test_name} TIMED OUT")
        return False
    except Exception as e:
        print(f"💥 {test_name} ERROR: {e}")
        return False

def main():
    """Run the focus test set"""
    print("🎯 Running Focus Test Set for v0.7.x Stabilization")
    print("=" * 60)
    
    # Focus test set from the user's specification
    focus_tests = [
        ("Basic Storage", "quick_test_storage.py"),
        ("Phase 19.3 Storage", "quick_test_phase193.py"),
        ("V0.7.3 Storage", "test_v073_storage.py"),
        ("V0.7.4 Validation", "validate_v074.py"),
        ("All Fixes Validation", "validate_all_fixes.py"),
    ]
    
    results = []
    
    for test_name, test_path in focus_tests:
        if os.path.exists(test_path):
            success = run_test(test_name, test_path)
            results.append((test_name, success))
        else:
            print(f"⚠️  Test file not found: {test_path}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 FOCUS TEST RESULTS SUMMARY")
    print(f"{'='*60}")
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status:8} {test_name}")
        if success:
            passed += 1
    
    print(f"\n📈 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL FOCUS TESTS PASSED! Version 0.7.x is STABLE!")
        return True
    else:
        print("💥 Some tests failed. Version 0.7.x needs more work.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)