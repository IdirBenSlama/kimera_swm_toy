#!/usr/bin/env python3
"""
Test Scar functionality in the unified Identity system.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from kimera.identity import Identity, create_scar_identity, create_geoid_identity
from kimera.storage import LatticeStorage
from kimera.entropy import calculate_relationship_entropy
from conftest import fresh_duckdb_path


def test_scar_creation():
    """Test creating scar identities"""
    print("🧪 Testing Scar creation...")
    
    # Create a scar identity
    scar = create_scar_identity("id1", "id2", weight=0.8)
    
    assert scar.identity_type == "scar"
    assert scar.weight == 0.8
    assert "id1" in scar.related_ids
    assert "id2" in scar.related_ids
    assert len(scar.related_ids) == 2
    
    print(f"✅ Created scar: {scar.id[:8]}... with related_ids: {scar.related_ids}")
    return scar


def test_scar_entropy():
    """Test entropy calculation for scars"""
    print("🧪 Testing Scar entropy...")
    
    # Create scars with different relationship counts
    simple_scar = create_scar_identity("id1", "id2", weight=1.0)
    complex_scar = Identity(
        identity_type="scar",
        related_ids=["id1", "id2", "id3", "id4"],
        weight=1.0
    )
    
    simple_entropy = simple_scar.entropy()
    complex_entropy = complex_scar.entropy()
    
    print(f"✅ Simple scar entropy: {simple_entropy:.3f}")
    print(f"✅ Complex scar entropy: {complex_entropy:.3f}")
    
    # Complex scar should have higher entropy
    assert complex_entropy > simple_entropy
    
    return simple_scar, complex_scar


def test_scar_storage():
    """Test storing and retrieving scars"""
    print("🧪 Testing Scar storage...")
    
    # Create temporary database using fresh_duckdb_path
    db_path = fresh_duckdb_path()
    
    try:
        storage = LatticeStorage(db_path)
        
        # Create and store a scar
        scar = create_scar_identity("concept_a", "concept_b", weight=0.9)
        storage.store_identity(scar)
        
        # Retrieve the scar
        retrieved = storage.fetch_identity(scar.id)
        
        assert retrieved is not None
        assert retrieved.identity_type == "scar"
        assert retrieved.weight == 0.9
        assert "concept_a" in retrieved.related_ids
        assert "concept_b" in retrieved.related_ids
        
        print(f"✅ Stored and retrieved scar: {retrieved.id[:8]}...")
        
        # Test listing scars
        scar_list = storage.list_identities(identity_type="scar")
        assert len(scar_list) >= 1
        
        print(f"✅ Found {len(scar_list)} scar(s) in storage")
        
        storage.close()
        
    finally:
        # Clean up
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_mixed_identity_types():
    """Test storing both geoids and scars together"""
    print("🧪 Testing mixed identity types...")
    
    # Create temporary database using fresh_duckdb_path
    db_path = fresh_duckdb_path()
    
    try:
        storage = LatticeStorage(db_path)
        
        # Create a geoid
        geoid = create_geoid_identity("This is a test concept", tags=["test"])
        storage.store_identity(geoid)
        
        # Create a scar
        scar = create_scar_identity(geoid.id, "external_concept", weight=0.7)
        storage.store_identity(scar)
        
        # Test counts
        total_count = storage.get_identity_count()
        geoid_count = storage.get_identity_count("geoid")
        scar_count = storage.get_identity_count("scar")
        
        assert total_count == 2
        assert geoid_count == 1
        assert scar_count == 1
        
        print(f"✅ Stored {geoid_count} geoid(s) and {scar_count} scar(s)")
        
        # Test entropy-based search
        entropy_results = storage.find_identities_by_entropy(min_entropy=0.0)
        assert len(entropy_results) >= 1
        
        print(f"✅ Found {len(entropy_results)} identities with entropy > 0")
        
        storage.close()
        
    finally:
        # Clean up
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_scar_effective_tau():
    """Test entropy-based time decay for scars"""
    print("🧪 Testing Scar effective tau...")
    
    # Create scars with different complexities
    simple_scar = create_scar_identity("id1", "id2")
    complex_scar = Identity(
        identity_type="scar",
        related_ids=["id1", "id2", "id3", "id4", "id5"],
        weight=1.0
    )
    
    simple_tau = simple_scar.effective_tau()
    complex_tau = complex_scar.effective_tau()
    
    print(f"✅ Simple scar tau: {simple_tau:.1f} seconds")
    print(f"✅ Complex scar tau: {complex_tau:.1f} seconds")
    
    # Complex scar should have longer tau (slower decay)
    assert complex_tau > simple_tau
    
    return simple_scar, complex_scar


def main():
    """Run all scar tests"""
    print("🚀 Testing Scar Functionality in Unified Identity System")
    print("=" * 60)
    
    try:
        # Test basic scar creation
        scar = test_scar_creation()
        
        # Test entropy calculation
        simple_scar, complex_scar = test_scar_entropy()
        
        # Test storage operations
        test_scar_storage()
        
        # Test mixed identity types
        test_mixed_identity_types()
        
        # Test effective tau calculation
        test_scar_effective_tau()
        
        print("\n" + "=" * 60)
        print("🎉 All Scar tests passed!")
        print("\nScar functionality is working correctly:")
        print("✅ Scar creation with relationships")
        print("✅ Entropy calculation for relationships")
        print("✅ Storage and retrieval")
        print("✅ Mixed storage with geoids")
        print("✅ Entropy-based time decay")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)