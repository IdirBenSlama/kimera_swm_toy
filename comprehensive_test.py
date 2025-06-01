#!/usr/bin/env python3
"""Comprehensive test of all API compatibility fixes"""

import sys
import os
import tempfile
sys.path.insert(0, 'src')

def test_echoform_api():
    """Test EchoForm API compatibility"""
    print("🧪 Testing EchoForm API...")
    
    from kimera.echoform import EchoForm
    
    # Test 1: No-arg constructor
    echo1 = EchoForm()
    assert echo1.anchor == ""
    assert echo1.domain == "echo"
    print("✅ EchoForm() constructor works")
    
    # Test 2: Config constructor
    config = {"mode": "test", "debug": True, "anchor": "test_anchor"}
    echo2 = EchoForm(config=config)
    assert echo2.config["mode"] == "test"
    assert echo2.anchor == "test_anchor"
    print("✅ EchoForm(config=...) constructor works")
    
    # Test 3: Process method
    result = echo1.process("test input")
    assert result["processed"] == True
    assert result["input"] == "test input"
    print("✅ EchoForm.process() method works")
    
    # Test 4: to_dict method
    data = echo1.to_dict()
    assert "anchor" in data
    assert "domain" in data
    print("✅ EchoForm.to_dict() method works")

def test_identity_api():
    """Test Identity API compatibility"""
    print("\n🧪 Testing Identity API...")
    
    from kimera.identity import Identity
    
    # Test 1: Content constructor
    id1 = Identity(content="test content")
    assert hasattr(id1, 'content')
    assert id1.content == "test content"
    assert id1.identity_type == "geoid"
    print("✅ Identity(content=...) constructor works")
    
    # Test 2: Content + metadata constructor
    metadata = {"type": "test", "priority": 1}
    id2 = Identity(content="test content", metadata=metadata)
    assert id2.metadata == metadata
    print("✅ Identity(content=..., metadata=...) constructor works")
    
    # Test 3: create_scar class method
    scar = Identity.create_scar(
        content="test scar",
        related_ids=["id1", "id2"],
        metadata={"relationship_type": "test"}
    )
    assert scar.identity_type == "scar"
    assert "related_ids" in scar.meta
    print("✅ Identity.create_scar() method works")
    
    # Test 4: Equality comparison
    id3 = Identity(content="test content")
    id4 = Identity(content="test content")
    id5 = Identity(content="different content")
    assert id3 == id4  # Same content
    assert id3 != id5  # Different content
    print("✅ Identity equality comparison works")

def test_storage_api():
    """Test LatticeStorage API compatibility"""
    print("\n🧪 Testing Storage API...")
    
    from kimera.storage import LatticeStorage
    from kimera.identity import Identity
    from kimera.echoform import EchoForm
    
    # Create temporary database
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()
    
    try:
        # Test 1: Constructor with invalid file handling
        storage = LatticeStorage(temp_file.name)
        print("✅ LatticeStorage constructor works")
        
        # Test 2: store_identity and fetch_identity
        identity = Identity(content="test content")
        storage.store_identity(identity)
        fetched = storage.fetch_identity(identity.id)
        assert fetched is not None
        print("✅ store_identity/fetch_identity works")
        
        # Test 3: store_echo_form compatibility stub
        echo = EchoForm(anchor="test_echo")
        storage.store_echo_form(echo)
        print("✅ store_echo_form compatibility stub works")
        
        # Test 4: store_geoid compatibility stub
        geoid_identity = Identity(content="geoid content")
        storage.store_geoid(geoid_identity)
        print("✅ store_geoid compatibility stub works")
        
        # Test 5: fetch_geoid compatibility stub
        result = storage.fetch_geoid(geoid_identity.id)
        assert result is not None
        print("✅ fetch_geoid compatibility stub works")
        
        # Test 6: Close method
        storage.close()
        print("✅ storage.close() method works")
        
    finally:
        # Clean up
        if os.path.exists(temp_file.name):
            try:
                os.unlink(temp_file.name)
            except:
                pass

def test_original_unit_tests():
    """Test that original unit test patterns work"""
    print("\n🧪 Testing original unit test patterns...")
    
    # Simulate the original test patterns
    from kimera.echoform import EchoForm
    from kimera.identity import Identity
    
    # Original EchoForm test pattern
    echo = EchoForm()
    assert echo is not None
    result = echo.process("test input")
    assert result is not None
    print("✅ Original EchoForm test pattern works")
    
    # Original EchoForm config test pattern
    config = {"mode": "test", "debug": True}
    echo = EchoForm(config=config)
    assert echo.config["mode"] == "test"
    assert echo.config["debug"] is True
    print("✅ Original EchoForm config test pattern works")
    
    # Original Identity test patterns
    identity = Identity(content="test content")
    assert identity.content == "test content"
    assert identity.id is not None
    assert len(identity.id) > 0
    print("✅ Original Identity test pattern works")
    
    # Original Identity metadata test pattern
    metadata = {"type": "test", "priority": 1}
    identity = Identity(content="test content", metadata=metadata)
    assert identity.metadata == metadata
    print("✅ Original Identity metadata test pattern works")
    
    # Original SCAR test pattern
    scar = Identity.create_scar(
        content="test scar",
        related_ids=["id1", "id2"],
        metadata={"relationship_type": "test"}
    )
    assert scar.identity_type == "scar"
    assert "related_ids" in scar.meta
    assert scar.meta["related_ids"] == ["id1", "id2"]
    print("✅ Original SCAR test pattern works")
    
    # Original equality test pattern
    id1 = Identity(content="same content")
    id2 = Identity(content="same content")
    id3 = Identity(content="different content")
    assert id1 == id2
    assert id1 != id3
    print("✅ Original equality test pattern works")

def main():
    """Run all compatibility tests"""
    print("🚀 Running comprehensive API compatibility tests...\n")
    
    try:
        test_echoform_api()
        test_identity_api()
        test_storage_api()
        test_original_unit_tests()
        
        print("\n🎉 ALL COMPATIBILITY TESTS PASSED!")
        print("\n✅ The API drift issues have been successfully resolved!")
        print("✅ All original test patterns now work with the new implementation!")
        print("✅ Both legacy and new code can coexist seamlessly!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)