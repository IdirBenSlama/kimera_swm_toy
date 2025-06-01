#!/usr/bin/env python3
"""Quick test to verify import fixes."""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all imports work correctly."""
    print("🧪 Testing imports after fixes...")
    
    try:
        # Test kimera.scar import (the main issue)
        from kimera.scar import Scar, create_scar
        print("  ✅ kimera.scar imports working")
        
        # Test other kimera imports
        from kimera.identity import Identity, create_scar_identity
        print("  ✅ kimera.identity imports working")
        
        from kimera.storage import LatticeStorage
        print("  ✅ kimera.storage imports working")
        
        # Test vault import
        from vault.core.vault import Vault
        print("  ✅ vault.core.vault imports working")
        
        print("  🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"  ❌ Import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_scar_creation():
    """Test creating a Scar object."""
    print("\n🧪 Testing Scar creation...")
    
    try:
        from kimera.scar import Scar
        from datetime import datetime
        
        scar = Scar(
            scar_id="test_001",
            gid_pair=("gid1", "gid2"),
            weight=0.8,
            timestamp=datetime.utcnow()
        )
        
        print(f"  ✅ Scar created: {scar.scar_id}")
        print(f"  ✅ GID pair: {scar.gid_pair}")
        print(f"  ✅ Weight: {scar.weight}")
        return True
        
    except Exception as e:
        print(f"  ❌ Scar creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_vault_creation():
    """Test creating a Vault object."""
    print("\n🧪 Testing Vault creation...")
    
    try:
        from vault.core.vault import Vault
        
        vault = Vault("test_vault")
        vault.store("test_key", {"data": "test_value"})
        retrieved = vault.retrieve("test_key")
        
        if retrieved and retrieved.get("data") == "test_value":
            print("  ✅ Vault store/retrieve working")
            return True
        else:
            print("  ❌ Vault store/retrieve failed")
            return False
            
    except Exception as e:
        print(f"  ❌ Vault test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🚀 Running import fix verification tests...\n")
    
    tests = [test_imports, test_scar_creation, test_vault_creation]
    passed = 0
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All import fixes working correctly!")
        return True
    else:
        print("⚠️  Some tests failed - check import paths")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)