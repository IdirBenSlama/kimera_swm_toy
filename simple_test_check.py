#!/usr/bin/env python3
"""
Simple test to check current imports and basic functionality
"""
import sys
import os
sys.path.insert(0, 'src')

def test_imports():
    """Test basic imports"""
    try:
        from kimera.echoform import EchoForm
        print("✅ EchoForm import successful")
        
        from kimera.identity import Identity
        print("✅ Identity import successful")
        
        from kimera.storage import LatticeStorage
        print("✅ LatticeStorage import successful")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_functionality():
    """Test basic functionality"""
    try:
        # Test EchoForm
        echo = EchoForm()
        print("✅ EchoForm creation successful")
        
        # Test Identity
        identity = Identity(content="test content")
        print("✅ Identity creation successful")
        
        # Test basic operations
        result = echo.process("test input")
        print("✅ EchoForm processing successful")
        
        # Test Identity serialization
        data = identity.to_dict()
        print("✅ Identity serialization successful")
        print(f"   Identity data keys: {list(data.keys())}")
        
        return True
    except Exception as e:
        print(f"❌ Basic functionality failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== Testing Current State ===")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path[:3]}")
    
    imports_ok = test_imports()
    if imports_ok:
        functionality_ok = test_basic_functionality()
        if functionality_ok:
            print("\n✅ All basic tests passed!")
        else:
            print("\n❌ Basic functionality tests failed")
    else:
        print("\n❌ Import tests failed")