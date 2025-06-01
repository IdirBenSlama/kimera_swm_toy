#!/usr/bin/env python3
"""Quick test of the enhanced benchmark system."""

import sys
import subprocess
from pathlib import Path

def test_kimera_only_mode():
    """Test that the benchmark works in Kimera-only mode."""
    print("Testing Kimera-only benchmark...")
    
    result = subprocess.run([
        sys.executable, "-m", "benchmarks.llm_compare",
        "--kimera-only", "--max-pairs", "3", "--no-viz"
    ], capture_output=True, text=True, cwd=Path(__file__).parent.parent.parent)
    
    print(f"Return code: {result.returncode}")
    print(f"STDOUT:\n{result.stdout}")
    if result.stderr:
        print(f"STDERR:\n{result.stderr}")
    
    if result.returncode == 0:
        print("✅ Benchmark completed successfully!")
        assert True
    else:
        print("❌ Benchmark failed")
        assert False, f"Benchmark failed with return code {result.returncode}"

def test_help_message():
    """Test that help message works."""
    print("\nTesting help message...")
    
    result = subprocess.run([
        sys.executable, "-m", "benchmarks.llm_compare", "--help"
    ], capture_output=True, text=True, cwd=Path(__file__).parent.parent.parent)
    
    if result.returncode == 0 and "Benchmark Kimera vs GPT-4o" in result.stdout:
        print("✅ Help message works!")
        assert True
    else:
        print("❌ Help message failed")
        assert False, f"Help message failed: {result.stdout}"

if __name__ == "__main__":
    print("🧪 Testing enhanced benchmark system...\n")
    
    help_ok = test_help_message()
    benchmark_ok = test_kimera_only_mode()
    
    if help_ok and benchmark_ok:
        print("\n🎉 All tests passed! Benchmark system is ready.")
    else:
        print("\n💥 Some tests failed.")