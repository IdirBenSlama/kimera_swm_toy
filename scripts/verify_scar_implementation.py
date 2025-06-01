#!/usr/bin/env python3
"""
Verify SCAR implementation is working correctly
"""
import sys
import os
sys.path.insert(0, 'src')

def verify_scar_imports():
    """Verify SCAR-related imports work"""
    try:
        from kimera.identity import Identity
        from kimera.storage import LatticeStorage
        print("✅ SCAR imports successful")
        return True
    except ImportError as e:
        print(f"❌ SCAR import failed: {e}")
        return False

def verify_scar_creation():
    """Verify SCAR creation functionality"""
    try:
        from kimera.identity import Identity
        
        # Create a test scar
        scar = Identity.create_scar(
            content="test scar",
            related_ids=["id1", "id2"],
            metadata={"relationship_type": "test"}
        )
        
        assert scar.identity_type == "scar"
        assert "related_ids" in scar.metadata
        assert scar.metadata["related_ids"] == ["id1", "id2"]
        
        print("✅ SCAR creation successful")
        return True
    except Exception as e:
        print(f"❌ SCAR creation failed: {e}")
        return False

def verify_scar_storage():
    """Verify SCAR storage functionality"""
    try:
        from kimera.identity import Identity
        from kimera.storage import LatticeStorage
        
        # Create temporary storage
        test_db = "test_scar_verify.db"
        if os.path.exists(test_db):
            os.remove(test_db)
        
        storage = LatticeStorage(db_path=test_db)
        
        # Create and store a scar
        scar = Identity.create_scar(
            content="verification scar",
            related_ids=["verify1", "verify2"],
            metadata={"relationship_type": "verification"}
        )
        
        storage.store_identity(scar)
        
        # Retrieve the scar
        retrieved = storage.get_identity(scar.id)
        assert retrieved is not None
        assert retrieved.identity_type == "scar"
        
        # Cleanup
        if os.path.exists(test_db):
            os.remove(test_db)
        
        print("✅ SCAR storage successful")
        return True
    except Exception as e:
        print(f"❌ SCAR storage failed: {e}")
        return False

def verify_vault_integration():
    """Verify Vault integration with SCAR"""
    try:
        # Check if vault directory exists
        if not os.path.exists("vault"):
            print("⚠️  Vault directory not found")
            return False
        
        if not os.path.exists("vault/core"):
            print("⚠️  Vault core directory not found")
            return False
        
        print("✅ Vault infrastructure exists")
        return True
    except Exception as e:
        print(f"❌ Vault verification failed: {e}")
        return False

def main():
    """Run all SCAR verification tests"""
    print("🔍 Verifying SCAR implementation...")
    print("=" * 50)
    
    tests = [
        ("Import Verification", verify_scar_imports),
        ("SCAR Creation", verify_scar_creation),
        ("SCAR Storage", verify_scar_storage),
        ("Vault Integration", verify_vault_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"🎯 SCAR Verification Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All SCAR functionality verified!")
        return True
    else:
        print("❌ Some SCAR tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)