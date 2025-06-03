#!/usr/bin/env python3
"""
Test dual-write functionality for P1 implementation
"""

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, 'src')

from kimera.storage_dual_write import get_dual_write_storage
from kimera.identity import create_geoid_identity, create_scar_identity, Identity
from kimera.cls import lattice_resolve, create_identity_lattice


def test_dual_write_basic():
    """Test basic dual-write functionality"""
    print("\n🧪 Testing basic dual-write functionality...")
    
    # Create temporary database
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        # Test without dual-write
        os.environ['KIMERA_ID_DUAL_WRITE'] = '0'
        storage = get_dual_write_storage(db_path)
        
        # Create and store identity
        identity1 = create_geoid_identity("Test without dual-write", tags=["test"])
        storage.store_identity(identity1)
        
        # Check stats (should show dual-write disabled)
        stats = storage.get_dual_write_stats()
        assert stats.get("error") == "Dual-write not enabled"
        print("✅ Single-write mode works correctly")
        
        storage.close()
        
        # Now test with dual-write enabled
        os.environ['KIMERA_ID_DUAL_WRITE'] = '1'
        storage = get_dual_write_storage(db_path)
        
        # Create and store identities
        identity2 = create_geoid_identity("Test with dual-write", tags=["dual"])
        storage.store_identity(identity2)
        
        scar = create_scar_identity(identity1.id, identity2.id, weight=0.8)
        storage.store_identity(scar)
        
        # Check stats
        stats = storage.get_dual_write_stats()
        assert stats["dual_write_enabled"] == True
        assert stats["successful_operations"] == 2  # 2 stores
        assert stats["failed_operations"] == 0
        assert stats["legacy_geoids_count"] >= 1
        assert stats["legacy_scars_count"] >= 1
        
        print("✅ Dual-write mode works correctly")
        print(f"   - Success rate: {stats['success_rate']:.1f}%")
        print(f"   - Legacy geoids: {stats['legacy_geoids_count']}")
        print(f"   - Legacy scars: {stats['legacy_scars_count']}")
        
        # Verify consistency
        consistency1 = storage.verify_dual_write_consistency(identity2.id)
        assert consistency1["consistent"] == True
        print("✅ Geoid dual-write consistency verified")
        
        consistency2 = storage.verify_dual_write_consistency(scar.id)
        assert consistency2["consistent"] == True
        print("✅ Scar dual-write consistency verified")
        
        storage.close()
        
    finally:
        # Cleanup
        try:
            # Make sure to close any open connections
            if 'storage' in locals():
                storage.close()
            # Also close global storage if it was initialized
            from kimera.storage import close_storage
            close_storage()
        except:
            pass
            
        # Now try to delete the file
        if os.path.exists(db_path):
            try:
                os.unlink(db_path)
            except PermissionError:
                # On Windows, sometimes we need to wait a bit
                import time
                time.sleep(0.1)
                try:
                    os.unlink(db_path)
                except:
                    pass  # Ignore if still can't delete
                    
        # Reset environment
        os.environ.pop('KIMERA_ID_DUAL_WRITE', None)


