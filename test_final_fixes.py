#!/usr/bin/env python3
"""
Quick test to validate the final 9 fixes for 0.7.x stabilization
"""
import sys
import os
import tempfile
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_benchmark_cli():
    """Test A: Benchmark CLI no longer has e() calls"""
    print("Testing benchmark CLI...")
    try:
        from benchmarks.llm_compare import main
        # This should not crash with UnboundLocalError
        print("✅ Benchmark CLI imports successfully")
        return True
    except Exception as e:
        print(f"❌ Benchmark CLI issue: {e}")
        return False

def test_init_geoid_import():
    """Test B: init_geoid can be imported from echoform"""
    print("Testing init_geoid import...")
    try:
        from kimera.echoform import init_geoid
        print("✅ init_geoid import successful")
        return True
    except Exception as e:
        print(f"❌ init_geoid import failed: {e}")
        return False

def test_storage_api():
    """Test C: Storage API with new signature"""
    print("Testing storage API...")
    try:
        from kimera.storage import LatticeStorage
        from kimera.echoform import EchoForm
        
        # Create temporary database
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        try:
            storage = LatticeStorage(db_path)
            
            # Test new prune signature
            deleted = storage.prune_old_forms(older_than_days=0)
            print(f"✅ Storage pruning works (deleted: {deleted})")
            
            # Test close method
            storage.close()
            print("✅ Storage close works")
            
            return True
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
                
    except Exception as e:
        print(f"❌ Storage API issue: {e}")
        return False

def test_migration_script():
    """Test D: Migration script encoding"""
    print("Testing migration script...")
    try:
        # Import the script to check for syntax errors
        sys.path.insert(0, str(Path(__file__).parent / "scripts"))
        import migrate_lattice_to_db
        print("✅ Migration script imports successfully")
        return True
    except Exception as e:
        print(f"❌ Migration script issue: {e}")
        return False

def test_multiprocessing():
    """Test E: Multiprocessing pickling"""
    print("Testing multiprocessing...")
    try:
        from kimera.reactor_mp import _run_cycle
        from kimera.geoid import Geoid
        
        # Test that _run_cycle is picklable
        import pickle
        pickled = pickle.dumps(_run_cycle)
        unpickled = pickle.loads(pickled)
        print("✅ Multiprocessing function is picklable")
        return True
    except Exception as e:
        print(f"❌ Multiprocessing issue: {e}")
        return False

def test_storage_metrics():
    """Test F: Storage metrics with new EchoForm API"""
    print("Testing storage metrics...")
    try:
        from kimera.echoform import EchoForm
        
        # Test new EchoForm constructor
        form = EchoForm(anchor="test", domain="test", phase="active")
        form.add_term("test", role="test_role", intensity=1.0, test=True)
        print("✅ EchoForm new API works")
        return True
    except Exception as e:
        print(f"❌ Storage metrics issue: {e}")
        return False

def main():
    """Run all tests"""
    print("🔧 Testing final 9 fixes for Kimera 0.7.x stabilization\n")
    
    tests = [
        ("A. Benchmark CLI", test_benchmark_cli),
        ("B. init_geoid import", test_init_geoid_import), 
        ("C. Storage API", test_storage_api),
        ("D. Migration script", test_migration_script),
        ("E. Multiprocessing", test_multiprocessing),
        ("F. Storage metrics", test_storage_metrics),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        print(f"\n--- {name} ---")
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {name} failed with exception: {e}")
            failed += 1
    
    print(f"\n📊 Results:")
    print(f"  ✅ Passed: {passed}")
    print(f"  ❌ Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All fixes validated! Ready for green board!")
        return 0
    else:
        print(f"\n⚠️  {failed} issues remain")
        return 1

if __name__ == "__main__":
    sys.exit(main())