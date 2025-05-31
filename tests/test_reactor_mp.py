"""Tests for multiprocessing reactor functionality."""

import pytest
from kimera.geoid import init_geoid
from kimera.reactor_mp import reactor_cycle_parallel, reactor_cycle_threaded


def test_reactor_parallel_basic():
    """Test basic multiprocessing reactor functionality."""
    # Create test geoids
    geoids = [init_geoid(f"test text {i}", "en", ["test"]) for i in range(400)]
    
    # Run parallel processing
    stats = reactor_cycle_parallel(geoids, workers=2, chunk=100)
    
    # Verify stats structure
    assert "workers" in stats
    assert "geoids" in stats
    assert "latency_ms" in stats
    assert "mem_mb" in stats
    assert "new_scars" in stats
    assert "chunks" in stats
    assert "mode" in stats
    
    # Verify values
    assert stats["workers"] == 2
    assert stats["geoids"] == 400
    assert stats["chunks"] == 4  # 400 geoids / 100 chunk size
    assert stats["new_scars"] >= 0  # Should be non-negative
    assert stats["latency_ms"] > 0  # Should take some time
    assert stats["mode"] in ["multiprocessing", "threading"]  # Should auto-detect


def test_reactor_threaded():
    """Test threading-based reactor functionality."""
    geoids = [init_geoid(f"thread test {i}", "en", ["test"]) for i in range(200)]
    
    # Force threading mode
    stats = reactor_cycle_threaded(geoids, workers=2, chunk=50)
    
    assert stats["workers"] == 2
    assert stats["geoids"] == 200
    assert stats["chunks"] == 4
    assert stats["mode"] == "threading"
    assert stats["new_scars"] >= 0


def test_reactor_parallel_force_multiprocessing():
    """Test forcing multiprocessing mode."""
    geoids = [init_geoid(f"mp test {i}", "en", ["test"]) for i in range(100)]
    
    # Force multiprocessing mode
    stats = reactor_cycle_parallel(geoids, workers=1, chunk=50, use_threading=False)
    
    assert stats["workers"] == 1
    assert stats["geoids"] == 100
    assert stats["mode"] == "multiprocessing"


def test_reactor_parallel_force_threading():
    """Test forcing threading mode."""
    geoids = [init_geoid(f"thread test {i}", "en", ["test"]) for i in range(100)]
    
    # Force threading mode
    stats = reactor_cycle_parallel(geoids, workers=2, chunk=50, use_threading=True)
    
    assert stats["workers"] == 2
    assert stats["geoids"] == 100
    assert stats["mode"] == "threading"


def test_reactor_parallel_auto_workers():
    """Test automatic worker count detection."""
    geoids = [init_geoid(f"text {i}", "en", ["test"]) for i in range(200)]
    
    # Don't specify workers (should auto-detect)
    stats = reactor_cycle_parallel(geoids, chunk=50)
    
    assert stats["workers"] >= 1  # Should have at least 1 worker
    assert stats["geoids"] == 200
    assert stats["chunks"] == 4  # 200 geoids / 50 chunk size


def test_reactor_parallel_small_dataset():
    """Test with small dataset (fewer geoids than chunk size)."""
    geoids = [init_geoid(f"small {i}", "en", ["test"]) for i in range(50)]
    
    stats = reactor_cycle_parallel(geoids, workers=1, chunk=100)
    
    assert stats["workers"] == 1
    assert stats["geoids"] == 50
    assert stats["chunks"] == 1  # All geoids fit in one chunk
    assert stats["new_scars"] >= 0


def test_reactor_parallel_empty_dataset():
    """Test with empty dataset."""
    geoids = []
    
    stats = reactor_cycle_parallel(geoids, workers=1, chunk=100)
    
    assert stats["workers"] == 1
    assert stats["geoids"] == 0
    assert stats["chunks"] == 0
    assert stats["new_scars"] == 0


def test_reactor_parallel_single_worker():
    """Test with single worker (should still work)."""
    geoids = [init_geoid(f"single {i}", "en", ["test"]) for i in range(100)]
    
    stats = reactor_cycle_parallel(geoids, workers=1, chunk=25)
    
    assert stats["workers"] == 1
    assert stats["geoids"] == 100
    assert stats["chunks"] == 4
    assert stats["new_scars"] >= 0