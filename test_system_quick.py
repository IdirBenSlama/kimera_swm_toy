#!/usr/bin/env python3
"""Quick system test to verify Kimera SWM is working."""

import sys
import os
import traceback

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test basic imports."""
    print("🧪 Testing imports...")
    
    try:
        from kimera.scar import Scar
        print("  ✅ Scar imported")
        
        from vault.core.vault import Vault
        print("  ✅ Vault imported")
        
        return True
    except Exception as e:
        print(f"  ❌ Import failed: {e}")
        return False

def test_scar_creation():
    """Test Scar creation."""
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
        return True
    except Exception as e:
        print(f"  ❌ Scar creation failed: {e}")
        return False

def test_vault():
    """Test Vault functionality."""
    print("\n🧪 Testing Vault...")
    
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
        return False

def main():
    """Run quick tests."""
    print("🚀 Running quick system tests...\n")
    
    tests = [test_imports, test_scar_creation, test_vault]
    passed = 0
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 System is working!")
        return True
    else:
        print("⚠️  Some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)