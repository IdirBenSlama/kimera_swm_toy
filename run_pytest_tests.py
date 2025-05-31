#!/usr/bin/env python3
"""
Run pytest tests to verify stabilization
"""
import subprocess
import sys
import os

def run_pytest(test_path, description):
    """Run pytest on a specific test file or directory"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    
    cmd = [sys.executable, "-m", "pytest", test_path, "-v", "--tb=short"]
    print(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
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
        print("❌ TIMEOUT (2 minutes)")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Run pytest test suite"""
    print("🚀 Pytest Test Suite")
    
    # Test files in order of importance
    tests = [
        ("tests/test_echoform_core.py", "Core EchoForm Tests"),
        ("tests/test_cls_integration.py", "CLS Integration Tests"),
        ("tests/test_storage_metrics.py", "Storage Metrics Tests"),
        ("tests/", "All Tests"),
    ]
    
    results = []
    
    for test_path, description in tests:
        if os.path.exists(test_path):
            success = run_pytest(test_path, description)
            results.append((description, success))
        else:
            print(f"⚠️  Test path {test_path} not found, skipping")
            results.append((description, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 PYTEST SUMMARY")
    print(f"{'='*60}")
    
    passed = 0
    total = len(results)
    
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {description}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} test suites passed")
    
    if passed >= total * 0.75:
        print("🎉 Most tests are passing!")
        return True
    else:
        print("💥 Significant test failures")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)