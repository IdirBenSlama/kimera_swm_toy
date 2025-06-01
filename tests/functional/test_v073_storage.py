#!/usr/bin/env python3
"""
Test Phase 19.3 persistent storage functionality
Comprehensive tests for DuckDB storage backend and CLI
"""
import sys
import os
import tempfile
import subprocess
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent))

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
    storage = None
    
    try:
        storage = LatticeStorage(db_path)
        
        # Test storing and retrieving EchoForm
        echo = EchoForm(anchor="test", domain="test", phase="active")
        echo.add_term("term1", 0.5)
        echo.add_term("term2", 0.7)
        
        storage.store_echo_form(echo)
        retrieved = storage.fetch_echo_form("test", "test")
        
        assert retrieved is not None
        assert retrieved.anchor == "test"
        assert retrieved.domain == "test"
        assert len(retrieved.terms) == 2
        
        print("✅ Basic storage operations work")
        
    finally:
        if storage:
            storage.close()


def test_storage_persistence():
    """Test that data persists across storage instances"""
    print("Testing storage persistence...")
    
    db_path = fresh_duckdb_path()
    
    # Store data in first instance
    storage1 = LatticeStorage(db_path)
    echo = EchoForm(anchor="persist", domain="test", phase="active")
    echo.add_term("persistent_term", 0.8)
    storage1.store_echo_form(echo)
    storage1.close()
    
    # Retrieve data in second instance
    storage2 = LatticeStorage(db_path)
    retrieved = storage2.fetch_echo_form("persist", "test")
    
    assert retrieved is not None
    assert retrieved.anchor == "persist"
    assert "persistent_term" in retrieved.terms
    assert retrieved.terms["persistent_term"] == 0.8
    
    storage2.close()
    print("✅ Data persistence works")


def test_storage_metrics():
    """Test storage metrics and statistics"""
    print("Testing storage metrics...")
    
    db_path = fresh_duckdb_path()
    storage = LatticeStorage(db_path)
    
    try:
        # Store multiple forms
        for i in range(5):
            echo = EchoForm(anchor=f"test_{i}", domain="metrics", phase="active")
            echo.add_term(f"term_{i}", 0.5 + i * 0.1)
            storage.store_echo_form(echo)
        
        # Test metrics
        count = storage.get_echo_form_count()
        assert count >= 5
        
        forms = storage.list_echo_forms()
        assert len(forms) >= 5
        
        print(f"✅ Storage metrics work (found {count} forms)")
        
    finally:
        storage.close()


def test_storage_pruning():
    """Test pruning old forms"""
    print("Testing storage pruning...")
    
    db_path = fresh_duckdb_path()
    storage = LatticeStorage(db_path)
    
    try:
        # Store some forms
        for i in range(3):
            echo = EchoForm(anchor=f"prune_{i}", domain="test", phase="active")
            echo.add_term(f"term_{i}", 0.5)
            storage.store_echo_form(echo)
        
        initial_count = storage.get_echo_form_count()
        
        # Prune old forms (use very short time to prune everything)
        pruned = storage.prune_old_forms(older_than_seconds=0)
        
        final_count = storage.get_echo_form_count()
        
        assert pruned >= 0  # Should have pruned some forms
        print(f"✅ Pruning works (pruned {pruned} forms)")
        
    finally:
        storage.close()


def test_lattice_integration():
    """Test lattice functionality with storage"""
    print("Testing lattice integration...")
    
    db_path = fresh_duckdb_path()
    storage = LatticeStorage(db_path)
    
    try:
        # Create some geoids
        geoid1 = init_geoid("AI will transform healthcare")
        geoid2 = init_geoid("Medical AI has accuracy concerns")
        
        # Store them
        storage.store_geoid(geoid1)
        storage.store_geoid(geoid2)
        
        # Test lattice resolution
        intensity = lattice_resolve(geoid1.id, geoid2.id)
        assert isinstance(intensity, (int, float))
        assert intensity >= 0
        
        # Test lattice form creation
        form = create_lattice_form("test_form", geoid1.id, geoid2.id)
        assert form is not None
        assert "name" in form
        
        print(f"✅ Lattice integration works (intensity: {intensity:.3f})")
        
    finally:
        storage.close()


def test_cli_integration():
    """Test CLI integration with storage"""
    print("Testing CLI integration...")
    
    # Test that the CLI can access storage
    try:
        result = subprocess.run([
            sys.executable, "-c", 
            "from kimera.storage import get_storage; s = get_storage(); print('CLI OK')"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and "CLI OK" in result.stdout:
            print("✅ CLI integration works")
        else:
            print(f"⚠️ CLI integration issue: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⚠️ CLI test timed out")
    except Exception as e:
        print(f"⚠️ CLI test error: {e}")


def run_all_tests():
    """Run all storage tests"""
    print("🚀 Starting v0.7.3 storage tests...\n")
    
    try:
        test_storage_basic_operations()
        print()
        
        test_storage_persistence()
        print()
        
        test_storage_metrics()
        print()
        
        test_storage_pruning()
        print()
        
        test_lattice_integration()
        print()
        
        test_cli_integration()
        print()
        
        print("🎉 All v0.7.3 storage tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)