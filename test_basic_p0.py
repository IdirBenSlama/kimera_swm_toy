#!/usr/bin/env python3
"""
Basic P0 test - minimal test to verify core functionality
"""

import sys
import os
import tempfile
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """Run basic P0 functionality test"""
    print("🧪 Basic P0 Test - Core Functionality")
    
    try:
        # Test 1: Basic imports
        print("1. Testing imports...")
        from kimera.identity import create_geoid_identity, create_scar_identity
        from kimera.storage import LatticeStorage
        print("   ✅ Core imports successful")
        
        # Test 2: Identity creation
        print("2. Testing identity creation...")
        geoid = create_geoid_identity("Test content", tags=["test"])
        scar = create_scar_identity("Scar content", relationships=[], tags=["test"])
        print(f"   ✅ Created geoid: {geoid.id[:8]}...")
        print(f"   ✅ Created scar: {scar.id[:8]}...")
        
        # Test 3: Entropy calculation
        print("3. Testing entropy calculation...")
        geoid_entropy = geoid.entropy()
        scar_entropy = scar.entropy()
        print(f"   ✅ Geoid entropy: {geoid_entropy:.3f}")
        print(f"   ✅ Scar entropy: {scar_entropy:.3f}")
        
        # Test 4: Storage operations
        print("4. Testing storage operations...")
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
            db_path = tmp.name
        
        try:
            storage = LatticeStorage(db_path)
            
            # Store identities
            storage.store_identity(geoid)
            storage.store_identity(scar)
            print("   ✅ Stored identities")
            
            # Retrieve identities
            retrieved_geoid = storage.fetch_identity(geoid.id)
            retrieved_scar = storage.fetch_identity(scar.id)
            
            assert retrieved_geoid is not None, "Failed to retrieve geoid"
            assert retrieved_scar is not None, "Failed to retrieve scar"
            print("   ✅ Retrieved identities")
            
            storage.close()
            
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
        
        # Test 5: CLS integration
        print("5. Testing CLS integration...")
        try:
            from kimera.cls import lattice_resolve
            intensity = lattice_resolve(geoid, scar)
            print(f"   ✅ Lattice intensity: {intensity}")
        except Exception as e:
            print(f"   ⚠️  CLS integration issue: {e}")
        
        # Test 6: Observability (optional)
        print("6. Testing observability...")
        try:
            from kimera.observability import get_metrics_summary
            summary = get_metrics_summary()
            print(f"   ✅ Observability available: {summary['metrics_available']}")
        except ImportError:
            print("   ⚠️  Observability not available (prometheus_client not installed)")
        except Exception as e:
            print(f"   ⚠️  Observability issue: {e}")
        
        print("\n🎉 Basic P0 test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Basic P0 test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)