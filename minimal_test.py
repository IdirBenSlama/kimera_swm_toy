#!/usr/bin/env python3
"""
Minimal test to check if anything works
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("Python version:", sys.version)
print("Current directory:", os.getcwd())
print("Python path:", sys.path[:3])  # Show first 3 entries

# Test 1: Can we import anything?
print("\n=== Testing Imports ===")
try:
    import kimera
    print("✅ kimera package imported")
except Exception as e:
    print(f"❌ kimera package failed: {e}")

try:
    from kimera import storage
    print("✅ kimera.storage imported")
except Exception as e:
    print(f"❌ kimera.storage failed: {e}")

try:
    from kimera.storage import LatticeStorage
    print("✅ LatticeStorage imported")
except Exception as e:
    print(f"❌ LatticeStorage failed: {e}")

# Test 2: Can we create a storage instance?
print("\n=== Testing Storage Creation ===")
try:
    from kimera.storage import LatticeStorage
    import tempfile
    
    # Create temp file
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.unlink(db_path)
    
    print(f"Temp DB path: {db_path}")
    
    storage = LatticeStorage(db_path)
    print("✅ Storage created")
    
    storage.close()
    print("✅ Storage closed")
    
    if os.path.exists(db_path):
        os.remove(db_path)
        print("✅ Temp file cleaned up")
    
except Exception as e:
    print(f"❌ Storage creation failed: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Test Complete ===")