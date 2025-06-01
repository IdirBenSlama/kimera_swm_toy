#!/usr/bin/env python3
"""
Test script for unified identity system
Validates the new Identity model and storage integration
"""

import sys
import tempfile
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

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
        lang="en", 
        tags=["test", "demo"]
    )
    
    assert geoid_identity.identity_type == "geoid"
    assert geoid_identity.raw == "Hello world"
    assert geoid_identity.echo == "Hello world"
    assert geoid_identity.lang_axis == "en"
    assert "test" in geoid_identity.tags
    print("✓ Geoid identity creation works")
    
    # Test scar-type identity
    scar_identity = create_scar_identity("id1", "id2", weight=0.8)
    
    assert scar_identity.identity_type == "scar"
    assert len(scar_identity.related_ids) == 2
    assert scar_identity.weight == 0.8
    print("✓ Scar identity creation works")
    
    return geoid_identity, scar_identity


def test_entropy_calculation():
    """Test entropy calculation for different identity types"""
    print("🧪 Testing entropy calculation...")
    
    # Create identity with terms for entropy calculation
    identity = create_geoid_identity("test content", tags=["entropy"])
    
    # Add some terms to meta for entropy calculation
    identity.meta["terms"] = [
        {"symbol": "test", "intensity": 0.5},
        {"symbol": "content", "intensity": 0.3},
        {"symbol": "entropy", "intensity": 0.2}
    ]
    
    entropy = identity.entropy()
    assert entropy > 0, f"Expected positive entropy, got {entropy}"
    print(f"✓ Entropy calculation works: {entropy:.3f}")
    
    # Test effective tau calculation
    effective_tau = identity.effective_tau()
    base_tau = 14 * 24 * 3600  # 14 days in seconds
    assert effective_tau >= base_tau, "Effective tau should be >= base tau"
    print(f"✓ Effective tau calculation works: {effective_tau/86400:.1f} days")
    
    return entropy


def test_storage_integration():
    """Test storing and retrieving identities"""
    print("🧪 Testing storage integration...")
    
    # Create temporary database using the proper helper
    def fresh_duckdb_path():
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)        # close handle
        os.unlink(path)     # remove file so DuckDB can create it
        return path
    
    db_path = fresh_duckdb_path()
    storage = None
    
    try:
        storage = LatticeStorage(db_path)
        
        # Create and store a geoid identity
        geoid = create_geoid_identity("storage test", tags=["storage"])
        geoid.meta["terms"] = [{"symbol": "storage", "intensity": 1.0}]
        
        storage.store_identity(geoid)
        print("✓ Identity stored successfully")
        
        # Retrieve the identity
        retrieved = storage.fetch_identity(geoid.id)
        assert retrieved is not None, "Failed to retrieve identity"
        assert retrieved.id == geoid.id
        assert retrieved.identity_type == geoid.identity_type
        assert retrieved.raw == geoid.raw
        print("✓ Identity retrieved successfully")
        
        # Test listing identities
        identities = storage.list_identities(limit=5)
        assert len(identities) >= 1, "Should have at least one identity"
        print(f"✓ Listed {len(identities)} identities")
        
        # Test count
        count = storage.get_identity_count()
        assert count >= 1, "Should have at least one identity"
        print(f"✓ Identity count: {count}")
        
        # Test entropy-based search
        entropy_identities = storage.find_identities_by_entropy(min_entropy=0.0)
        assert len(entropy_identities) >= 1, "Should find identities with entropy"
        print(f"✓ Found {len(entropy_identities)} identities by entropy")
        
    finally:
        if storage:
            storage.close()
        # Clean up
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_serialization():
    """Test identity serialization and deserialization"""
    print("🧪 Testing serialization...")
    
    # Create identity with complex data
    identity = create_geoid_identity("serialization test")
    identity.meta = {
        "terms": [{"symbol": "test", "intensity": 0.7}],
        "custom_field": "custom_value"
    }
    
    # Convert to dict and back
    data_dict = identity.to_dict()
    restored = Identity.from_dict(data_dict)
    
    assert restored.id == identity.id
    assert restored.identity_type == identity.identity_type
    assert restored.raw == identity.raw
    assert restored.meta == identity.meta
    print("✓ Serialization round-trip works")


def main():
    """Run all tests"""
    print("🚀 Testing Unified Identity System\n")
    
    try:
        # Run tests
        geoid, scar = test_identity_creation()
        entropy = test_entropy_calculation()
        test_storage_integration()
        test_serialization()
        
        print(f"\n✅ All tests passed!")
        print(f"   • Geoid ID: {geoid.id}")
        print(f"   • Scar ID: {scar.id}")
        print(f"   • Sample entropy: {entropy:.3f}")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise


if __name__ == "__main__":
    main()