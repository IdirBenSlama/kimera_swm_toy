#!/usr/bin/env python3
"""Final verification of cache implementation."""

import subprocess
import sys

def run_pytest_test(test_path):
    """Run a specific pytest test."""
    cmd = f"poetry run pytest {test_path} -v"
    print(f"\n🧪 Running: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr and "warnings summary" not in result.stderr.lower():
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run final cache verification."""
    print("🚀 Final Cache Implementation Verification")
    print("=" * 60)
    
    tests = [
        ("tests/test_cache.py::TestEmbeddingCache::test_cache_roundtrip", "Cache Roundtrip (Timing Fix)"),
        ("tests/test_cache.py::TestEmbeddingCache::test_cache_persistence", "Cache Persistence"),
        ("tests/test_cache.py::TestEmbeddingCache::test_cache_different_languages", "Language Keying"),
        ("tests/test_cache.py::TestCacheIntegration::test_geoid_encoding_uses_cache", "Geoid Integration"),
        ("tests/test_cache.py", "Full Cache Test Suite"),
    ]
    
    results = []
    for test_path, description in tests:
        print(f"\n{'='*60}")
        print(f"🧪 {description}")
        print(f"{'='*60}")
        
        success = run_pytest_test(test_path)
        results.append((description, success))
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"\n{status}: {description}")
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 FINAL RESULTS")
    print(f"{'='*60}")
    
    passed = 0
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status}: {description}")
        if success:
            passed += 1
    
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 CACHE IMPLEMENTATION COMPLETE!")
        print("✅ All tests passing")
        print("✅ Persistence working")
        print("✅ Language keying working") 
        print("✅ Timing assertions robust")
        print("✅ Integration with geoids working")
        print("\n🚀 Ready for Phase 3: Advanced Metrics & ROC Analysis")
        return 0
    else:
        print(f"\n❌ {total - passed} tests still failing")
        print("Please review the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())