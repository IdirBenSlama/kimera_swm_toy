#!/usr/bin/env python3
"""Check current system status."""

import sys
import os
import traceback

# Add src to path
src_path = os.path.join(os.path.dirname(__file__), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

print("🔍 CHECKING CURRENT SYSTEM STATUS")
print("=" * 50)

print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Src path: {src_path}")
print(f"Src exists: {os.path.exists(src_path)}")

# Check src structure
if os.path.exists(src_path):
    print(f"\nSrc contents:")
    for item in os.listdir(src_path):
        item_path = os.path.join(src_path, item)
        if os.path.isdir(item_path):
            print(f"  📁 {item}/")
        else:
            print(f"  📄 {item}")

# Test imports one by one
print("\n🧪 TESTING IMPORTS ONE BY ONE")
print("-" * 30)

imports_to_test = [
    ("kimera", "kimera"),
    ("kimera.core", "kimera.core"),
    ("kimera.core.identity", "kimera.core.identity"),
    ("IdentityManager", "kimera.core.identity.IdentityManager"),
    ("StorageManager", "kimera.core.storage.StorageManager"),
    ("CacheManager", "kimera.core.cache.CacheManager"),
    ("MixedPipeline", "kimera.pipeline.mixed.MixedPipeline"),
    ("MetricsCollector", "kimera.utils.metrics.MetricsCollector")
]

successful_imports = []
failed_imports = []

for name, import_path in imports_to_test:
    try:
        if "." in import_path and import_path.count(".") > 1:
            # For class imports like kimera.core.identity.IdentityManager
            module_path, class_name = import_path.rsplit(".", 1)
            module = __import__(module_path, fromlist=[class_name])
            getattr(module, class_name)
        else:
            # For module imports
            __import__(import_path)
        
        print(f"✅ {name}: SUCCESS")
        successful_imports.append(name)
    except Exception as e:
        print(f"❌ {name}: FAILED - {e}")
        failed_imports.append((name, str(e)))

print("\n" + "=" * 50)
print("📊 IMPORT STATUS SUMMARY")
print("=" * 50)

print(f"✅ Successful: {len(successful_imports)}")
for name in successful_imports:
    print(f"   - {name}")

print(f"\n❌ Failed: {len(failed_imports)}")
for name, error in failed_imports:
    print(f"   - {name}: {error}")

# If basic imports work, test functionality
if len(successful_imports) >= 3:  # At least some core imports work
    print("\n🧪 TESTING BASIC FUNCTIONALITY")
    print("-" * 30)
    
    try:
        from kimera.core.identity import IdentityManager
        identity_mgr = IdentityManager()
        test_id = identity_mgr.generate_id("test")
        print(f"✅ Generated ID: {test_id}")
        
        is_valid = identity_mgr.validate_id(test_id)
        print(f"✅ ID validation: {is_valid}")
        
        print("✅ Basic functionality working")
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        traceback.print_exc()

print("\n" + "=" * 50)
print("🏁 STATUS CHECK COMPLETE")
print("=" * 50)