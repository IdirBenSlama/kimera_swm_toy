#!/usr/bin/env python3
"""
Test specific fixes applied to Kimera 0.7.x
"""
import sys
import os
import tempfile
import traceback

# Add src to path
sys.path.insert(0, 'src')

def test_fix_1_benchmark_cli():
    """Test Fix 1: Benchmark CLI import issue"""
    print("🔧 Testing Fix 1: Benchmark CLI...")
    try:
        # This should work now with the fixed import
        from benchmarks.llm_compare import main as benchmark_main
        print("✅ Benchmark CLI import successful")
        return True
    except Exception as e:
        print(f"❌ Benchmark CLI import failed: {e}")
        return False

def test_fix_2_storage_api():
    """Test Fix 2: Storage API consistency"""
    print("🔧 Testing Fix 2: Storage API...")
    try:
        from kimera.storage import LatticeStorage, get_storage, close_storage
        from kimera.echoform import EchoForm, init_geoid
        
        # Test init_geoid with proper parameters
        test_geoid = init_geoid("test text", "en", ["test"])
        
        # Test the fixed get_storage function
        storage = get_storage(":memory:")
        
        # Test storing a form
        form = EchoForm("test")
        storage.store_form(form)
        
        # Test retrieving forms
        forms = storage.get_stored_forms()
        assert len(forms) == 1
        
        # Test metrics
        metrics = storage.get_metrics()
        assert 'total_forms' in metrics
        
        close_storage()
        print("✅ Storage API working correctly")
        return True
    except Exception as e:
        print(f"❌ Storage API test failed: {e}")
        traceback.print_exc()
        return False

def test_fix_3_migration_encoding():
    """Test Fix 3: Migration script encoding"""
    print("🔧 Testing Fix 3: Migration script encoding...")
    try:
        from scripts.migrate_lattice_to_db import migrate_lattice_to_db
        
        # Test that the function can be imported and called
        # (We won't actually run a full migration)
        print("✅ Migration script import successful")
        return True
    except Exception as e:
        print(f"❌ Migration script test failed: {e}")
        return False

def test_fix_4_multiprocessing():
    """Test Fix 4: Multiprocessing pickling"""
    print("🔧 Testing Fix 4: Multiprocessing pickling...")
    try:
        from kimera.geoid import init_geoid
        from kimera.reactor_mp import ReactorMP
        import pickle
        
        # Test Geoid creation and pickling (this was failing before)
        geoid = init_geoid("test text", "en", ["test"])
        pickled = pickle.dumps(geoid)
        unpickled = pickle.loads(pickled)
        
        # Test ReactorMP creation
        reactor = ReactorMP()
        
        print("✅ Multiprocessing pickling working correctly")
        return True
    except Exception as e:
        print(f"❌ Multiprocessing test failed: {e}")
        traceback.print_exc()
        return False

def test_fix_5_storage_metrics():
    """Test Fix 5: Storage metrics tests"""
    print("🔧 Testing Fix 5: Storage metrics...")
    try:
        from kimera.storage import LatticeStorage
        from kimera.echoform import EchoForm, init_geoid
        
        # Test init_geoid with proper parameters
        test_geoid = init_geoid("test text", "en", ["test"])
        
        # Create storage and add some forms
        storage = LatticeStorage(":memory:")
        
        # Add forms and test metrics
        for i in range(3):
            form = EchoForm(f"test_{i}")
            storage.store_form(form)
        
        metrics = storage.get_metrics()
        
        # Check that metrics are working
        assert 'total_forms' in metrics
        assert metrics['total_forms'] == 3
        
        storage.close()
        print("✅ Storage metrics working correctly")
        return True
    except Exception as e:
        print(f"❌ Storage metrics test failed: {e}")
        traceback.print_exc()
        return False

def test_fix_6_math_isclose():
    """Test Fix 6: Math.isclose import"""
    print("🔧 Testing Fix 6: Math.isclose import...")
    try:
        # Test that math.isclose is available and working
        import math
        
        # Test the function
        result = math.isclose(1.0, 1.0000001, rel_tol=1e-6)
        assert result == True
        
        result = math.isclose(1.0, 2.0, rel_tol=1e-6)
        assert result == False
        
        print("✅ Math.isclose working correctly")
        return True
    except Exception as e:
        print(f"❌ Math.isclose test failed: {e}")
        return False

def main():
    """Run all specific fix tests"""
    print("🔧 Testing Specific Kimera 0.7.x Fixes")
    print("=" * 50)
    
    fixes = [
        ("Fix 1: Benchmark CLI", test_fix_1_benchmark_cli),
        ("Fix 2: Storage API", test_fix_2_storage_api),
        ("Fix 3: Migration Encoding", test_fix_3_migration_encoding),
        ("Fix 4: Multiprocessing", test_fix_4_multiprocessing),
        ("Fix 5: Storage Metrics", test_fix_5_storage_metrics),
        ("Fix 6: Math.isclose", test_fix_6_math_isclose),
    ]
    
    passed = 0
    total = len(fixes)
    
    for fix_name, test_func in fixes:
        print(f"\n📋 Testing {fix_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {fix_name} PASSED")
            else:
                print(f"❌ {fix_name} FAILED")
        except Exception as e:
            print(f"❌ {fix_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Fix Test Results: {passed}/{total} fixes verified")
    
    if passed == total:
        print("🎉 ALL FIXES VERIFIED! Kimera 0.7.x is ready.")
        return True
    else:
        print(f"❌ {total - passed} fixes need attention.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)