#!/usr/bin/env python3
"""
Validate all applied fixes for Kimera 0.7.x
"""
import sys
import os
import traceback

# Add src to path
sys.path.insert(0, 'src')

def test_imports():
    """Test that all imports work correctly"""
    print("🔍 Testing imports...")
    try:
        # Core imports
        from kimera.echoform import EchoForm, init_geoid
        from kimera.storage import LatticeStorage, get_storage, close_storage
        from kimera.cls import Geoid, lattice_resolve, create_lattice_form
        from kimera.reactor_mp import ReactorMP
        from kimera.__main__ import main
        print("✅ All core imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        traceback.print_exc()
        return False

def test_basic_functionality():
    """Test basic functionality"""
    print("🔍 Testing basic functionality...")
    try:
        # Initialize geoid
        from kimera.echoform import init_geoid, EchoForm
        init_geoid()
        print("✅ Geoid initialization successful")
        
        # Create EchoForm
        form = EchoForm("test")
        print(f"✅ EchoForm created: {form}")
        
        # Test storage
        from kimera.storage import LatticeStorage
        storage = LatticeStorage(":memory:")
        print("✅ Storage created")
        
        # Store and retrieve form
        storage.store_form(form)
        forms = storage.get_stored_forms()
        print(f"✅ Stored and retrieved {len(forms)} forms")
        
        storage.close()
        print("✅ Storage closed")
        
        return True
    except Exception as e:
        print(f"❌ Basic functionality error: {e}")
        traceback.print_exc()
        return False

def test_storage_operations():
    """Test storage operations"""
    print("🔍 Testing storage operations...")
    try:
        from kimera.storage import LatticeStorage, get_storage, close_storage
        from kimera.echoform import EchoForm, init_geoid
        
        init_geoid()
        
        # Test get_storage function
        storage = get_storage(":memory:")
        print("✅ get_storage() works")
        
        # Create and store multiple forms
        forms = [EchoForm(f"test_{i}") for i in range(3)]
        for form in forms:
            storage.store_form(form)
        
        # Retrieve forms
        stored_forms = storage.get_stored_forms()
        print(f"✅ Stored and retrieved {len(stored_forms)} forms")
        
        # Test metrics
        metrics = storage.get_metrics()
        print(f"✅ Storage metrics: {metrics}")
        
        close_storage()
        print("✅ Storage closed via close_storage()")
        
        return True
    except Exception as e:
        print(f"❌ Storage operations error: {e}")
        traceback.print_exc()
        return False

def test_multiprocessing():
    """Test multiprocessing functionality"""
    print("🔍 Testing multiprocessing...")
    try:
        from kimera.reactor_mp import ReactorMP
        from kimera.cls import Geoid
        
        # Create a simple geoid for testing
        geoid = Geoid()
        
        # Test that ReactorMP can be created (but don't run it)
        reactor = ReactorMP()
        print("✅ ReactorMP created successfully")
        
        # Test pickling of Geoid (this was a previous issue)
        import pickle
        pickled = pickle.dumps(geoid)
        unpickled = pickle.loads(pickled)
        print("✅ Geoid pickling/unpickling works")
        
        return True
    except Exception as e:
        print(f"❌ Multiprocessing error: {e}")
        traceback.print_exc()
        return False

def test_cli():
    """Test CLI functionality"""
    print("🔍 Testing CLI...")
    try:
        from kimera.__main__ import main
        
        # Test that main function exists and can be imported
        print("✅ CLI main function imported successfully")
        
        # Test benchmark CLI
        from benchmarks.llm_compare import main as benchmark_main
        print("✅ Benchmark CLI imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ CLI error: {e}")
        traceback.print_exc()
        return False

def test_migration_script():
    """Test migration script"""
    print("🔍 Testing migration script...")
    try:
        from scripts.migrate_lattice_to_db import migrate_lattice_to_db
        print("✅ Migration script imported successfully")
        return True
    except Exception as e:
        print(f"❌ Migration script error: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all validation tests"""
    print("🚀 Kimera 0.7.x Fixes Validation")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Basic Functionality", test_basic_functionality),
        ("Storage Operations", test_storage_operations),
        ("Multiprocessing", test_multiprocessing),
        ("CLI", test_cli),
        ("Migration Script", test_migration_script),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test PASSED")
            else:
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            print(f"❌ {test_name} test FAILED with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Kimera 0.7.x fixes are working correctly.")
        return True
    else:
        print(f"❌ {total - passed} tests failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)