def test_dual_write_with_cls():
    """Test dual-write with CLS integration"""
    print("\n🧪 Testing dual-write with CLS integration...")
    
    # Create temporary database
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        # Enable dual-write
        os.environ['KIMERA_ID_DUAL_WRITE'] = '1'
        
        # Need to reset the global storage instance
        from kimera.storage import close_storage
        close_storage()
        
        # Set the database path for global storage
        os.environ['KIMERA_LATTICE_DB'] = db_path
        
        # Create identities and perform lattice resolution
        intensity = create_identity_lattice(
            "The sun is bright",
            "The sun is dark",
            tags_a=["test", "cls"],
            tags_b=["test", "cls"]
        )
        
        print(f"✅ CLS lattice resolution with dual-write: intensity = {intensity}")
        
        # Get storage instance to check stats
        storage = get_dual_write_storage(db_path)
        stats = storage.get_dual_write_stats()
        
        print(f"   - Total operations: {stats['total_operations']}")
        print(f"   - New identities: {stats['new_identities_count']}")
        print(f"   - Legacy records: {stats['total_legacy_count']}")
        
        # Verify all identities have consistent dual-write
        identities = storage.list_identities(limit=100)
        inconsistent = []
        
        for id_meta in identities:
            consistency = storage.verify_dual_write_consistency(id_meta["id"])
            if not consistency.get("consistent", False):
                inconsistent.append(id_meta["id"])
        
        if inconsistent:
            print(f"❌ Found {len(inconsistent)} inconsistent identities")
            for id in inconsistent[:3]:  # Show first 3
                print(f"   - {id}")
        else:
            print(f"✅ All {len(identities)} identities are consistent")
        
        storage.close()
        
    finally:
        # Cleanup
        try:
            # Make sure to close any open connections
            if 'storage' in locals():
                storage.close()
            # Also close global storage if it was initialized
            from kimera.storage import close_storage
            close_storage()
        except:
            pass
            
        # Now try to delete the file
        if os.path.exists(db_path):
            try:
                os.unlink(db_path)
            except PermissionError:
                # On Windows, sometimes we need to wait a bit
                import time
                time.sleep(0.1)
                try:
                    os.unlink(db_path)
                except:
                    pass  # Ignore if still can't delete
                    
        # Reset environment
        os.environ.pop('KIMERA_ID_DUAL_WRITE', None)
        os.environ.pop('KIMERA_LATTICE_DB', None)


def test_dual_write_migration_scenario():
    """Test a realistic migration scenario"""
    print("\n🧪 Testing migration scenario...")
    
    # Create temporary database
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        # Phase 1: Create data without dual-write
        os.environ['KIMERA_ID_DUAL_WRITE'] = '0'
        storage = get_dual_write_storage(db_path)
        
        # Create some identities
        identities = []
        for i in range(5):
            identity = create_geoid_identity(f"Legacy identity {i}", tags=[f"batch{i//2}"])
            storage.store_identity(identity)
            identities.append(identity)
        
        # Create some scars
        for i in range(0, 4, 2):
            scar = create_scar_identity(identities[i].id, identities[i+1].id, weight=0.5+i*0.1)
            storage.store_identity(scar)
        
        initial_count = storage.get_identity_count()
        print(f"✅ Phase 1: Created {initial_count} identities without dual-write")
        
        storage.close()
        
        # Phase 2: Enable dual-write and create more data
        os.environ['KIMERA_ID_DUAL_WRITE'] = '1'
        storage = get_dual_write_storage(db_path)
        
        # Create more identities with dual-write
        for i in range(5, 10):
            identity = create_geoid_identity(f"Dual-write identity {i}", tags=["dual"])
            storage.store_identity(identity)
        
        stats = storage.get_dual_write_stats()
        print(f"✅ Phase 2: Dual-write enabled")
        print(f"   - New operations: {stats['successful_operations']}")
        print(f"   - Legacy geoids: {stats['legacy_geoids_count']}")
        print(f"   - Total identities: {storage.get_identity_count()}")
        
        # Phase 3: Run migration for old data
        print("\n📋 Phase 3: Migrating old data...")
        
        # Get all identities that might not be in legacy tables
        all_identities = storage.list_identities(limit=1000)
        migrated = 0
        
        for id_meta in all_identities:
            # Check if exists in legacy
            consistency = storage.verify_dual_write_consistency(id_meta["id"])
            if consistency.get("error") == "Identity not found in legacy storage":
                # Re-store to trigger dual-write
                identity = storage.fetch_identity(id_meta["id"])
                if identity:
                    storage.store_identity(identity)
                    migrated += 1
        
        print(f"✅ Migrated {migrated} identities to legacy tables")
        
        # Final verification
        final_stats = storage.get_dual_write_stats()
        print(f"\n📊 Final Statistics:")
        print(f"   - Total identities: {storage.get_identity_count()}")
        print(f"   - Legacy geoids: {final_stats['legacy_geoids_count']}")
        print(f"   - Legacy scars: {final_stats['legacy_scars_count']}")
        print(f"   - Success rate: {final_stats['success_rate']:.1f}%")
        
        # Verify all are consistent
        all_consistent = True
        for id_meta in storage.list_identities(limit=1000):
            consistency = storage.verify_dual_write_consistency(id_meta["id"])
            if not consistency.get("consistent", False):
                all_consistent = False
                print(f"❌ Inconsistent: {id_meta['id']}")
                break
        
        if all_consistent:
            print("✅ All identities are consistent between new and legacy storage!")
        
        storage.close()
        
    finally:
        # Cleanup
        try:
            # Make sure to close any open connections
            if 'storage' in locals():
                storage.close()
            # Also close global storage if it was initialized
            from kimera.storage import close_storage
            close_storage()
        except:
            pass
            
        # Now try to delete the file
        if os.path.exists(db_path):
            try:
                os.unlink(db_path)
            except PermissionError:
                # On Windows, sometimes we need to wait a bit
                import time
                time.sleep(0.1)
                try:
                    os.unlink(db_path)
                except:
                    pass  # Ignore if still can't delete
                    
        # Reset environment
        os.environ.pop('KIMERA_ID_DUAL_WRITE', None)


