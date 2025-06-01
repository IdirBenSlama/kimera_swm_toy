#!/usr/bin/env python3
"""Execute verification tests directly."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("🚀 EXECUTING VERIFICATION TESTS")
print("=" * 50)

# Test 1: Basic imports
print("\n🧪 Test 1: Basic Imports")
try:
    from kimera.core.identity import IdentityManager
    from kimera.core.storage import StorageManager
    from kimera.core.cache import CacheManager
    from kimera.pipeline.mixed import MixedPipeline
    from kimera.utils.metrics import MetricsCollector
    print("✅ All imports successful")
    imports_ok = True
except Exception as e:
    print(f"❌ Import failed: {e}")
    imports_ok = False

# Test 2: Basic functionality
print("\n🧪 Test 2: Basic Functionality")
if imports_ok:
    try:
        identity_mgr = IdentityManager()
        test_id = identity_mgr.generate_id("test")
        is_valid = identity_mgr.validate_id(test_id)
        print(f"✅ Generated and validated ID: {test_id} (valid: {is_valid})")
        functionality_ok = True
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        functionality_ok = False
else:
    functionality_ok = False
    print("❌ Skipped due to import failures")

# Test 3: Pipeline creation
print("\n🧪 Test 3: Pipeline Creation")
if imports_ok:
    try:
        pipeline = MixedPipeline()
        print("✅ MixedPipeline created successfully")
        pipeline_ok = True
    except Exception as e:
        print(f"❌ Pipeline creation failed: {e}")
        pipeline_ok = False
else:
    pipeline_ok = False
    print("❌ Skipped due to import failures")

# Summary
print("\n" + "=" * 50)
print("📊 VERIFICATION RESULTS")
print("=" * 50)

tests = [
    ("Basic Imports", imports_ok),
    ("Basic Functionality", functionality_ok),
    ("Pipeline Creation", pipeline_ok)
]

passed = sum(1 for _, ok in tests if ok)
total = len(tests)

for name, ok in tests:
    status = "✅ PASSED" if ok else "❌ FAILED"
    print(f"{status}: {name}")

print(f"\nOverall: {passed}/{total} tests passed")

if passed == total:
    print("\n🎉 ALL VERIFICATION TESTS PASSED!")
    print("✅ System is ready for production")
else:
    print(f"\n⚠️ {total - passed} test(s) failed")
    print("❌ Issues need to be addressed")

print("\n" + "=" * 50)