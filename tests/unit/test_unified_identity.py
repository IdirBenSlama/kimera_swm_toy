#!/usr/bin/env python3
"""
Test script for unified identity system
Validates the new Identity model and storage integration
"""

import sys
import tempfile
import os
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

try:
    from kimera.identity import Identity, create_geoid_identity, create_scar_identity
    from kimera.storage import LatticeStorage
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all dependencies are installed")
    sys.exit(1)


def test_identity_creation():
    """Test creating different types of identities"""
    print("🧪 Testing identity creation...")
    
    # Test geoid-type identity
    geoid_identity = create_geoid_identity(
        text="Hello world",
        weight=0.8
    )
    
    assert geoid_identity.identity_type == "geoid"
    assert geoid_identity.raw == "Hello world"
    assert geoid_identity.weight == 0.8
    assert geoid_identity.id.startswith("geoid_")
    print("[PASS] Geoid identity creation works")
    
    # Test scar-type identity
    scar_identity = create_scar_identity(
        id1="test_id_1",
        id2="test_id_2",
        weight=0.9
    )
    
    assert scar_identity.identity_type == "scar"
    assert "test_id_1" in scar_identity.related_ids
    assert "test_id_2" in scar_identity.related_ids
    assert scar_identity.weight == 0.9
    assert scar_identity.id.startswith("scar_")
    print("[PASS] Scar identity creation works")


def test_entropy_calculation():
    """Test entropy calculation for different identity types"""
    print("🧪 Testing entropy calculation...")
    
    # Test geoid entropy (content-based)
    geoid = create_geoid_identity("This is a test message")
    geoid_entropy = geoid.entropy()
    assert geoid_entropy > 0
    print(f"[PASS] Geoid entropy: {geoid_entropy:.3f}")
    
    # Test scar entropy (relationship-based)
    scar = create_scar_identity("id1", "id2", weight=1.0)
    scar_entropy = scar.entropy()
    assert scar_entropy > 0
    print(f"[PASS] Scar entropy: {scar_entropy:.3f}")
    
    # Test complex scar entropy
    complex_scar = Identity(
        identity_type="scar",
        related_ids=["id1", "id2", "id3", "id4"],
        weight=1.0
    )
    complex_entropy = complex_scar.entropy()
    assert complex_entropy > scar_entropy  # More relations = higher entropy
    print(f"[PASS] Complex scar entropy: {complex_entropy:.3f}")


def test_effective_tau():
    """Test effective tau calculation"""
    print("🧪 Testing effective tau calculation...")
    
    # Test geoid tau
    geoid = create_geoid_identity("Test content")
    geoid_tau = geoid.effective_tau()
    assert geoid_tau > 0
    print(f"[PASS] Geoid tau: {geoid_tau/86400:.1f} days")
    
    # Test scar tau
    scar = create_scar_identity("id1", "id2")
    scar_tau = scar.effective_tau()
    assert scar_tau > 0
    print(f"[PASS] Scar tau: {scar_tau/86400:.1f} days")


def test_storage_integration():
    """Test storage and retrieval of identities"""
    print("🧪 Testing storage integration...")
    
    # Create temporary database
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    
    try:
        storage = LatticeStorage(db_path)
        
        # Store geoid identity
        geoid = create_geoid_identity("Test storage content")
        storage.store_identity(geoid)
        print("[PASS] Stored geoid identity")
        
        # Store scar identity
        scar = create_scar_identity("test_1", "test_2")
        storage.store_identity(scar)
        print("[PASS] Stored scar identity")
        
        # Retrieve identities
        retrieved_geoid = storage.fetch_identity(geoid.id)
        assert retrieved_geoid is not None
        assert retrieved_geoid.id == geoid.id
        assert retrieved_geoid.identity_type == "geoid"
        print("[PASS] Retrieved geoid identity")
        
        retrieved_scar = storage.fetch_identity(scar.id)
        assert retrieved_scar is not None
        assert retrieved_scar.id == scar.id
        assert retrieved_scar.identity_type == "scar"
        print("[PASS] Retrieved scar identity")
        
        # Test listing by type
        geoids = storage.list_identities(identity_type="geoid")
        scars = storage.list_identities(identity_type="scar")
        
        assert len(geoids) >= 1
        assert len(scars) >= 1
        print(f"[PASS] Found {len(geoids)} geoids and {len(scars)} scars")
        
        storage.close()
        
    finally:
        # Cleanup
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_metadata_support():
    """Test metadata support in identities"""
    print("🧪 Testing metadata support...")
    
    # Test geoid with metadata
    geoid = create_geoid_identity("Test content")
    geoid.meta = {
        "source": "test_suite",
        "category": "unit_test",
        "priority": "high"
    }
    
    assert geoid.meta["source"] == "test_suite"
    assert geoid.meta["category"] == "unit_test"
    print("[PASS] Geoid metadata works")
    
    # Test scar with metadata
    scar = create_scar_identity("id1", "id2")
    scar.meta = {
        "relationship_type": "contradicts",
        "strength": "strong",
        "discovered_at": "2024-12-19"
    }
    
    assert scar.meta["relationship_type"] == "contradicts"
    assert scar.meta["strength"] == "strong"
    print("[PASS] Scar metadata works")


def run_all_tests():
    """Run all identity tests"""
    print("🚀 Starting unified identity tests...\n")
    
    try:
        test_identity_creation()
        print()
        
        test_entropy_calculation()
        print()
        
        test_effective_tau()
        print()
        
        test_storage_integration()
        print()
        
        test_metadata_support()
        print()
        
        print("🎉 All unified identity tests passed!")
        return True
        
    except Exception as e:
        print(f"[FAIL] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)