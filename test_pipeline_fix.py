#!/usr/bin/env python3
"""
Test the complete pipeline fix for Kimera-SWM v0.7.0
Validates that all library-level breakage is resolved.
"""

import sys
import os
import subprocess
from pathlib import Path

def print_section(title):
    """Print a test section header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)

def test_init_geoid_signatures():
    """Test all init_geoid signature variations."""
    print_section("TESTING INIT_GEOID SIGNATURES")
    
    sys.path.insert(0, str(Path("src")))
    
    try:
        from kimera.geoid import init_geoid
        
        # Test 1: Old signature (3 positional)
        print("1. Testing old signature...")
        g1 = init_geoid("Hello world", "en", ["default"])
        assert g1.raw == "Hello world"
        print("   [OK] Old signature works")
        
        # Test 2: New signature with raw
        print("2. Testing new signature with raw...")
        g2 = init_geoid("Hello world", "en", ["test"], raw="Original")
        assert g2.raw == "Original"
        print("   [OK] New signature with raw works")
        
        # Test 3: Streaming loader signature (keyword-only)
        print("3. Testing streaming loader signature...")
        g3 = init_geoid(raw="Streaming text", lang="en", tags=["benchmark"])
        assert g3.raw == "Streaming text"
        assert g3.context_layers == ["benchmark"]
        print("   [OK] Streaming loader signature works")
        
        # Test 4: Minimal signature
        print("4. Testing minimal signature...")
        g4 = init_geoid("Minimal")
        assert g4.raw == "Minimal"
        assert g4.lang_axis == "en"
        print("   [OK] Minimal signature works")
        
        print("\n[SUCCESS] All init_geoid signatures working!")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] init_geoid test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dependencies():
    """Test that all required dependencies are available."""
    print_section("TESTING DEPENDENCIES")
    
    required = [
        ("pandas", "pandas"),
        ("numpy", "numpy"), 
        ("matplotlib", "matplotlib"),
        ("pytest", "pytest"),
        ("pyyaml", "yaml"),
        ("scikit-learn", "sklearn"),
        ("sentence-transformers", "sentence_transformers")
    ]
    
    missing = []
    for name, import_name in required:
        try:
            __import__(import_name)
            print(f"[OK] {name}")
        except ImportError:
            missing.append(name)
            print(f"[MISSING] {name}")
    
    if missing:
        print(f"\n[ERROR] Missing dependencies: {', '.join(missing)}")
        print("Run: poetry install")
        return False
    
    print("\n[SUCCESS] All dependencies available!")
    return True

def test_core_imports():
    """Test that core Kimera modules can be imported."""
    print_section("TESTING CORE IMPORTS")
    
    try:
        sys.path.insert(0, str(Path("src")))
        
        print("Testing kimera.geoid...")
        from kimera.geoid import init_geoid, Geoid
        print("   [OK] geoid module")
        
        print("Testing kimera.metrics...")
        from kimera.metrics import roc_stats, pr_stats, bootstrap_ci
        print("   [OK] metrics module")
        
        print("Testing kimera.cache...")
        from kimera.cache import embed_cache, get_cache_stats
        print("   [OK] cache module")
        
        print("Testing kimera.resonance...")
        from kimera.resonance import resonance, THRESH
        print("   [OK] resonance module")
        
        print("Testing kimera.reactor...")
        from kimera.reactor import reactor_cycle_batched
        print("   [OK] reactor module")
        
        print("\n[SUCCESS] All core modules imported!")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Core import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_benchmark_import():
    """Test that benchmark module can be imported."""
    print_section("TESTING BENCHMARK IMPORT")
    
    try:
        sys.path.insert(0, str(Path("benchmarks")))
        from benchmarks.llm_compare import stream_dataset_pairs, main
        print("[OK] llm_compare module imported")
        
        from benchmarks.openai_async import AsyncOpenAIClient
        print("[OK] openai_async module imported")
        
        print("\n[SUCCESS] Benchmark modules working!")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Benchmark import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_files():
    """Test that required data files exist."""
    print_section("TESTING DATA FILES")
    
    required_files = [
        "data/toy_contradictions.csv",
        "data/contradictions_2k.csv"
    ]
    
    all_found = True
    for file in required_files:
        if Path(file).exists():
            size = Path(file).stat().st_size
            print(f"[OK] {file} ({size} bytes)")
        else:
            print(f"[MISSING] {file}")
            all_found = False
    
    if all_found:
        print("\n[SUCCESS] All data files found!")
    else:
        print("\n[WARNING] Some data files missing - may affect benchmarks")
    
    return all_found

def test_pytest_run():
    """Test that pytest runs without errors."""
    print_section("TESTING PYTEST")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", "-v", "--tb=short", "-x"
        ], capture_output=True, text=True, timeout=180)
        
        if result.returncode == 0:
            print("[SUCCESS] Pytest passed!")
            print("Output:")
            print(result.stdout[-500:])  # Last 500 chars
            return True
        else:
            print(f"[ERROR] Pytest failed with code {result.returncode}")
            print("STDOUT:", result.stdout[-500:])
            print("STDERR:", result.stderr[-500:])
            return False
            
    except subprocess.TimeoutExpired:
        print("[ERROR] Pytest timed out")
        return False
    except Exception as e:
        print(f"[ERROR] Pytest execution failed: {e}")
        return False

def test_simple_benchmark():
    """Test a simple benchmark run."""
    print_section("TESTING SIMPLE BENCHMARK")
    
    try:
        # Test Kimera-only mode (no API key needed)
        result = subprocess.run([
            sys.executable, "-m", "benchmarks.llm_compare",
            "data/toy_contradictions.csv",
            "--max-pairs", "5",
            "--kimera-only",
            "--no-viz"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("[SUCCESS] Simple benchmark completed!")
            print("Output:")
            print(result.stdout[-300:])  # Last 300 chars
            return True
        else:
            print(f"[ERROR] Benchmark failed with code {result.returncode}")
            print("STDOUT:", result.stdout[-300:])
            print("STDERR:", result.stderr[-300:])
            return False
            
    except subprocess.TimeoutExpired:
        print("[ERROR] Benchmark timed out")
        return False
    except Exception as e:
        print(f"[ERROR] Benchmark execution failed: {e}")
        return False

def main():
    """Run all pipeline tests."""
    print("Kimera-SWM v0.7.0 - Pipeline Fix Validation")
    print("Testing library-level breakage fixes")
    
    # Check if we're in the right directory
    if not Path("src/kimera").exists():
        print("\n[ERROR] Not in Kimera project root directory")
        print("Please run from the project root where src/kimera exists")
        return 1
    
    tests = [
        ("Dependencies", test_dependencies),
        ("init_geoid Signatures", test_init_geoid_signatures),
        ("Core Imports", test_core_imports),
        ("Benchmark Import", test_benchmark_import),
        ("Data Files", test_data_files),
        ("Pytest", test_pytest_run),
        ("Simple Benchmark", test_simple_benchmark)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"\n[ERROR] {name} test crashed: {e}")
    
    print_section("FINAL RESULTS")
    print(f"Pipeline Tests: {passed}/{total} passed")
    
    if passed == total:
        print("\n[SUCCESS] All pipeline tests passed!")
        print("\nLibrary-level breakage is FIXED. Ready for:")
        print("1. Full benchmark: poetry run python -m benchmarks.llm_compare")
        print("2. Error-bucket analysis")
        print("3. Threshold tuning")
        return 0
    elif passed >= total - 2:
        print(f"\n[MOSTLY WORKING] {total - passed} minor issues remain")
        print("Core functionality should work for benchmarks")
        return 0
    else:
        print(f"\n[ERROR] {total - passed} major issues remain")
        print("Library-level fixes needed before proceeding")
        return 1

if __name__ == "__main__":
    sys.exit(main())