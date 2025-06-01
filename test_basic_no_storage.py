#!/usr/bin/env python3
"""
Test basic functionality without storage dependencies
"""
import sys
import os
sys.path.insert(0, 'src')

def test_echoform_only():
    """Test EchoForm without storage"""
    try:
        from kimera.echoform import EchoForm
        print("✅ EchoForm import successful")
        
        # Test creation
        echo = EchoForm()
        print("✅ EchoForm creation successful")
        
        # Test with parameters
        echo2 = EchoForm(anchor="test", domain="test")
        print("✅ EchoForm with parameters successful")
        
        # Test processing
        result = echo.process("test input")
        print("✅ EchoForm processing successful")
        print(f"   Result keys: {list(result.keys())}")
        
        # Test serialization
        data = echo.to_dict()
        print("✅ EchoForm serialization successful")
        print(f"   Data keys: {list(data.keys())}")
        
        return True
    except Exception as e:
        print(f"❌ EchoForm test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_identity_only():
    """Test Identity without storage"""
    try:
        from kimera.identity import Identity
        print("✅ Identity import successful")
        
        # Test creation with content (legacy style)
        identity = Identity(content="test content")
        print("✅ Identity creation successful")
        
        # Test serialization
        data = identity.to_dict()
        print("✅ Identity serialization successful")
        print(f"   Data keys: {list(data.keys())}")
        
        # Check if content is in the data
        if "content" in data:
            print(f"✅ Content field present: {data['content']}")
        else:
            print("❌ Content field missing from serialization")
            return False
        
        # Test SCAR creation
        scar = Identity.create_scar(
            content="test scar",
            related_ids=["id1", "id2"],
            metadata={"relationship_type": "test"}
        )
        print("✅ SCAR creation successful")
        
        scar_data = scar.to_dict()
        print(f"   SCAR data keys: {list(scar_data.keys())}")
        
        return True
    except Exception as e:
        print(f"❌ Identity test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== Testing Basic Functionality (No Storage) ===")
    
    echoform_ok = test_echoform_only()
    identity_ok = test_identity_only()
    
    if echoform_ok and identity_ok:
        print("\n✅ All basic tests passed!")
    else:
        print("\n❌ Some tests failed")
        if not echoform_ok:
            print("   - EchoForm tests failed")
        if not identity_ok:
            print("   - Identity tests failed")