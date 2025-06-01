#!/usr/bin/env python3
"""
Quick test to verify imports work
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all required modules can be imported"""
    try:
        print("Testing imports...")
        
        # Test core imports
        from kimera.storage import LatticeStorage
        print("✅ LatticeStorage imported")
        
        from kimera.identity import create_geoid_identity, create_scar_identity
        print("✅ Identity functions imported")
        
        from kimera.echoform import EchoForm
        print("✅ EchoForm imported")
        
        # Test migration script
        import scripts.migrate_identity as migrate
        print("✅ Migration script imported")
        
        # Test observability (optional)
        try:
            from kimera.observability import get_metrics_summary
            print("✅ Observability imported")
        except ImportError as e:
            print(f"⚠️  Observability not available: {e}")
        
        # Test CLS
        from kimera.cls import lattice_resolve, create_lattice_form
        print("✅ CLS functions imported")
        
        print("🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)