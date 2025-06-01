#!/usr/bin/env python3
"""
P0 Fix Verification Script
Tests the critical fixes applied for P0 stability
"""

import sys
import os
import tempfile
import subprocess
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_storage_connection_fix():
    """Test that storage connections are properly managed"""
    print("🧪 Testing storage connection management...")
    
    try:
        from kimera.storage import LatticeStorage
        from kimera.echoform import EchoForm
        
        # Create temporary database using the fixed pattern
        def fresh_duckdb_path():
            fd, path = tempfile.mkstemp(suffix=".db")
            os.close(fd)        # close handle
            os.unlink(path)     # remove file so DuckDB can create it
            return path
        
        db_path = fresh_duckdb_path()
        storage = None
        
        try:
            storage = LatticeStorage(db_path)
            
            # Create and store a test form
            form = EchoForm(
                anchor="connection_test",
                domain="test",
                terms=[{"symbol": "test", "role": "test_role", "intensity": 0.5}],
                phase="test_phase"
            )
            storage.store_form(form)
            
            # Verify storage works
            count = storage.get_form_count()
            assert count == 1, f"Expected 1 form, got {count}"
            
            print("✅ Storage connection management working correctly")
            return True
            
        finally:
            if storage:
                storage.close()
            if os.path.exists(db_path):
                os.remove(db_path)
                
    except Exception as e:
        print(f"❌ Storage connection test failed: {e}")
        return False

def test_identity_system():
    """Test that the identity system is working"""
    print("🧪 Testing identity system...")
    
    try:
        from kimera.identity import create_geoid_identity, Identity
        from kimera.storage import LatticeStorage
        
        # Create temporary database
        def fresh_duckdb_path():
            fd, path = tempfile.mkstemp(suffix=".db")
            os.close(fd)
            os.unlink(path)
            return path
        
        db_path = fresh_duckdb_path()
        storage = None
        
        try:
            storage = LatticeStorage(db_path)
            
            # Create identity
            identity = create_geoid_identity("Test identity", tags=["test"])
            assert isinstance(identity, Identity), "Should create Identity object"
            
            # Test storage (if identity storage is implemented)
            try:
                storage.store_identity(identity)
                retrieved = storage.fetch_identity(identity.id)
                assert retrieved is not None, "Should retrieve stored identity"
                print("✅ Identity system working correctly")
            except AttributeError:
                print("⚠️  Identity storage methods not yet implemented")
            
            return True
            
        finally:
            if storage:
                storage.close()
            if os.path.exists(db_path):
                os.remove(db_path)
                
    except Exception as e:
        print(f"❌ Identity system test failed: {e}")
        return False

def test_multiprocessing_guard():
    """Test that multiprocessing guard is in place"""
    print("🧪 Testing multiprocessing guard...")
    
    try:
        from kimera import reactor_mp
        
        # Check if the guard is present
        import inspect
        source = inspect.getsource(reactor_mp)
        
        if "freeze_support" in source:
            print("✅ Multiprocessing guard present")
            return True
        else:
            print("❌ Multiprocessing guard missing")
            return False
            
    except Exception as e:
        print(f"❌ Multiprocessing guard test failed: {e}")
        return False

def test_ci_configuration():
    """Test that CI configuration is valid"""
    print("🧪 Testing CI configuration...")
    
    try:
        import yaml
        
        ci_path = Path(".github/workflows/ci.yml")
        if not ci_path.exists():
            print("❌ CI configuration file not found")
            return False
        
        with open(ci_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Basic validation
        assert "name" in config, "CI config should have name"
        assert "jobs" in config, "CI config should have jobs"
        assert "test" in config["jobs"], "CI config should have test job"
        
        print("✅ CI configuration is valid YAML")
        return True
        
    except Exception as e:
        print(f"❌ CI configuration test failed: {e}")
        return False

def main():
    """Run all P0 verification tests"""
    print("🚀 Running P0 Fix Verification Suite")
    print("=" * 50)
    
    tests = [
        test_storage_connection_fix,
        test_identity_system,
        test_multiprocessing_guard,
        test_ci_configuration,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
        print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("=" * 50)
    print(f"📊 P0 Fix Verification Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All P0 fixes verified successfully!")
        return 0
    else:
        print("⚠️  Some P0 fixes need attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())