#!/usr/bin/env python3
"""
Test Phase 19.3 persistent storage functionality
Comprehensive tests for DuckDB storage backend and CLI
"""
import sys
import os
import tempfile
import subprocess

sys.path.insert(0, 'src')
sys.path.insert(0, 'tests')

from kimera.storage import LatticeStorage, get_storage, close_storage
from kimera.echoform import EchoForm
from kimera.geoid import init_geoid
from kimera.cls import lattice_resolve, create_lattice_form
from conftest import fresh_duckdb_path


def test_storage_basic_operations():
    """Test basic storage operations"""
    print("Testing basic storage operations...")
    
    # Use fresh DuckDB path
    db_path = fresh_duckdb_path()
    
    try:
        storage = LatticeStorage(db_path)
        
        # Create test form
        form = EchoForm(
            anchor="test_storage",
            domain="test",
            terms=[
                {"symbol": "test", "role": "test_role", "intensity": 0.5}
            ],
            phase="test_phase"
        )
        
        # Test store
        storage.store_form(form)
        
        # Test fetch
        retrieved = storage.fetch_form("test_storage")
        assert retrieved is not None
        assert retrieved.anchor == "test_storage"
        assert retrieved.domain == "test"
        assert len(retrieved.terms) == 1
        
        # Test update
        form.add_term(symbol="updated", role="update_role", intensity=0.3)
        storage.update_form(form)
        
        updated = storage.fetch_form("test_storage")
        assert len(updated.terms) == 2
        
        # Test list
        forms_list = storage.list_forms(limit=10)
        assert len(forms_list) == 1
        assert forms_list[0]["anchor"] == "test_storage"
        
        # Test count
        count = storage.get_form_count()
        assert count == 1
        
        count_test = storage.get_form_count(domain="test")
        assert count_test == 1
        
        count_other = storage.get_form_count(domain="other")
        assert count_other == 0
        
        storage.close()
        print("✅ Basic storage operations test passed")
        
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


def test_storage_time_decay():
    """Test time-decay functionality"""
    print("Testing time-decay functionality...")
    
    db_path = fresh_duckdb_path()
    
    try:
        storage = LatticeStorage(db_path)
        
        # Create form with known intensity
        form = EchoForm(
            anchor="decay_test",
            domain="test",
            terms=[
                {"symbol": "test", "role": "test_role", "intensity": 1.0}
            ],
            phase="test_phase"
        )
        
        storage.store_form(form)
        
        # Get initial intensity
        initial_form = storage.fetch_form("decay_test")
        initial_intensity = initial_form.intensity_sum()
        
        # Apply decay with very short tau for testing
        storage.apply_time_decay(tau_days=0.001)  # Very short for immediate effect
        
        # Get decayed intensity
        decayed_form = storage.fetch_form("decay_test")
        decayed_intensity = decayed_form.intensity_sum()
        
        # Should be less than initial (decay applied)
        assert decayed_intensity < initial_intensity
        
        storage.close()
        print("✅ Time-decay test passed")
        
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


def test_storage_pruning():
    """Test pruning old forms"""
    print("Testing pruning functionality...")
    
    db_path = fresh_duckdb_path()
    
    try:
        storage = LatticeStorage(db_path)
        
        # Create multiple forms
        for i in range(5):
            form = EchoForm(
                anchor=f"prune_test_{i}",
                domain="test",
                terms=[{"symbol": f"test_{i}", "role": "test_role", "intensity": 0.5}],
                phase="test_phase"
            )
            storage.store_form(form)
        
        # Verify all forms exist
        count_before = storage.get_form_count()
        assert count_before == 5
        
        # Prune with 0 days (should remove all)
        deleted = storage.prune_old_forms(older_than_days=0)
        assert deleted == 5
        
        # Verify all forms removed
        count_after = storage.get_form_count()
        assert count_after == 0
        
        storage.close()
        print("✅ Pruning test passed")
        
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


def test_cls_with_persistent_storage():
    """Test CLS operations with persistent storage"""
    print("Testing CLS with persistent storage...")
    
    db_path = fresh_duckdb_path()
    
    try:
        # Initialize storage
        storage = get_storage(db_path)
        
        # Create test geoids
        geo_a = init_geoid("Persistent test A", "en", ["test"])
        geo_b = init_geoid("Persistent test B", "en", ["test"])
        
        # Test lattice resolve
        intensity1 = lattice_resolve(geo_a, geo_b)
        assert intensity1 == 1.1  # 1.0 + 0.1
        
        # Verify form was stored
        anchor = f"{geo_a.gid}_{geo_b.gid}"
        stored_form = storage.fetch_form(anchor)
        assert stored_form is not None
        assert stored_form.domain == "cls"
        
        # Test repeat resolve
        intensity2 = lattice_resolve(geo_a, geo_b)
        assert intensity2 == 1.2  # 1.0 + 0.1 + 0.1
        
        # Test create lattice form
        custom_form = create_lattice_form("persistent_custom", geo_a, geo_b)
        assert custom_form.anchor == "persistent_custom"
        
        # Verify both forms in storage
        cls_count = storage.get_form_count(domain="cls")
        assert cls_count == 2
        
        close_storage()
        print("✅ CLS with persistent storage test passed")
        
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


def test_cli_commands():
    """Test CLI commands"""
    print("Testing CLI commands...")
    
    db_path = fresh_duckdb_path()
    
    try:
        # Create some test data first
        storage = LatticeStorage(db_path)
        
        form = EchoForm(
            anchor="cli_test",
            domain="cli",
            terms=[{"symbol": "cli", "role": "test", "intensity": 0.8}],
            phase="test"
        )
        storage.store_form(form)
        storage.close()
        
        # Test CLI list command
        result = subprocess.run([
            sys.executable, "-m", "kimera", "lattice", "list"
        ], capture_output=True, text=True, cwd="src")
        
        # Should not error (even if no forms in default DB)
        assert result.returncode == 0
        
        print("✅ CLI commands test passed")
        
    except subprocess.CalledProcessError as e:
        print(f"CLI test failed: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
    
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


def test_migration_script():
    """Test the migration script"""
    print("Testing migration script...")
    
    try:
        # Run migration script
        result = subprocess.run([
            sys.executable, "scripts/migrate_lattice_to_db.py"
        ], capture_output=True, text=True)
        
        # Should complete successfully
        assert result.returncode == 0
        assert "Migration and verification complete" in result.stdout
        
        print("✅ Migration script test passed")
        
    except subprocess.CalledProcessError as e:
        print(f"Migration test failed: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
    
    finally:
        # Clean up any created database
        close_storage()
        if os.path.exists("kimera_lattice.db"):
            os.remove("kimera_lattice.db")


def main():
    """Run all Phase 19.3 storage tests"""
    print("🧪 Phase 19.3 Persistent Storage Tests")
    print("=" * 40)
    
    tests = [
        test_storage_basic_operations,
        test_storage_time_decay,
        test_storage_pruning,
        test_cls_with_persistent_storage,
        test_cli_commands,
        test_migration_script
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
        print()
    
    print(f"📊 Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All Phase 19.3 storage tests passed!")
        return True
    else:
        print("💥 Some tests failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)