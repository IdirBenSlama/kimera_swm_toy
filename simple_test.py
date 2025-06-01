#!/usr/bin/env python3
"""
Simple test to verify basic functionality
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_basic_imports():
    """Test basic imports"""
    print("Testing basic imports...")
    
    try:
        from kimera.storage import LatticeStorage
        print("✅ LatticeStorage import successful")
        
        from kimera.echoform import EchoForm
        print("✅ EchoForm import successful")
        
        from kimera.identity import Identity, create_geoid_identity
        print("✅ Identity imports successful")
        
        from kimera.geoid import init_geoid
        print("✅ Geoid import successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_storage_basic():
    """Test basic storage functionality"""
    print("Testing basic storage...")
    
    try:
        import tempfile
        import os
        from kimera.storage import LatticeStorage
        from kimera.echoform import EchoForm
        
        # Create temporary database
        fd, db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        os.unlink(db_path)
        
        storage = None
        try:
            storage = LatticeStorage(db_path)
            print("✅ Storage created successfully")
            
            # Test basic operation
            count = storage.get_form_count()
            print(f"✅ Form count: {count}")
            
            return True
            
        finally:
            if storage:
                storage.close()
            if os.path.exists(db_path):
                os.remove(db_path)
                
    except Exception as e:
        print(f"❌ Storage test failed: {e}")
        return False

def main():
    """Run simple tests"""
    print("🚀 Running Simple Verification Tests")
    print("=" * 40)
    
    tests = [test_basic_imports, test_storage_basic]
    results = []
    
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
        print()
    
    passed = sum(results)
    total = len(results)
    
    print("=" * 40)
    print(f"Results: {passed}/{total} tests passed")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())