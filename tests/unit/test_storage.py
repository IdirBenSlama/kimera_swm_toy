#!/usr/bin/env python3
"""
Unit tests for the Storage system
"""
import sys
import os
sys.path.insert(0, 'src')

import pytest
from kimera.storage import LatticeStorage
from kimera.identity import Identity

@pytest.fixture
def temp_storage():
    """Create a temporary storage instance for testing"""
    test_db = "test_storage.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    storage = LatticeStorage(db_path=test_db)
    yield storage
    
    # Cleanup - close connection first
    storage.close()
    if os.path.exists(test_db):
        os.remove(test_db)

def test_storage_creation(temp_storage):
    """Test storage creation"""
    assert temp_storage is not None

def test_store_and_retrieve_identity(temp_storage):
    """Test storing and retrieving an identity"""
    identity = Identity(content="test content")
    
    # Store identity
    temp_storage.store_identity(identity)
    
    # Retrieve identity
    retrieved = temp_storage.get_identity(identity.id)
    assert retrieved is not None
    assert retrieved.content == identity.content

def test_store_multiple_identities(temp_storage):
    """Test storing multiple identities"""
    identities = [
        Identity(content="content 1"),
        Identity(content="content 2"),
        Identity(content="content 3")
    ]
    
    # Store all identities
    for identity in identities:
        temp_storage.store_identity(identity)
    
    # Retrieve all identities
    for identity in identities:
        retrieved = temp_storage.get_identity(identity.id)
        assert retrieved is not None
        assert retrieved.content == identity.content

def test_search_identities(temp_storage):
    """Test searching for identities"""
    # Store test identities
    identity1 = Identity(content="search test content")
    identity2 = Identity(content="different content")
    
    temp_storage.store_identity(identity1)
    temp_storage.store_identity(identity2)
    
    # Search for identities
    results = temp_storage.search_identities("search")
    assert len(results) >= 1
    assert any(r.content == identity1.content for r in results)

def test_scar_storage(temp_storage):
    """Test storing and retrieving scars"""
    scar = Identity.create_scar(
        content="test scar",
        related_ids=["id1", "id2"],
        metadata={"relationship_type": "test"}
    )
    
    # Store scar
    temp_storage.store_identity(scar)
    
    # Retrieve scar
    retrieved = temp_storage.get_identity(scar.id)
    assert retrieved is not None
    assert retrieved.identity_type == "scar"
    assert "related_ids" in retrieved.metadata

if __name__ == "__main__":
    # Note: These tests require pytest fixtures, so they should be run with pytest
    print("Run these tests with: python -m pytest tests/unit/test_storage.py -v")