#!/usr/bin/env python3
"""Run cache tests to verify fixes."""

import subprocess
import sys

def run_test(test_name):
    """Run a specific test and return success status."""
    cmd = f"poetry run pytest tests/test_cache.py::{test_name} -v"
    print(f"\n🧪 Running {test_name}...")
    print(f"Command: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        success = result.returncode == 0
        print(f"{'✅ PASS' if success else '❌ FAIL'}: {test_name}")
        return success
    except Exception as e:
        print(f"❌ ERROR running {test_name}: {e}")
        return False

def main():
    """Run the specific tests that were failing."""
    print("🚀 Testing cache fixes...")
    
    tests = [
        "TestEmbeddingCache::test_cache_persistence",
        "TestEmbeddingCache::test_cache_different_languages",
        "TestEmbeddingCache::test_cache_roundtrip",
    ]
    
    results = []
    for test in tests:
        results.append(run_test(test))
    
    print(f"\n📊 Summary:")
    for i, test in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"  {status}: {test}")
    
    passed = sum(results)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All cache fixes working!")
        return 0
    else:
        print("❌ Some tests still failing.")
        return 1

if __name__ == "__main__":
    sys.exit(main())