#!/usr/bin/env python3
"""
Execute comprehensive verification
"""
import subprocess
import sys
import os

def execute_verification():
    """Execute comprehensive system verification"""
    print("✅ EXECUTING COMPREHENSIVE VERIFICATION")
    print("=" * 50)
    
    verifications = [
        ("Import Verification", "verify_import_fixes.py"),
        ("Unicode Verification", "verify_unicode_fix.py"),
        ("SCAR Verification", "verify_scar_implementation.py"),
        ("P0 Verification", "verify_p0_fixes.py")
    ]
    
    results = []
    for name, script in verifications:
        if os.path.exists(script):
            print(f"🔍 Running {name}...")
            try:
                result = subprocess.run([sys.executable, script], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {name} PASSED")
                    results.append((name, "PASSED"))
                else:
                    print(f"❌ {name} FAILED: {result.stderr}")
                    results.append((name, "FAILED"))
            except Exception as e:
                print(f"❌ {name} ERROR: {e}")
                results.append((name, "ERROR"))
        else:
            print(f"⚠️ {script} not found")
            results.append((name, "NOT_FOUND"))
    
    # Summary
    passed = sum(1 for _, status in results if status == "PASSED")
    total = len(results)
    
    print(f"\n📊 VERIFICATION SUMMARY:")
    print(f"  Passed: {passed}/{total}")
    for name, status in results:
        emoji = "✅" if status == "PASSED" else "❌" if status == "FAILED" else "⚠️"
        print(f"  {emoji} {name}: {status}")
    
    if passed == total:
        print(f"\n🎉 ALL VERIFICATIONS PASSED!")
        return True
    else:
        print(f"\n⚠️ {total - passed} verifications need attention")
        return False

if __name__ == "__main__":
    execute_verification()