#!/usr/bin/env python3
"""
Quick status verification for system health
"""
import os
import subprocess
import sys

def quick_status_verification():
    """Perform quick status verification"""
    print("⚡ QUICK STATUS VERIFICATION")
    print("=" * 35)
    
    checks = []
    
    # Check core source files
    core_files = [
        "src/kimera/identity.py",
        "src/kimera/storage.py", 
        "src/kimera/cls.py",
        "src/kimera/reactor.py"
    ]
    
    print("🔍 Checking core files...")
    core_ok = True
    for file in core_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} MISSING")
            core_ok = False
    checks.append(("Core Files", core_ok))
    
    # Check vault structure
    print("\n🏛️ Checking vault structure...")
    vault_files = [
        "vault/__init__.py",
        "vault/core/__init__.py",
        "vault/core/vault.py",
        "vault/storage/__init__.py"
    ]
    
    vault_ok = True
    for file in vault_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} MISSING")
            vault_ok = False
    checks.append(("Vault Structure", vault_ok))
    
    # Check test structure
    print("\n🧪 Checking test structure...")
    test_dirs = ["tests/unit", "tests/integration", "tests/archive"]
    test_ok = True
    for dir_path in test_dirs:
        if os.path.exists(dir_path):
            test_count = len([f for f in os.listdir(dir_path) if f.endswith('.py')])
            print(f"  ✅ {dir_path} ({test_count} tests)")
        else:
            print(f"  ❌ {dir_path} MISSING")
            test_ok = False
    checks.append(("Test Structure", test_ok))
    
    # Check documentation
    print("\n📚 Checking documentation...")
    doc_files = [
        "docs/status/FINAL_STATUS.md",
        "docs/implementation/SCAR_IMPLEMENTATION_GUIDE.md",
        "docs/TRACEABILITY_INDEX.md"
    ]
    
    doc_ok = True
    for file in doc_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} MISSING")
            doc_ok = False
    checks.append(("Documentation", doc_ok))
    
    # Check scripts organization
    print("\n🔧 Checking scripts organization...")
    script_dirs = [
        "scripts/development",
        "scripts/testing", 
        "scripts/verification",
        "scripts/maintenance"
    ]
    
    scripts_ok = True
    for dir_path in script_dirs:
        if os.path.exists(dir_path):
            script_count = len([f for f in os.listdir(dir_path) if f.endswith('.py')])
            print(f"  ✅ {dir_path} ({script_count} scripts)")
        else:
            print(f"  ❌ {dir_path} MISSING")
            scripts_ok = False
    checks.append(("Scripts Organization", scripts_ok))
    
    # Quick import test
    print("\n🐍 Quick import test...")
    try:
        import sys
        sys.path.insert(0, 'src')
        import kimera.identity
        import kimera.storage
        print("  ✅ Core imports working")
        import_ok = True
    except Exception as e:
        print(f"  ❌ Import failed: {e}")
        import_ok = False
    checks.append(("Core Imports", import_ok))
    
    # Summary
    passed = sum(1 for _, ok in checks if ok)
    total = len(checks)
    
    print(f"\n📊 QUICK STATUS SUMMARY:")
    print(f"  Checks passed: {passed}/{total}")
    print(f"  Success rate: {(passed/total*100):.1f}%")
    
    for name, ok in checks:
        emoji = "✅" if ok else "❌"
        print(f"  {emoji} {name}")
    
    if passed == total:
        print(f"\n🎉 ALL CHECKS PASSED - SYSTEM HEALTHY")
        return True
    else:
        print(f"\n⚠️ {total - passed} CHECKS FAILED - NEEDS ATTENTION")
        return False

if __name__ == "__main__":
    success = quick_status_verification()
    sys.exit(0 if success else 1)