#!/usr/bin/env python3
"""
Comprehensive verification suite runner
Executes all verification scripts in sequence
"""

import sys
import subprocess
import os
from pathlib import Path

def run_script(script_name, description):
    """Run a verification script and return success status"""
    print(f"\n{'='*60}")
    print(f"🔍 {description}")
    print('='*60)
    
    try:
        result = subprocess.run([
            sys.executable, script_name
        ], capture_output=False, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            return True
        else:
            print(f"❌ {description} - FAILED (exit code: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - TIMEOUT")
        return False
    except Exception as e:
        print(f"💥 {description} - ERROR: {e}")
        return False

def main():
    """Run the complete verification suite"""
    print("🚀 KIMERA COMPREHENSIVE VERIFICATION SUITE")
    print("=" * 60)
    
    # Change to project directory
    os.chdir(Path(__file__).parent)
    
    # Verification scripts to run
    verifications = [
        ("verify_all_fixes.py", "Comprehensive verification of all fixes"),
        ("validate_all_green.py", "Full validation pipeline"),
        ("test_p0_integration.py", "P0 integration test suite"),
    ]
    
    results = []
    for script, description in verifications:
        if os.path.exists(script):
            success = run_script(script, description)
            results.append((script, success))
        else:
            print(f"⚠️  Script {script} not found - skipping")
            results.append((script, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 VERIFICATION SUMMARY")
    print('='*60)
    
    passed = 0
    total = len(results)
    
    for script, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{script:<30} {status}")
        if success:
            passed += 1
    
    print(f"\nOverall Results: {passed}/{total} verifications passed")
    
    if passed == total:
        print("\n🎉 ALL VERIFICATIONS PASSED!")
        print("\n✅ KIMERA PROJECT STATUS: FULLY OPERATIONAL")
        print("\n🚀 READY FOR:")
        print("   • Production deployment")
        print("   • Benchmark testing")
        print("   • Research applications")
        print("   • Further development")
        
        print("\n📋 RECOMMENDED NEXT STEPS:")
        print("   1. poetry run pytest -q")
        print("   2. Run benchmarks for full functionality validation")
        print("   3. Deploy to production environment")
        
        return True
    else:
        print(f"\n⚠️  {total - passed} verification(s) failed")
        print("   Please address the failing verifications before proceeding")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)