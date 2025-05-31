#!/usr/bin/env python3
"""
Test basic functionality to ensure everything works
"""
import sys
import os
sys.path.insert(0, 'src')

def main():
    print("🧪 Testing Basic Functionality")
    print("=" * 30)
    
    try:
        # Test 1: Import all modules
        print("1. Testing imports...")
        from kimera.storage import get_storage, close_storage
        from kimera.echoform import EchoForm
        from kimera.geoid import init_geoid
        from kimera.cls import lattice_resolve
        print("   ✅ All imports successful")
        
        # Test 2: Create storage
        print("2. Testing storage creation...")
        if os.path.exists("test_basic.db"):
            os.remove("test_basic.db")
        storage = get_storage("test_basic.db")
        print("   ✅ Storage created successfully")
        
        # Test 3: Create and store a form
        print("3. Testing form creation and storage...")
        form = EchoForm(
            anchor="test_basic",
            domain="test",
            terms=[{"symbol": "test", "role": "basic", "intensity": 1.0}],
            phase="testing"
        )
        storage.store_form(form)
        print("   ✅ Form stored successfully")
        
        # Test 4: Retrieve form
        print("4. Testing form retrieval...")
        retrieved = storage.fetch_form("test_basic")
        assert retrieved is not None
        assert retrieved.anchor == "test_basic"
        print("   ✅ Form retrieved successfully")
        
        # Test 5: Test CLS functionality
        print("5. Testing CLS functionality...")
        geo_a = init_geoid("Test A", "en", ["test"])
        geo_b = init_geoid("Test B", "en", ["test"])
        intensity = lattice_resolve(geo_a, geo_b)
        print(f"   ✅ CLS resolve returned intensity: {intensity}")
        
        # Test 6: List forms
        print("6. Testing form listing...")
        forms = storage.list_forms(limit=5)
        print(f"   ✅ Found {len(forms)} forms")
        
        close_storage()
        print("\n🎉 All basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Clean up
        if os.path.exists("test_basic.db"):
            os.remove("test_basic.db")


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)