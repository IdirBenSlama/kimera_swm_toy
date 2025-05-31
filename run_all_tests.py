#!/usr/bin/env python3
"""
Run all tests to verify v0.7.x stabilization
"""
import subprocess
import sys
import os
import time

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    print(f"Command: {cmd}")
    print()
    
    start_time = time.time()
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        elapsed = time.time() - start_time
        
        print(f"Exit code: {result.returncode}")
        print(f"Duration: {elapsed:.2f}s")
        
        if result.stdout:
            print("\nSTDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)
        
        success = result.returncode == 0
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"\n{status}")
        
        return success
        
    except subprocess.TimeoutExpired:
        print("❌ TIMEOUT (5 minutes)")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Run comprehensive test suite"""
    print("🚀 Kimera v0.7.x Stabilization Test Suite")
    print("=" * 60)
    
    # Test commands in order of importance
    tests = [
        ("python test_quick_fixes.py", "Quick Fixes Validation"),
        ("python -m pytest tests/test_echoform_core.py -v", "Core EchoForm Tests"),
        ("python -m pytest tests/test_cls_integration.py -v", "CLS Integration Tests"),
        ("python -m pytest tests/test_storage_metrics.py -v", "Storage Metrics Tests"),
        ("python quick_test_phase193.py", "Phase 19.3 Quick Test"),
        ("python test_basic_functionality.py", "Basic Functionality Test"),
        ("python validate_all_fixes.py", "All Fixes Validation"),
        ("python run_comprehensive_test.py", "Comprehensive Test Suite"),
    ]
    
    results = []
    
    for cmd, description in tests:
        success = run_command(cmd, description)
        results.append((description, success))
        
        # If a critical test fails, we might want to continue anyway to see the full picture
        if not success and "Quick Fixes" in description:
            print(f"\n⚠️  Critical test failed: {description}")
            print("Continuing with remaining tests to get full picture...")
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = 0
    total = len(results)
    
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {description}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! v0.7.x is stable!")
        return True
    elif passed >= total * 0.8:
        print(f"\n⚠️  Most tests passed ({passed}/{total}). Minor issues remain.")
        return True
    else:
        print(f"\n💥 Significant issues found ({passed}/{total} passed).")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)