def test_dual_write_performance():
    """Test performance impact of dual-write"""
    print("\n🧪 Testing dual-write performance impact...")
    
    import time
    
    # Create temporary database
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        # Test single-write performance
        os.environ['KIMERA_ID_DUAL_WRITE'] = '0'
        storage = get_dual_write_storage(db_path)
        
        start_time = time.time()
        for i in range(100):
            identity = create_geoid_identity(f"Performance test {i}", tags=["perf"])
            storage.store_identity(identity)
        single_write_time = time.time() - start_time
        
        storage.close()
        
        # Test dual-write performance
        os.environ['KIMERA_ID_DUAL_WRITE'] = '1'
        storage = get_dual_write_storage(db_path)
        
        start_time = time.time()
        for i in range(100, 200):
            identity = create_geoid_identity(f"Performance test {i}", tags=["perf"])
            storage.store_identity(identity)
        dual_write_time = time.time() - start_time
        
        # Calculate overhead
        overhead = ((dual_write_time - single_write_time) / single_write_time) * 100
        
        print(f"📊 Performance Results:")
        print(f"   - Single-write: {single_write_time:.3f}s for 100 operations")
        print(f"   - Dual-write: {dual_write_time:.3f}s for 100 operations")
        print(f"   - Overhead: {overhead:.1f}%")
        
        if overhead < 20:
            print("✅ Dual-write overhead is within acceptable range (<20%)")
        else:
            print(f"⚠️  Dual-write overhead ({overhead:.1f}%) exceeds target of 20%")
        
        storage.close()
        
    finally:
        # Cleanup
        try:
            # Make sure to close any open connections
            if 'storage' in locals():
                storage.close()
            # Also close global storage if it was initialized
            from kimera.storage import close_storage
            close_storage()
        except:
            pass
            
        # Now try to delete the file
        if os.path.exists(db_path):
            try:
                os.unlink(db_path)
            except PermissionError:
                # On Windows, sometimes we need to wait a bit
                import time
                time.sleep(0.1)
                try:
                    os.unlink(db_path)
                except:
                    pass  # Ignore if still can't delete
                    
        # Reset environment
        os.environ.pop('KIMERA_ID_DUAL_WRITE', None)


def main():
    """Run all dual-write tests"""
    print("🚀 Testing P1 Dual-Write Implementation")
    print("=" * 50)
    
    tests = [
        test_dual_write_basic,
        test_dual_write_with_cls,
        test_dual_write_migration_scenario,
        test_dual_write_performance
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"\n❌ {test.__name__} failed: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n📊 Test Results: {passed}/{len(tests)} passed")
    
    if failed == 0:
        print("🎉 All dual-write tests passed!")
        return True
    else:
        print(f"❌ {failed} tests failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)