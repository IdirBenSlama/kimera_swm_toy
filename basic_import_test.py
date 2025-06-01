#!/usr/bin/env python3
"""
Basic import test - just check if we can import the modules
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    print("🔍 Basic Import Test")
    print("=" * 30)
    
    print(f"Python version: {sys.version}")
    print(f"Working directory: {Path.cwd()}")
    
    # Test 1: Import kimera package
    print("\n1. Testing kimera package import...")
    try:
        import kimera
        print("✅ kimera imported successfully")
    except Exception as e:
        print(f"❌ kimera import failed: {e}")
        return 1
    
    # Test 2: Import storage
    print("\n2. Testing storage import...")
    try:
        from kimera.storage import LatticeStorage
        print("✅ LatticeStorage imported successfully")
    except Exception as e:
        print(f"❌ LatticeStorage import failed: {e}")
        return 1
    
    # Test 3: Import identity
    print("\n3. Testing identity import...")
    try:
        from kimera.identity import Identity, create_geoid_identity
        print("✅ Identity imports successful")
    except Exception as e:
        print(f"❌ Identity import failed: {e}")
        return 1
    
    # Test 4: Import echoform
    print("\n4. Testing echoform import...")
    try:
        from kimera.echoform import EchoForm
        print("✅ EchoForm imported successfully")
    except Exception as e:
        print(f"❌ EchoForm import failed: {e}")
        return 1
    
    print("\n✅ All basic imports successful!")
    return 0

if __name__ == "__main__":
    sys.exit(main())