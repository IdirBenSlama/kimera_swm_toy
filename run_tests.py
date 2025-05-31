#!/usr/bin/env python3
"""Run cache tests and verification."""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            return True
        else:
            print(f"❌ {description} - FAILED (exit code: {result.returncode})")
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Running Kimera Cache Tests")
    
    # Change to project directory
    project_dir = Path(__file__).parent
    
    tests = [
        ("python verify_cache.py", "Cache Verification"),
        ("python cache_demo.py", "Cache Demo"),
        ("poetry run pytest tests/test_cache.py::TestEmbeddingCache::test_cache_roundtrip -v", "Basic Cache Test"),
        ("poetry run pytest tests/test_cache.py::TestResonanceCache::test_resonance_cache_basic -v", "Resonance Cache Test"),
    ]
    
    passed = 0
    total = len(tests)
    
    for cmd, description in tests:
        if run_command(cmd, description):
            passed += 1
    
    print(f"\n{'='*60}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    print(f"{'='*60}")
    
    if passed == total:
        print("🎉 All tests passed! Cache implementation is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())