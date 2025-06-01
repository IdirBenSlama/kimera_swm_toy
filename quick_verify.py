#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

print("🔍 Quick verification of our fixes...")

try:
    # Test EchoForm
    print("1. Testing EchoForm...")
    from kimera.echoform import EchoForm
    
    echo = EchoForm()
    print(f"   ✅ EchoForm() created: {type(echo)}")
    
    config = {"mode": "test", "debug": True}
    echo2 = EchoForm(config=config)
    print(f"   ✅ EchoForm(config=...) created with config: {echo2.config}")
    
    result = echo.process("test")
    print(f"   ✅ process() method works: {result['processed']}")
    
except Exception as e:
    print(f"   ❌ EchoForm error: {e}")
    import traceback
    traceback.print_exc()

try:
    # Test Identity
    print("\n2. Testing Identity...")
    from kimera.identity import Identity
    
    identity = Identity(content="test content")
    print(f"   ✅ Identity(content=...) created: {identity.content}")
    
    metadata = {"type": "test"}
    identity2 = Identity(content="test", metadata=metadata)
    print(f"   ✅ Identity with metadata: {identity2.metadata}")
    
    scar = Identity.create_scar(content="scar", related_ids=["id1"], metadata={"rel": "test"})
    print(f"   ✅ create_scar() works: {scar.identity_type}")
    
    data = identity.to_dict()
    restored = Identity.from_dict(data)
    print(f"   ✅ to_dict/from_dict works: {restored.content}")
    
except Exception as e:
    print(f"   ❌ Identity error: {e}")
    import traceback
    traceback.print_exc()

try:
    # Test Storage
    print("\n3. Testing Storage...")
    from kimera.storage import LatticeStorage
    import tempfile
    import os
    
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()
    
    storage = LatticeStorage(temp_file.name)
    print(f"   ✅ LatticeStorage created")
    
    identity = Identity(content="storage test")
    storage.store_identity(identity)
    print(f"   ✅ store_identity works")
    
    retrieved = storage.get_identity(identity.id)
    print(f"   ✅ get_identity works: {retrieved is not None}")
    
    results = storage.search_identities("storage")
    print(f"   ✅ search_identities works: {len(results)} results")
    
    storage.close()
    os.unlink(temp_file.name)
    print(f"   ✅ close() works")
    
except Exception as e:
    print(f"   ❌ Storage error: {e}")
    import traceback
    traceback.print_exc()

print("\n🎯 Quick verification complete!")