#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

def test_echoform_creation():
    """Test basic EchoForm creation"""
    from kimera.echoform import EchoForm
    echo = EchoForm()
    assert echo is not None
    print("✅ test_echoform_creation passed")
    
def test_echoform_basic_operations():
    """Test basic EchoForm operations"""
    from kimera.echoform import EchoForm
    echo = EchoForm()
    
    # Test basic functionality
    result = echo.process("test input")
    assert result is not None
    print("✅ test_echoform_basic_operations passed")
    
def test_echoform_configuration():
    """Test EchoForm configuration"""
    from kimera.echoform import EchoForm
    config = {
        "mode": "test",
        "debug": True
    }
    echo = EchoForm(config=config)
    assert echo.config["mode"] == "test"
    assert echo.config["debug"] is True
    print("✅ test_echoform_configuration passed")

def test_identity_creation():
    """Test basic identity creation"""
    from kimera.identity import Identity
    identity = Identity(content="test content")
    assert identity.content == "test content"
    assert identity.id is not None
    assert len(identity.id) > 0
    print("✅ test_identity_creation passed")

def test_identity_with_metadata():
    """Test identity creation with metadata"""
    from kimera.identity import Identity
    metadata = {"type": "test", "priority": 1}
    identity = Identity(content="test content", metadata=metadata)
    assert identity.metadata == metadata
    print("✅ test_identity_with_metadata passed")

def test_identity_scar_creation():
    """Test SCAR identity creation"""
    from kimera.identity import Identity
    scar = Identity.create_scar(
        content="test scar",
        related_ids=["id1", "id2"],
        metadata={"relationship_type": "test"}
    )
    assert scar.identity_type == "scar"
    assert "related_ids" in scar.meta
    assert scar.meta["related_ids"] == ["id1", "id2"]
    print("✅ test_identity_scar_creation passed")

def test_identity_equality():
    """Test identity equality comparison"""
    from kimera.identity import Identity
    id1 = Identity(content="same content")
    id2 = Identity(content="same content")
    id3 = Identity(content="different content")
    
    # Same content should be equal
    assert id1 == id2
    # Different content should not be equal
    assert id1 != id3
    print("✅ test_identity_equality passed")

if __name__ == "__main__":
    print("Running direct tests...")
    
    try:
        test_echoform_creation()
        test_echoform_basic_operations()
        test_echoform_configuration()
        print("✅ All EchoForm tests passed!")
    except Exception as e:
        print(f"❌ EchoForm test failed: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        test_identity_creation()
        test_identity_with_metadata()
        test_identity_scar_creation()
        test_identity_equality()
        print("✅ All Identity tests passed!")
    except Exception as e:
        print(f"❌ Identity test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🎉 Direct tests complete!")