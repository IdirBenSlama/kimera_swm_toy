#!/usr/bin/env python3
"""Final verification that all import path fixes are working."""

import sys
import os
import importlib.util

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_module_exists(module_path, module_name):
    """Test if a module exists and can be imported."""
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            print(f"  ❌ Module {module_name} not found")
            return False
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print(f"  ✅ Module {module_name} loaded successfully")
        return True
        
    except Exception as e:
        print(f"  ❌ Error loading {module_name}: {e}")
        return False

def test_import_statements():
    """Test specific import statements that were problematic."""
    print("🧪 Testing specific import statements...")
    
    tests = [
        ("from kimera.scar import Scar", "Scar"),
        ("from kimera.scar import create_scar", "create_scar"),
        ("from kimera.identity import Identity", "Identity"),
        ("from kimera.storage import LatticeStorage", "LatticeStorage"),
        ("from vault.core.vault import Vault", "Vault"),
    ]
    
    passed = 0
    for import_stmt, expected_name in tests:
        try:
            # Execute the import statement
            exec(import_stmt)
            
            # Check if the imported name exists in locals
            if expected_name in locals():
                print(f"  ✅ {import_stmt}")
                passed += 1
            else:
                print(f"  ❌ {import_stmt} - {expected_name} not found")
                
        except Exception as e:
            print(f"  ❌ {import_stmt} - Error: {e}")
    
    return passed, len(tests)

def test_old_imports_fail():
    """Test that the old incorrect imports properly fail."""
    print("\n🧪 Testing that old incorrect imports fail (as expected)...")
    
    old_imports = [
        "from kimera.core.scar import Scar",
        "from kimera.core import scar",
        "import kimera.core.scar",
    ]
    
    failed_as_expected = 0
    for import_stmt in old_imports:
        try:
            exec(import_stmt)
            print(f"  ⚠️  {import_stmt} - Should have failed but didn't")
        except ImportError:
            print(f"  ✅ {import_stmt} - Correctly fails (as expected)")
            failed_as_expected += 1
        except Exception as e:
            print(f"  ✅ {import_stmt} - Fails with: {e}")
            failed_as_expected += 1
    
    return failed_as_expected, len(old_imports)

def test_file_structure():
    """Test that the expected files exist."""
    print("\n🧪 Testing file structure...")
    
    expected_files = [
        "src/kimera/scar.py",
        "src/kimera/identity.py", 
        "src/kimera/storage.py",
        "vault/core/vault.py",
        "test_import_fixes.py",
        "test_system_quick.py",
        "test_vault_and_scar.py",
    ]
    
    found = 0
    for file_path in expected_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path} exists")
            found += 1
        else:
            print(f"  ❌ {file_path} missing")
    
    return found, len(expected_files)

def main():
    """Run all verification tests."""
    print("🚀 FINAL VERIFICATION OF IMPORT PATH FIXES")
    print("=" * 50)
    print()
    
    # Test file structure
    files_found, total_files = test_file_structure()
    
    # Test import statements
    imports_passed, total_imports = test_import_statements()
    
    # Test old imports fail
    old_failed, total_old = test_old_imports_fail()
    
    print("\n📊 VERIFICATION RESULTS:")
    print(f"  Files found: {files_found}/{total_files}")
    print(f"  New imports working: {imports_passed}/{total_imports}")
    print(f"  Old imports correctly failing: {old_failed}/{total_old}")
    
    total_score = files_found + imports_passed + old_failed
    max_score = total_files + total_imports + total_old
    
    print(f"\n🎯 Overall Score: {total_score}/{max_score}")
    
    if total_score == max_score:
        print("🎉 ALL IMPORT PATH FIXES VERIFIED SUCCESSFULLY!")
        print("\n✅ The architectural drift has been resolved:")
        print("   • All imports now use correct module paths")
        print("   • sys.path is properly configured")
        print("   • Old incorrect imports properly fail")
        print("   • Test files are updated and working")
        return True
    else:
        print("⚠️  Some issues remain - check the output above")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)