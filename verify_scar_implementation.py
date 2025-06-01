#!/usr/bin/env python3
"""
Verify that Scar implementation is complete and working.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from conftest import fresh_duckdb_path

def test_imports():
    """Test that all scar-related imports work"""
    print("🔍 Testing imports...")
    
    try:
        from kimera.identity import Identity, create_scar_identity, create_geoid_identity
        from kimera.storage import LatticeStorage
        from kimera.entropy import calculate_relationship_entropy, adaptive_tau
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_scar_creation():
    """Test basic scar creation"""
    print("🔍 Testing scar creation...")
    
    try:
        from kimera.identity import create_scar_identity, Identity
        
        # Test factory function
        scar1 = create_scar_identity("id1", "id2", weight=0.8)
        assert scar1.identity_type == "scar"
        assert scar1.weight == 0.8
        assert len(scar1.related_ids) == 2
        
        # Test direct creation
        scar2 = Identity(
            identity_type="scar",
            related_ids=["a", "b", "c"],
            weight=0.9
        )
        assert scar2.identity_type == "scar"
        assert len(scar2.related_ids) == 3
        
        print("✅ Scar creation works")
        return True
    except Exception as e:
        print(f"❌ Scar creation failed: {e}")
        return False

def test_entropy_calculation():
    """Test entropy calculation for scars"""
    print("🔍 Testing entropy calculation...")
    
    try:
        from kimera.identity import create_scar_identity, Identity
        
        # Simple scar
        simple = create_scar_identity("id1", "id2")
        simple_entropy = simple.entropy()
        
        # Complex scar
        complex_scar = Identity(
            identity_type="scar",
            related_ids=["id1", "id2", "id3", "id4"],
            weight=1.0
        )
        complex_entropy = complex_scar.entropy()
        
        assert complex_entropy > simple_entropy
        assert simple_entropy > 0
        
        print(f"✅ Entropy calculation works (simple: {simple_entropy:.3f}, complex: {complex_entropy:.3f})")
        return True
    except Exception as e:
        print(f"❌ Entropy calculation failed: {e}")
        return False

def test_storage_integration():
    """Test storage integration"""
    print("🔍 Testing storage integration...")
    
    try:
        from kimera.identity import create_scar_identity, create_geoid_identity
        from kimera.storage import LatticeStorage
        
        # Create temporary database using fresh_duckdb_path
        db_path = fresh_duckdb_path()
        
        try:
            storage = LatticeStorage(db_path)
            
            # Create and store identities
            geoid = create_geoid_identity("Test concept")
            scar = create_scar_identity(geoid.id, "external_id", weight=0.7)
            
            storage.store_identity(geoid)
            storage.store_identity(scar)
            
            # Test retrieval
            retrieved_geoid = storage.fetch_identity(geoid.id)
            retrieved_scar = storage.fetch_identity(scar.id)
            
            assert retrieved_geoid is not None
            assert retrieved_scar is not None
            assert retrieved_scar.identity_type == "scar"
            
            # Test counts
            total = storage.get_identity_count()
            geoid_count = storage.get_identity_count("geoid")
            scar_count = storage.get_identity_count("scar")
            
            assert total == 2
            assert geoid_count == 1
            assert scar_count == 1
            
            storage.close()
            
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
        
        print("✅ Storage integration works")
        return True
    except Exception as e:
        print(f"❌ Storage integration failed: {e}")
        return False

def test_time_decay():
    """Test entropy-based time decay"""
    print("🔍 Testing time decay...")
    
    try:
        from kimera.identity import create_scar_identity, Identity
        
        # Simple scar
        simple = create_scar_identity("id1", "id2")
        simple_tau = simple.effective_tau()
        
        # Complex scar
        complex_scar = Identity(
            identity_type="scar",
            related_ids=["id1", "id2", "id3", "id4", "id5"],
            weight=1.0
        )
        complex_tau = complex_scar.effective_tau()
        
        assert complex_tau > simple_tau
        assert simple_tau > 0
        
        print(f"✅ Time decay works (simple: {simple_tau:.1f}s, complex: {complex_tau:.1f}s)")
        return True
    except Exception as e:
        print(f"❌ Time decay failed: {e}")
        return False

def test_metadata_support():
    """Test metadata support"""
    print("🔍 Testing metadata support...")
    
    try:
        from kimera.identity import create_scar_identity
        
        scar = create_scar_identity("id1", "id2", weight=0.8)
        scar.meta = {
            "relationship_type": "contradicts",
            "confidence": 0.9,
            "source": "test"
        }
        
        assert scar.meta["relationship_type"] == "contradicts"
        assert scar.meta["confidence"] == 0.9
        
        # Test serialization
        data = scar.to_dict()
        assert "meta" in data
        assert data["meta"]["relationship_type"] == "contradicts"
        
        print("✅ Metadata support works")
        return True
    except Exception as e:
        print(f"❌ Metadata support failed: {e}")
        return False

def test_serialization():
    """Test serialization/deserialization"""
    print("🔍 Testing serialization...")
    
    try:
        from kimera.identity import create_scar_identity, Identity
        
        # Create scar with metadata
        original = create_scar_identity("id1", "id2", weight=0.8)
        original.meta = {"type": "test", "value": 42}
        
        # Serialize
        data = original.to_dict()
        
        # Deserialize
        restored = Identity.from_dict(data)
        
        assert restored.identity_type == "scar"
        assert restored.weight == 0.8
        assert restored.related_ids == original.related_ids
        assert restored.meta["type"] == "test"
        assert restored.meta["value"] == 42
        
        print("✅ Serialization works")
        return True
    except Exception as e:
        print(f"❌ Serialization failed: {e}")
        return False

def main():
    """Run all verification tests"""
    print("🚀 Verifying Scar Implementation")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_scar_creation,
        test_entropy_calculation,
        test_storage_integration,
        test_time_decay,
        test_metadata_support,
        test_serialization
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All Scar functionality verified!")
        print("\nScar implementation is complete and working:")
        print("✅ Unified Identity model supports scars")
        print("✅ Entropy calculation for relationships")
        print("✅ Storage integration with DuckDB")
        print("✅ Entropy-based time decay")
        print("✅ Rich metadata support")
        print("✅ Serialization/deserialization")
        print("✅ Factory functions for easy creation")
        
        print("\nNext steps:")
        print("• Run 'python scar_demo.py' for a demonstration")
        print("• Run 'python test_scar_functionality.py' for comprehensive tests")
        print("• See SCAR_IMPLEMENTATION_GUIDE.md for usage examples")
        
        return True
    else:
        print(f"❌ {failed} test(s) failed - implementation needs fixes")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)