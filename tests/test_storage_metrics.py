"""
Test storage metrics collection
"""
import os

from kimera.storage import (
    get_storage, close_storage, 
    get_storage_metrics, reset_storage_metrics
)
from kimera.echoform import EchoForm
from conftest import fresh_duckdb_path


def test_storage_metrics_collection():
    """Test that storage operations are properly timed and counted"""
    # Use fresh DuckDB path
    db_path = fresh_duckdb_path()
    
    try:
        # Reset metrics
        reset_storage_metrics()
        
        # Get storage instance
        storage = get_storage(db_path)
        
        # Create test form
        form = EchoForm(anchor="test_anchor", domain="test_domain", phase="active")
        form.add_term("test", role="metric_role", intensity=1.0, test=True)
        
        # Store form (should trigger store_form metric)
        storage.store_form(form)
        
        # Fetch form (should trigger fetch_form metric)
        fetched = storage.fetch_form("test_anchor")
        assert fetched is not None
        
        # List forms (should trigger list_forms metric)
        forms = storage.list_forms(limit=5)
        assert len(forms) == 1
        
        # Get count (should trigger get_form_count metric)
        count = storage.get_form_count()
        assert count == 1
        
        # Get metrics
        metrics = get_storage_metrics()
        
        # Verify metrics were collected
        assert "store_form" in metrics
        assert "fetch_form" in metrics
        assert "list_forms" in metrics
        assert "get_form_count" in metrics
        
        # Verify counts
        assert metrics["store_form_count"] >= 1
        assert metrics["fetch_form_count"] >= 1
        assert metrics["list_forms_count"] >= 1
        assert metrics["get_form_count_count"] >= 1
        
        # Verify timing values are reasonable (> 0, < 1 second)
        assert 0 < metrics["store_form"] < 1.0
        assert 0 < metrics["fetch_form"] < 1.0
        assert 0 < metrics["list_forms"] < 1.0
        assert 0 < metrics["get_form_count"] < 1.0
        
        print(f"Storage metrics: {metrics}")
        
    finally:
        close_storage()
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_metrics_reset():
    """Test that metrics can be reset"""
    # Use fresh DuckDB path
    db_path = fresh_duckdb_path()
    
    try:
        # Reset metrics
        reset_storage_metrics()
        
        # Get storage and perform operations
        storage = get_storage(db_path)
        form = EchoForm(anchor="test_anchor", domain="test_domain", phase="active")
        storage.store_form(form)
        
        # Check metrics exist
        metrics = get_storage_metrics()
        assert len(metrics) > 0
        
        # Reset metrics
        reset_storage_metrics()
        
        # Check metrics are cleared
        metrics = get_storage_metrics()
        assert len(metrics) == 0
        
    finally:
        close_storage()
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_metrics_accumulation():
    """Test that metrics accumulate across multiple operations"""
    # Use fresh DuckDB path
    db_path = fresh_duckdb_path()
    
    try:
        # Reset metrics
        reset_storage_metrics()
        
        # Get storage
        storage = get_storage(db_path)
        
        # Perform multiple store operations
        for i in range(3):
            form = EchoForm(anchor=f"test_anchor_{i}", domain="test_domain", phase="active")
            form.add_term(f"test_{i}", role="metric_role", intensity=1.0, test=True)
            storage.store_form(form)
        
        # Perform multiple fetch operations
        for i in range(3):
            storage.fetch_form(f"test_anchor_{i}")
        
        # Get metrics
        metrics = get_storage_metrics()
        
        # Verify counts accumulated
        assert metrics["store_form_count"] == 3
        assert metrics["fetch_form_count"] == 3
        
        # Verify timing accumulated
        assert metrics["store_form"] > 0
        assert metrics["fetch_form"] > 0
        
        print(f"Accumulated metrics: {metrics}")
        
    finally:
        close_storage()
        if os.path.exists(db_path):
            os.unlink(db_path)


if __name__ == "__main__":
    test_storage_metrics_collection()
    test_metrics_reset()
    test_metrics_accumulation()
    print("✅ All storage metrics tests passed!")