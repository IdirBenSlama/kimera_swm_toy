#!/usr/bin/env python3
"""
Simple P0 test to verify basic functionality
"""

import sys
import os
import tempfile
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import safe console for Windows compatibility
from kimera.utils.safe_console import safe_print

def test_basic_identity():
    """Test basic identity creation and storage"""
    safe_print("🧪 Testing basic identity functionality...")
    
    try:
        from kimera.identity import create_geoid_identity, create_scar_identity
        from kimera.storage import LatticeStorage
        
        # Create identities
        geoid = create_geoid_identity("Test content", tags=["test"])
        scar = create_scar_identity("Scar content", relationships=[], tags=["test"])
        
        safe_print(f"✅ Created geoid: {geoid.id}")
        safe_print(f"✅ Created scar: {scar.id}")
        
        # Test entropy
        geoid_entropy = geoid.entropy()
        scar_entropy = scar.entropy()
        
        safe_print(f"✅ Geoid entropy: {geoid_entropy:.3f}")
        safe_print(f"✅ Scar entropy: {scar_entropy:.3f}")
        
        # Test storage
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
            db_path = tmp.name
        
        try:
            storage = LatticeStorage(db_path)
            
            # Store identities
            storage.store_identity(geoid)
            storage.store_identity(scar)
            
            # Retrieve identities
            retrieved_geoid = storage.fetch_identity(geoid.id)
            retrieved_scar = storage.fetch_identity(scar.id)
            
            assert retrieved_geoid is not None, "Failed to retrieve geoid"
            assert retrieved_scar is not None, "Failed to retrieve scar"
            
            safe_print("✅ Storage and retrieval working")
            
            storage.close()
            
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
        
        return True
        
    except Exception as e:
        safe_print(f"❌ Basic identity test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cls_integration():
    """Test CLS integration"""
    safe_print("🧪 Testing CLS integration...")
    
    try:
        from kimera.identity import create_geoid_identity
        from kimera.cls import lattice_resolve
        
        # Create test identities
        identity_a = create_geoid_identity("Content A", tags=["test"])
        identity_b = create_geoid_identity("Content B", tags=["test"])
        
        # Test lattice resolve
        intensity = lattice_resolve(identity_a, identity_b)
        
        safe_print(f"✅ Lattice intensity: {intensity}")
        assert isinstance(intensity, (int, float)), "Intensity should be numeric"
        
        return True
        
    except Exception as e:
        safe_print(f"❌ CLS integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_observability():
    """Test observability hooks"""
    safe_print("🧪 Testing observability...")
    
    try:
        # Test if observability can be imported
        try:
            from kimera.observability import get_metrics_summary
            safe_print("✅ Observability available")
            
            # Test metrics
            summary = get_metrics_summary()
            safe_print(f"✅ Metrics summary: {summary}")
            
        except ImportError:
            safe_print("⚠️  Observability not available (prometheus_client not installed)")
            safe_print("✅ Graceful fallback working")
        
        return True
        
    except Exception as e:
        safe_print(f"❌ Observability test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run simple P0 tests"""
    safe_print("🚀 Running Simple P0 Tests\n")
    
    tests = [
        test_basic_identity,
        test_cls_integration,
        test_observability
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            safe_print("")
        except Exception as e:
            safe_print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
            safe_print("")
    
    passed = sum(results)
    total = len(results)
    
    safe_print(f"📊 Simple P0 Results: {passed}/{total} passed")
    
    if passed == total:
        safe_print("🎉 All simple P0 tests passed!")
        return True
    else:
        safe_print("💥 Some simple P0 tests failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)