#!/usr/bin/env python3
"""Test that all the fixes work correctly.

Run with: poetry run python test_fixes.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_geoid_raw_parameter():
    """Test that init_geoid accepts the raw parameter."""
    from kimera.geoid import init_geoid
    
    # Test with raw parameter
    g1 = init_geoid("Hello world", "en", ["test"], raw="Original text")
    assert g1.raw == "Original text", f"Expected 'Original text', got '{g1.raw}'"
    print("✅ init_geoid raw parameter OK")
    
    # Test without raw parameter (should default to text)
    g2 = init_geoid("Hello world", "en", ["test"])
    assert g2.raw == "Hello world", f"Expected 'Hello world', got '{g2.raw}'"

def test_benchmark_kimera_class():
    """Test that KimeraBenchmark works with text inputs and returns proper bool."""
    from benchmarks.llm_compare import KimeraBenchmark
    
    kimera = KimeraBenchmark()
    result = kimera.detect_contradiction("The sky is blue", "The sky is red")
    
    is_contra, conf, reason = result
    assert isinstance(is_contra, bool), f"Expected bool, got {type(is_contra)} (numpy.bool_ issue?)"
    assert isinstance(conf, float), f"Expected float, got {type(conf)}"
    assert isinstance(reason, str), f"Expected str, got {type(reason)}"
    print("✅ KimeraBenchmark returns native bool")

def test_streaming_functions():
    """Test that streaming functions can be imported."""
    from benchmarks.llm_compare import stream_dataset_pairs, load_dataset_efficiently
    print("✅ Streaming functions import successfully")

def main():
    print("🧪 Testing Phase 2.1 fixes...")
    
    test_geoid_raw_parameter()
    test_benchmark_kimera_class()
    test_streaming_functions()
    
    print("✅ All quick-fix checks passed")
    
    assert True  # All tests passed

if __name__ == "__main__":
    main()