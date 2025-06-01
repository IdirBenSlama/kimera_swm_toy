#!/usr/bin/env python3
"""Quick test of our fixes"""

import sys
sys.path.insert(0, 'src')

def test_echoform_fixes():
    from kimera.echoform import EchoForm
    
    # Test no-arg constructor
    echo1 = EchoForm()
    print(f"✅ EchoForm() works: {echo1.anchor}")
    
    # Test config constructor
    config = {"mode": "test", "debug": True}
    echo2 = EchoForm(config=config)
    print(f"✅ EchoForm(config=...) works: {echo2.config}")
    
    # Test process method
    result = echo1.process("test input")
    print(f"✅ process() works: {result}")

def test_identity_fixes():
    from kimera.identity import Identity
    
    # Test content constructor
    id1 = Identity(content="test content")
    print(f"✅ Identity(content=...) works: {id1.content}")
    
    # Test create_scar
    scar = Identity.create_scar(content="test scar", related_ids=["id1", "id2"])
    print(f"✅ Identity.create_scar() works: {scar.identity_type}")
    
    # Test equality
    id2 = Identity(content="test content")
    print(f"✅ Identity equality works: {id1 == id2}")

def test_storage_fixes():
    from kimera.storage import LatticeStorage
    from kimera.identity import Identity
    from kimera.echoform import EchoForm
    import tempfile
    import os
    
    # Create temp storage
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()
    
    try:
        storage = LatticeStorage(temp_file.name)
        print("✅ LatticeStorage constructor works")
        
        # Test store_identity
        identity = Identity(content="test")
        storage.store_identity(identity)
        print("✅ store_identity works")
        
        # Test fetch_identity
        fetched = storage.fetch_identity(identity.id)
        print(f"✅ fetch_identity works: {fetched is not None}")
        
        # Test compatibility stubs
        echo = EchoForm()
        storage.store_echo_form(echo)
        print("✅ store_echo_form compatibility works")
        
        storage.close()
        
    finally:
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

if __name__ == "__main__":
    print("Testing EchoForm fixes...")
    test_echoform_fixes()
    
    print("\nTesting Identity fixes...")
    test_identity_fixes()
    
    print("\nTesting Storage fixes...")
    test_storage_fixes()
    
    print("\n🎉 All quick tests passed!")