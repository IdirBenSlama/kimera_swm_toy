#!/usr/bin/env python3
"""
Complete Verification Runner
Runs all verification scripts and provides comprehensive report
"""

import sys
import os
import subprocess
from pathlib import Path

def run_script_safely(script_name, description, timeout=120):
    """Run a script safely with error handling"""
    if not os.path.exists(script_name):
        return False, f"Script {script_name} not found"
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, timeout=timeout)
        
        success = result.returncode == 0
        message = "Success" if success else f"Failed (exit {result.returncode})"
        
        if not success and result.stderr:
            message += f": {result.stderr[:200]}..."
        
        return success, message
        
    except subprocess.TimeoutExpired:
        return False, f"Timeout after {timeout}s"
    except Exception as e:
        return False, f"Error: {e}"

def main():
    """Run complete verification suite"""
    print("🚀 KIMERA COMPLETE VERIFICATION SUITE")
    print("=" * 60)
    
    # Change to project directory
    os.chdir(Path(__file__).parent)
    
    # Verification scripts to run
    verifications = [
        ("project_status_summary.py", "Project Status Summary", 30),
        ("final_verification.py", "Final Comprehensive Verification", 180),
        ("simple_identity_test.py", "Simple Identity Test", 60),
        ("test_p0_integration.py", "P0 Integration Tests", 180),
    ]
    
    print("📋 Running verification scripts...")
    print("-" * 60)
    
    results = []
    for script, description, timeout in verifications:
        print(f"\n🔍 {description}")
        print(f"   Running: {script}")
        
        success, message = run_script_safely(script, description, timeout)
        results.append((script, description, success, message))
        
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   {status}: {message}")
    
    # Summary Report
    print(f"\n{'='*60}")
    print("📊 VERIFICATION SUMMARY REPORT")
    print('='*60)
    
    passed = 0
    total = len(results)
    
    for script, description, success, message in results:
        status = "✅" if success else "❌"
        print(f"{status} {description}")
        if not success:
            print(f"     Issue: {message}")
        if success:
            passed += 1
    
    print(f"\nResults: {passed}/{total} verifications passed")
    
    # Final Assessment
    print(f"\n{'='*60}")
    print("🎯 FINAL ASSESSMENT")
    print('='*60)
    
    if passed == total:
        print("🎉 ALL VERIFICATIONS PASSED!")
        print("\n✅ KIMERA PROJECT STATUS: FULLY OPERATIONAL")
        print("\n🚀 SYSTEM CAPABILITIES:")
        print("   • Unified Identity Model")
        print("   • Entropy-Adaptive Time Decay")
        print("   • Lattice-Based Resolution")
        print("   • Comprehensive Storage")
        print("   • Production-Ready Architecture")
        
        print("\n📋 READY FOR:")
        print("   • poetry run pytest -q")
        print("   • Production deployment")
        print("   • Research applications")
        print("   • Performance benchmarking")
        
        print("\n🎯 NEXT STEPS:")
        print("   1. poetry run pytest -q  # Run full test suite")
        print("   2. Deploy to production environment")
        print("   3. Begin research phase")
        print("   4. Run performance benchmarks")
        
        return True
        
    elif passed >= total * 0.75:
        print("⚠️  MOSTLY OPERATIONAL - Minor issues to address")
        print(f"   {total - passed} verification(s) failed")
        print("   System is largely functional but needs attention")
        return False
        
    else:
        print("❌ SIGNIFICANT ISSUES DETECTED")
        print(f"   {total - passed} verification(s) failed")
        print("   Please address failing verifications before proceeding")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n{'='*60}")
    if success:
        print("🎉 KIMERA PROJECT: VERIFICATION COMPLETE - ALL SYSTEMS GO!")
    else:
        print("⚠️  KIMERA PROJECT: ISSUES DETECTED - REVIEW REQUIRED")
    print('='*60)
    sys.exit(0 if success else 1)