#!/usr/bin/env python3
"""
Complete P0 test suite runner
Runs all P0 tests in the correct order with proper error handling
"""

import subprocess
import sys
import os
from pathlib import Path

def run_test(script_name, description, env_vars=None):
    """Run a test script with proper error handling"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    
    # Check if script exists
    if not Path(script_name).exists():
        print(f"⚠️  Script {script_name} not found, skipping...")
        return None
    
    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)
    
    try:
        result = subprocess.run([
            sys.executable, script_name
        ], capture_output=True, text=True, env=env, cwd=Path(__file__).parent)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        success = result.returncode == 0
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"\n{status} - Return Code: {result.returncode}")
        
        return success
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Run the complete P0 test suite"""
    print("🚀 Kimera P0 Complete Test Suite")
    print("Running all P0 tests in sequence...")
    
    # Test sequence
    tests = [
        {
            "script": "simple_p0_test.py",
            "description": "Basic P0 Functionality Test",
            "env": None
        },
        {
            "script": "test_migration_dev.py", 
            "description": "Migration Test with Dual-Write",
            "env": {"KIMERA_ID_DUAL_WRITE": "1"}
        },
        {
            "script": "test_p0_integration.py",
            "description": "P0 Integration Tests",
            "env": None
        },
        {
            "script": "pytest_migration_marker.py",
            "description": "Migration Marker Tests",
            "env": None
        }
    ]
    
    results = []
    
    for i, test in enumerate(tests, 1):
        print(f"\n🔄 Running Test {i}/{len(tests)}")
        
        success = run_test(
            test["script"], 
            test["description"], 
            test["env"]
        )
        
        if success is not None:
            results.append({
                "test": test["description"],
                "success": success
            })
        
        if success is False:
            print(f"\n⚠️  Test {i} failed. Continuing with remaining tests...")
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 FINAL RESULTS")
    print(f"{'='*60}")
    
    passed = 0
    for i, result in enumerate(results, 1):
        status = "✅ PASSED" if result["success"] else "❌ FAILED"
        print(f"{i}. {result['test']}: {status}")
        if result["success"]:
            passed += 1
    
    total = len(results)
    if total == 0:
        print("⚠️  No tests were run")
        return False
        
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL P0 TESTS PASSED!")
        print("✅ Kimera P0 functionality is working correctly")
        print("\nNext steps:")
        print("- Run full benchmark suite")
        print("- Deploy to production environment")
        print("- Monitor metrics and performance")
    else:
        print(f"\n💥 {total - passed} tests failed")
        print("❌ P0 functionality needs attention")
        print("\nRecommended actions:")
        print("- Review failed test outputs above")
        print("- Fix identified issues")
        print("- Re-run this test suite")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)