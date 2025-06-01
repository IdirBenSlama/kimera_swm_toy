#!/usr/bin/env python3
"""
Comprehensive test runner for P0 verification
"""

import subprocess
import sys
import os
from pathlib import Path

def run_test_script(script_name, description):
    """Run a test script and return the result"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"Running: {script_name}")
    print('='*60)
    
    try:
        result = subprocess.run([
            sys.executable, script_name
        ], capture_output=True, text=True, timeout=120)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)
        
        success = result.returncode == 0
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"\n{status} (exit code: {result.returncode})")
        
        return success
        
    except subprocess.TimeoutExpired:
        print("❌ TIMEOUT - Test took longer than 2 minutes")
        return False
    except FileNotFoundError:
        print(f"❌ FILE NOT FOUND - {script_name} does not exist")
        return False
    except Exception as e:
        print(f"❌ ERROR - Failed to run test: {e}")
        return False

def main():
    """Run all verification tests"""
    print("🚀 P0 Comprehensive Verification Suite")
    print("🎯 Testing all critical fixes and functionality")
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Define test suite
    tests = [
        ("basic_import_test.py", "Basic Import Test - Core module imports"),
        ("test_storage_fix.py", "Storage Connection Management - P0 Critical Fix"),
        ("quick_verification_test.py", "Quick Verification - Basic functionality"),
        ("test_unified_identity.py", "Unified Identity System - Core feature"),
        ("test_v073_storage.py", "Storage Test Suite - All storage functions"),
        ("verify_p0_fixes.py", "P0 Fix Verification - Comprehensive check"),
    ]
    
    results = []
    
    for script, description in tests:
        success = run_test_script(script, description)
        results.append((script, description, success))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 FINAL RESULTS SUMMARY")
    print('='*60)
    
    passed = 0
    total = len(results)
    
    for script, description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {script:<25} - {description}")
        if success:
            passed += 1
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! P0 verification successful!")
        return 0
    else:
        print("⚠️  Some tests failed. P0 needs attention.")
        return 1

if __name__ == "__main__":
    sys.exit(main())