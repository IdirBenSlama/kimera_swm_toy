#!/usr/bin/env python3
"""
Unit tests for the Identity system
"""
import sys
sys.path.insert(0, 'src')

import pytest
from kimera.identity import Identity

def test_identity_creation():
    """Test basic identity creation"""
    identity = Identity(content="test content")
    assert identity.content == "test content"
    assert identity.id is not None
    assert len(identity.id) > 0

def test_identity_with_metadata():
    """Test identity creation with metadata"""
    metadata = {"type": "test", "priority": 1}
    identity = Identity(content="test content", metadata=metadata)
    assert identity.metadata == metadata

def test_identity_scar_creation():
    """Test SCAR identity creation"""
    scar = Identity.create_scar(
        content="test scar",
        related_ids=["id1", "id2"],
        metadata={"relationship_type": "test"}
    )
    assert scar.identity_type == "scar"
    assert "related_ids" in scar.metadata
    assert scar.metadata["related_ids"] == ["id1", "id2"]

def test_identity_equality():
    """Test identity equality comparison"""
    id1 = Identity(content="same content")
    id2 = Identity(content="same content")
    id3 = Identity(content="different content")
    
    # Same content should be equal
    assert id1 == id2
    # Different content should not be equal
    assert id1 != id3

def test_identity_serialization():
    """Test identity serialization"""
    identity = Identity(content="test content", metadata={"test": True})
    
    # Test to_dict
    data = identity.to_dict()
    assert data["content"] == "test content"
    assert data["metadata"]["test"] is True
    
    # Test from_dict
    restored = Identity.from_dict(data)
    assert restored.content == identity.content
    assert restored.metadata == identity.metadata

if __name__ == "__main__":
    test_identity_creation()
    test_identity_with_metadata()
    test_identity_scar_creation()
    test_identity_equality()
    test_identity_serialization()
    print("✅ All Identity unit tests passed!")