#!/usr/bin/env python3
"""
Direct test of quick validation
"""
import sys
import os

# Add src to path
sys.path.insert(0, 'src')

def main():
    print("🔍 Testing Quick Validation...")
    
    try:
        # Test basic imports
        print("Testing imports...")
        from kimera.echoform import EchoForm, init_geoid
        from kimera.storage import LatticeStorage
        from kimera.cls import Geoid
        print("✅ All imports successful")
        
        # Test basic functionality
        print("Testing basic functionality...")
        init_geoid()
        print("✅ Geoid initialization successful")
        
        # Test EchoForm creation
        form = EchoForm("test")
        print(f"✅ EchoForm created: {form}")
        
        # Test storage
        storage = LatticeStorage(":memory:")
        print("✅ Storage created")
        
        # Test storage operations
        storage.store_form(form)
        print("✅ Form stored")
        
        forms = storage.get_stored_forms()
        print(f"✅ Retrieved {len(forms)} forms")
        
        storage.close()
        print("✅ Storage closed")
        
        print("\n🎉 Quick validation PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)