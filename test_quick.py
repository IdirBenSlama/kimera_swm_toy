#!/usr/bin/env python3
"""Quick test to verify the benchmark works with the new raw field."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from kimera.geoid import init_geoid
from kimera.dataset import load_toy_dataset

def test_geoid_raw_field():
    """Test that geoids have the raw field."""
    g = init_geoid("Test sentence", "en", ["default"])
    print(f"✓ Geoid raw field: '{g.raw}'")
    assert g.raw == "Test sentence"

def test_dataset_loading():
    """Test that dataset loading works."""
    try:
        geoids = load_toy_dataset(Path("data/toy_contradictions.csv"))
        print(f"✓ Loaded {len(geoids)} geoids from dataset")
        if geoids:
            print(f"✓ First geoid raw: '{geoids[0].raw[:50]}...'")
        assert len(geoids) > 0, "Dataset should contain geoids"
        assert True  # Test passed
    except Exception as e:
        print(f"✗ Dataset loading failed: {e}")
        assert False, f"Dataset loading failed: {e}"

def test_benchmark_import():
    """Test that benchmark can be imported."""
    try:
        sys.path.insert(0, str(Path(__file__).parent / "benchmarks"))
        from benchmarks import llm_compare
        print("✓ Benchmark module imports successfully")
        assert hasattr(llm_compare, 'run_benchmark'), "Module should have run_benchmark function"
        assert True  # Test passed
    except Exception as e:
        print(f"✗ Benchmark import failed: {e}")
        assert False, f"Benchmark import failed: {e}"

if __name__ == "__main__":
    print("Running quick tests...")
    
    test_geoid_raw_field()
    test_dataset_loading()
    test_benchmark_import()
    
    print("\n✓ All tests completed! Ready to run benchmark.")
    print("\nTry: poetry run python -m benchmarks.llm_compare --kimera-only --max-pairs 5")