#!/usr/bin/env python3
"""
Quick stabilization check
"""
import sys
import os

# Add src to path
sys.path.insert(0, 'src')

from kimera.utils.safe_console import puts

def check_imports():
    """Check if our key modules import correctly"""
    puts("[CHECK] Checking imports...")
    
    try:
        # Test conftest
        from conftest import fresh_duckdb_path
        puts("[PASS] conftest imports")
        
        # Test storage
        from kimera.storage import LatticeStorage
        puts("[PASS] storage imports")
        
        # Test echoform
        from kimera.echoform import EchoForm
        puts("[PASS] echoform imports")
        
        # Test reactor_mp
        from kimera import reactor_mp
        puts("[PASS] reactor_mp imports")
        
        return True
        
    except Exception as e:
        puts(f"[FAIL] Import failed: {e}")
        return False

def check_basic_functionality():
    """Test basic functionality"""
    puts("\n[TEST] Testing basic functionality...")
    
    try:
        from conftest import fresh_duckdb_path
        from kimera.storage import LatticeStorage
        from kimera.echoform import EchoForm
        
        # Test storage creation and close
        db_path = fresh_duckdb_path()
        storage = LatticeStorage(db_path)
        storage.close()
        
        # Test EchoForm
        form = EchoForm("test")
        form.add_term("symbol", role="test", intensity=1.0)
        
        # Cleanup
        if os.path.exists(db_path):
            os.remove(db_path)
        
        puts("[PASS] Basic functionality works")
        return True
        
    except Exception as e:
        puts(f"[FAIL] Basic functionality failed: {e}")
        return False

def check_files():
    """Check critical files exist"""
    puts("\n[FILES] Checking critical files...")
    
    files = [
        "conftest.py",
        "src/kimera/storage.py",
        "src/kimera/echoform.py", 
        "src/kimera/reactor_mp.py",
    ]
    
    all_exist = True
    for filepath in files:
        exists = os.path.exists(filepath)
        status = "[PASS]" if exists else "[FAIL]"
        puts(f"{status} {filepath}")
        if not exists:
            all_exist = False
    
    return all_exist

def main():
    """Run stabilization check"""
    puts("[START] Kimera v0.7.x Stabilization Check")
    puts("=" * 40)
    
    files_ok = check_files()
    imports_ok = check_imports()
    functionality_ok = check_basic_functionality()
    
    puts(f"\n[STATS] Results:")
    puts(f"   Files: {'[PASS]' if files_ok else '[FAIL]'}")
    puts(f"   Imports: {'[PASS]' if imports_ok else '[FAIL]'}")
    puts(f"   Functionality: {'[PASS]' if functionality_ok else '[FAIL]'}")
    
    if files_ok and imports_ok and functionality_ok:
        puts(f"\n[SUCCESS] STABILIZATION SUCCESSFUL!")
        puts(f"   All critical components are working")
        return True
    else:
        puts(f"\n[ERROR] Issues remain")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)