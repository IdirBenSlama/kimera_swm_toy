#!/usr/bin/env python3
"""
Run all verification scripts in sequence
"""

import sys
import os
import subprocess
from pathlib import Path

def run_verification(script_name, description):
    """Run a verification script"""
    print(f"\n{'='*50}")
    print(f"🔍 {description}")
    print('='*50)
    
    if not os.path.exists(script_name):
        print(f"⚠️  Script {script_name} not found - skipping")
        return False
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=False, text=True, timeout=300)
        
        success = result.returncode == 0
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"\n{status} - {description}")
        return success
        
    except subprocess.TimeoutExpired:
        print(f"⏰ TIMEOUT - {description}")
        return False
    except Exception as e:
        print(f"💥 ERROR - {description}: {e}")
        return False

def main():
    """Run all verifications"""
    print("🚀 KIMERA VERIFICATION SUITE")
    
    # Change to project directory
    os.chdir(Path(__file__).parent)
    
    verifications = [
        ("verify_all_fixes.py", "Comprehensive verification of all fixes"),
        ("validate_all_green.py", "Full validation pipeline"),
        ("test_p0_integration.py", "P0 integration test suite"),
    ]
    
    results = []
    for script, description in verifications:
        success = run_verification(script, description)
        results.append((script, success))
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 FINAL RESULTS")
    print('='*50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for script, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {script}")
    
    print(f"\nResults: {passed}/{total} verifications passed")
    
    if passed == total:
        print("\n🎉 ALL VERIFICATIONS PASSED!")
        print("\n✅ KIMERA PROJECT STATUS: FULLY OPERATIONAL")
        print("\n🚀 READY FOR:")
        print("   • poetry run pytest -q")
        print("   • Benchmark testing")
        print("   • Production deployment")
        return True
    else:
        print(f"\n⚠️  {total - passed} verification(s) failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)