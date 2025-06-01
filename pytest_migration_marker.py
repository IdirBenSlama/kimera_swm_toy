#!/usr/bin/env python3
"""
Pytest marker for migration testing
Provides @pytest.mark.migration decorator for CI gating
"""

import pytest
import tempfile
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


@pytest.mark.migration
def test_migration_in_memory():
    """
    Migration test that runs on in-memory database for CI
    This test can be run with: pytest -m migration
    """
    from kimera.storage import LatticeStorage
    from kimera.identity import create_geoid_identity
    from kimera.echoform import EchoForm
    import scripts.migrate_identity as migrate
    
    # Use in-memory database for CI
    storage = LatticeStorage(":memory:")
    
    try:
        # Create test EchoForm data
        echo1 = EchoForm("Test migration content 1", lang="en")
        echo2 = EchoForm("Test migration content 2", lang="en")
        
        storage.store_echoform(echo1)
        storage.store_echoform(echo2)
        
        # Add identity schema
        migrate.add_identity_schema(storage)
        
        # Migrate data
        migration_log = migrate.migrate_echoforms_to_identities(storage)
        
        # Verify migration
        assert len(migration_log) == 2, f"Expected 2 migrations, got {len(migration_log)}"
        
        # Test new identity creation
        new_identity = create_geoid_identity("Post-migration test", tags=["ci_test"])
        storage.store_identity(new_identity)
        
        # Verify retrieval
        retrieved = storage.fetch_identity(new_identity.id)
        assert retrieved is not None, "Failed to retrieve identity after migration"
        assert retrieved.raw == new_identity.raw, "Data integrity check failed"
        
        # Verify migration log structure
        for log_entry in migration_log:
            assert "echoform_anchor" in log_entry
            assert "identity_id" in log_entry
            assert "migration_timestamp" in log_entry
        
        print(f"✅ Migration test passed: {len(migration_log)} EchoForms migrated")
        
    finally:
        storage.close()


@pytest.mark.migration
def test_dual_write_consistency():
    """
    Test dual-write consistency for migration safety
    """
    from kimera.storage import LatticeStorage
    from kimera.identity import create_geoid_identity, create_scar_identity
    
    # Set dual-write mode
    os.environ["KIMERA_ID_DUAL_WRITE"] = "1"
    
    try:
        storage = LatticeStorage(":memory:")
        
        # Create identities of different types
        geoid_identity = create_geoid_identity("Geoid test content", tags=["dual_write"])
        scar_identity = create_scar_identity(
            "Scar test content",
            relationships=[{"target_id": "test_target", "type": "reference", "strength": 0.5}],
            tags=["dual_write"]
        )
        
        # Store identities
        storage.store_identity(geoid_identity)
        storage.store_identity(scar_identity)
        
        # Retrieve and verify
        retrieved_geoid = storage.fetch_identity(geoid_identity.id)
        retrieved_scar = storage.fetch_identity(scar_identity.id)
        
        assert retrieved_geoid is not None, "Failed to retrieve geoid identity"
        assert retrieved_scar is not None, "Failed to retrieve scar identity"
        
        # Verify data integrity
        assert retrieved_geoid.raw == geoid_identity.raw, "Geoid data mismatch"
        assert retrieved_scar.raw == scar_identity.raw, "Scar data mismatch"
        assert retrieved_geoid.type == "geoid", "Geoid type mismatch"
        assert retrieved_scar.type == "scar", "Scar type mismatch"
        
        # Test entropy consistency
        original_geoid_entropy = geoid_identity.entropy()
        retrieved_geoid_entropy = retrieved_geoid.entropy()
        assert abs(original_geoid_entropy - retrieved_geoid_entropy) < 0.001, "Entropy calculation inconsistency"
        
        print("✅ Dual-write consistency test passed")
        
    finally:
        storage.close()
        if "KIMERA_ID_DUAL_WRITE" in os.environ:
            del os.environ["KIMERA_ID_DUAL_WRITE"]


@pytest.mark.migration
def test_entropy_preservation():
    """
    Test that entropy calculations are preserved across storage operations
    """
    from kimera.storage import LatticeStorage
    from kimera.identity import create_geoid_identity
    
    storage = LatticeStorage(":memory:")
    
    try:
        # Create identity with known entropy characteristics
        identity = create_geoid_identity(
            "Test content with multiple terms",
            tags=["entropy", "test", "multiple", "terms", "preservation"]
        )
        
        # Calculate original entropy
        original_entropy = identity.entropy()
        original_tau = identity.effective_tau()
        
        # Store and retrieve
        storage.store_identity(identity)
        retrieved = storage.fetch_identity(identity.id)
        
        # Calculate retrieved entropy
        retrieved_entropy = retrieved.entropy()
        retrieved_tau = retrieved.effective_tau()
        
        # Verify preservation
        assert abs(original_entropy - retrieved_entropy) < 0.001, "Entropy not preserved"
        assert abs(original_tau - retrieved_tau) < 0.001, "Effective tau not preserved"
        
        print(f"✅ Entropy preservation test passed (entropy: {original_entropy:.3f})")
        
    finally:
        storage.close()


if __name__ == "__main__":
    # Run migration tests directly
    print("🧪 Running migration marker tests...")
    
    try:
        test_migration_in_memory()
        test_dual_write_consistency()
        test_entropy_preservation()
        print("🎉 All migration marker tests passed!")
    except Exception as e:
        print(f"❌ Migration marker tests failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)