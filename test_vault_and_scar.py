#!/usr/bin/env python3
"""
Test script to verify Vault and Scar functionality.
"""

import sys
import os
import traceback
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_basic_imports():
    """Test that core modules can be imported."""
    print("🧪 Testing basic imports...")
    
    try:
        from kimera.scar import Scar
        print("  ✅ kimera.scar imported successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import kimera.scar: {e}")
        return False
    
    try:
        from vault.core.vault import Vault
        print("  ✅ vault.core.vault imported successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import vault.core.vault: {e}")
        return False
    
    return True

def test_scar_creation():
    """Test Scar creation."""
    print("\n🧪 Testing Scar creation...")
    
    try:
        from kimera.core.scar import Scar
        
        # Create a simple scar
        scar = Scar(
            scar_id="test_scar_001",
            content="Test scar content",
            metadata={"test": True, "priority": "high"}
        )
        
        print(f"  ✅ Scar created: {scar.scar_id}")
        print(f"  📝 Content: {scar.content[:50]}...")
        print(f"  📊 Metadata: {scar.metadata}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Scar creation failed: {e}")
        traceback.print_exc()
        return False

def test_storage_operations():
    """Test storage operations with Scars."""
    print("\n🧪 Testing storage operations...")
    
    try:
        from kimera.core.scar import Scar
        from kimera.storage.lattice import LatticeStorage
        
        # Create storage
        storage = LatticeStorage()
        
        # Create and store a scar
        scar = Scar(
            scar_id="storage_test_001",
            content="Storage test content",
            metadata={"storage_test": True}
        )
        
        storage.store_scar(scar)
        print(f"  ✅ Scar stored: {scar.scar_id}")
        
        # Retrieve the scar
        retrieved = storage.get_scar("storage_test_001")
        if retrieved and retrieved.scar_id == scar.scar_id:
            print(f"  ✅ Scar retrieved: {retrieved.scar_id}")
            return True
        else:
            print("  ❌ Scar retrieval failed")
            return False
            
    except Exception as e:
        print(f"  ❌ Storage operations failed: {e}")
        traceback.print_exc()
        return False

def test_vault_snapshot():
    """Test vault snapshot functionality."""
    print("\n🧪 Testing vault snapshot...")
    
    try:
        from vault.core.vault import Vault
        
        # Create vault and store some data
        vault = Vault("test_vault")
        
        test_data = {
            "scar_count": 42,
            "system_status": "operational",
            "last_update": "2024-12-19"
        }
        
        vault.store("system_info", test_data)
        print("  ✅ Data stored in vault")
        
        # Create snapshot
        snapshot = vault.snapshot()
        if "system_info" in snapshot:
            print(f"  ✅ Snapshot created with {len(snapshot)} items")
            print(f"  📊 Snapshot data: {snapshot['system_info']}")
            return True
        else:
            print("  ❌ Snapshot creation failed")
            return False
            
    except Exception as e:
        print(f"  ❌ Vault snapshot failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Vault and Scar functionality tests...\n")
    
    tests = [
        test_basic_imports,
        test_scar_creation,
        test_storage_operations,
        test_vault_snapshot
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"  ❌ Test {test.__name__} crashed: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Kimera SWM system is operational.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)