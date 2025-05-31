#!/usr/bin/env python3
"""Test v0.4.0 multiprocessing features.

Run with: poetry run python test_v040.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_multiprocessing_import():
    """Test that multiprocessing reactor can be imported."""
    from kimera.reactor_mp import reactor_cycle_parallel, reactor_cycle_threaded
    from kimera import reactor_cycle_parallel as exported_func
    from kimera import reactor_cycle_threaded as exported_threaded
    
    assert reactor_cycle_parallel is exported_func
    assert reactor_cycle_threaded is exported_threaded
    print("✅ Multiprocessing and threading reactors import correctly")

def test_multiprocessing_basic():
    """Test basic multiprocessing functionality."""
    from kimera.geoid import init_geoid
    from kimera.reactor_mp import reactor_cycle_parallel
    
    # Create test geoids
    geoids = [init_geoid(f"test {i}", "en", ["test"]) for i in range(100)]
    
    # Run with auto-detection (should use threading on Windows/small datasets)
    stats = reactor_cycle_parallel(geoids, workers=2, chunk=25)
    
    assert stats["workers"] == 2
    assert stats["geoids"] == 100
    assert stats["chunks"] == 4
    assert "latency_ms" in stats
    assert "new_scars" in stats
    assert "mode" in stats
    assert stats["mode"] in ["multiprocessing", "threading"]
    
    print(f"✅ Parallel reactor works correctly (mode: {stats['mode']})")

def test_threading_mode():
    """Test threading mode specifically."""
    from kimera.geoid import init_geoid
    from kimera.reactor_mp import reactor_cycle_threaded
    
    # Create test geoids
    geoids = [init_geoid(f"thread {i}", "en", ["test"]) for i in range(50)]
    
    # Run with threading
    stats = reactor_cycle_threaded(geoids, workers=2, chunk=25)
    
    assert stats["mode"] == "threading"
    assert stats["workers"] == 2
    assert stats["geoids"] == 50
    
    print("✅ Threading mode works correctly")

def test_demo_mp_flag():
    """Test that demo accepts --mp flag."""
    import subprocess
    import sys
    
    # Test help output includes --mp flag
    result = subprocess.run([
        sys.executable, "-m", "kimera.demo", "--help"
    ], capture_output=True, text=True, cwd=Path(__file__).parent)
    
    assert "--mp" in result.stdout
    print("✅ Demo CLI accepts --mp flag")

def test_benchmark_mp_flag():
    """Test that benchmark accepts --mp flag."""
    import subprocess
    import sys
    
    # Test help output includes --mp flag
    result = subprocess.run([
        sys.executable, "-m", "benchmarks.llm_compare", "--help"
    ], capture_output=True, text=True, cwd=Path(__file__).parent)
    
    assert "--mp" in result.stdout
    print("✅ Benchmark CLI accepts --mp flag")

def main():
    print("🧪 Testing v0.4.0 multiprocessing features...\n")
    
    test_multiprocessing_import()
    test_multiprocessing_basic()
    test_threading_mode()
    test_demo_mp_flag()
    test_benchmark_mp_flag()
    
    print("\n🎉 All v0.4.0 features working correctly!")
    print("✨ Auto-detection should use threading on Windows/small datasets!")
    print("\nNext steps:")
    print("  poetry run pytest tests/test_reactor_mp.py -v")
    print("  poetry run python -m kimera.demo data/toy_contradictions.csv --mp 4")
    print("  # Should auto-detect threading mode for better performance")
    print("\nFor larger datasets (5k+ geoids):")
    print("  poetry run python -m kimera.demo large_dataset.csv --mp 4 --chunk 1000")
    print("  # Will use multiprocessing with larger chunks")

if __name__ == "__main__":
    main()