#!/usr/bin/env python3
"""
Quick test to verify storage functionality works
"""
import sys
import os
sys.path.insert(0, 'src')

def test_basic_storage():
    """Test basic storage operations"""
    print("Testing basic storage...")
    
    try:
        from kimera.storage import get_storage, close_storage
        from kimera.echoform import EchoForm
        
        # Clean up any existing test database
        if os.path.exists("test_storage.db"):
            os.remove("test_storage.db")
        
        # Get storage instance
        storage = get_storage("test_storage.db")
        
        # Create a test form
        form = EchoForm(
            anchor="test_basic",
            domain="test",
            terms=[{"symbol": "test", "role": "basic", "intensity": 1.0}],
            phase="testing"
        )
        
        # Store it
        storage.store_form(form)
        print("✅ Form stored successfully")
        
        # Fetch it back
        retrieved = storage.fetch_form("test_basic")
        assert retrieved is not None
        assert retrieved.anchor == "test_basic"
        assert retrieved.domain == "test"
        print("✅ Form retrieved successfully")
        
        # List forms
        forms = storage.list_forms(limit=5)
        assert len(forms) == 1
        assert forms[0]["anchor"] == "test_basic"
        print("✅ Form listing works")
        
        # Count forms
        count = storage.get_form_count()
        assert count == 1
        print("✅ Form counting works")
        
        close_storage()
        print("✅ Storage closed successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Storage test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Clean up
        if os.path.exists("test_storage.db"):
            os.remove("test_storage.db")


def test_cls_integration():
    """Test CLS with storage"""
    print("\nTesting CLS integration...")
    
    try:
        from kimera.storage import get_storage, close_storage
        from kimera.geoid import init_geoid
        from kimera.cls import lattice_resolve
        
        # Clean up any existing test database
        if os.path.exists("test_cls.db"):
            os.remove("test_cls.db")
        
        # Get storage instance
        storage = get_storage("test_cls.db")
        
        # Create test geoids
        geo_a = init_geoid("Test A", "en", ["test"])
        geo_b = init_geoid("Test B", "en", ["test"])
        
        # Test lattice resolve
        intensity1 = lattice_resolve(geo_a, geo_b)
        print(f"First resolve: {intensity1}")
        
        intensity2 = lattice_resolve(geo_a, geo_b)
        print(f"Second resolve: {intensity2}")
        
        # Verify intensities increased
        assert intensity2 > intensity1
        print("✅ CLS integration works")
        
        close_storage()
        return True
        
    except Exception as e:
        print(f"❌ CLS test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Clean up
        if os.path.exists("test_cls.db"):
            os.remove("test_cls.db")


def main():
    print("🧪 Quick Storage Test")
    print("=" * 20)
    
    success1 = test_basic_storage()
    success2 = test_cls_integration()
    
    if success1 and success2:
        print("\n🎉 All tests passed! Storage is working correctly.")
        return True
    else:
        print("\n💥 Some tests failed.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)