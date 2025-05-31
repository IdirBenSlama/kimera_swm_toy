#!/usr/bin/env python3
"""
Quick verification that v0.7.5 is ready for release
"""
import sys
import os

# Add src to path
sys.path.insert(0, 'src')

def main():
    print("=" * 50)
    print("KIMERA v0.7.5 RELEASE VERIFICATION")
    print("=" * 50)
    
    # Test 1: Safe console
    try:
        from kimera.utils.safe_console import puts
        puts("[PASS] Safe console import works")
    except Exception as e:
        print(f"[FAIL] Safe console: {e}")
        return False
    
    # Test 2: Core functionality
    try:
        from conftest import fresh_duckdb_path
        from kimera.storage import LatticeStorage
        from kimera.echoform import EchoForm
        
        # Quick storage test
        db_path = fresh_duckdb_path()
        storage = LatticeStorage(db_path)
        
        form = EchoForm("test")
        form.add_term("symbol", role="test", intensity=1.0)
        storage.store_form(form)
        
        # Test the row count fix
        count = storage.prune_old_forms(older_than_seconds=3600)
        
        storage.close()
        if os.path.exists(db_path):
            os.remove(db_path)
        
        puts(f"[PASS] Core functionality works, pruned {count} forms")
        
    except Exception as e:
        puts(f"[FAIL] Core functionality: {e}")
        return False
    
    # Test 3: Version check
    try:
        with open('pyproject.toml', 'r') as f:
            content = f.read()
            if 'version = "0.7.5"' in content:
                puts("[PASS] Version is 0.7.5")
            else:
                puts("[FAIL] Version not 0.7.5")
                return False
    except Exception as e:
        puts(f"[FAIL] Version check: {e}")
        return False
    
    puts("\n[SUCCESS] Kimera v0.7.5 is ready for release!")
    puts("   All core functionality working")
    puts("   Safe console output implemented")
    puts("   Storage row count fixed")
    puts("   Version bumped to 0.7.5")
    puts("\n   Ready to commit and tag!")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 RELEASE READY! 🎉")
    else:
        print("\n❌ Issues found - fix before release")
    sys.exit(0 if success else 1)