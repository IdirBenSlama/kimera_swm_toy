#!/usr/bin/env python3
"""
Quick test to verify Scar functionality is working after DuckDB fix.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from conftest import fresh_duckdb_path

def test_scar_basic():
    """Quick test of basic scar functionality"""
    print("🧪 Quick Scar Test")
    
    try:
        # Test imports
        from kimera.identity import Identity, create_scar_identity
        from kimera.storage import LatticeStorage
        print("✅ Imports successful")
        
        # Test scar creation
        scar = create_scar_identity("concept_a", "concept_b", weight=0.8)
        assert scar.identity_type == "scar"
        assert scar.weight == 0.8
        print("✅ Scar creation successful")
        
        # Test storage with fixed DuckDB path
        db_path = fresh_duckdb_path()
        storage = LatticeStorage(db_path)
        
        # Store and retrieve
        storage.store_identity(scar)
        retrieved = storage.fetch_identity(scar.id)
        
        assert retrieved is not None
        assert retrieved.identity_type == "scar"
        print("✅ Storage and retrieval successful")
        
        storage.close()
        
        # Clean up
        if os.path.exists(db_path):
            os.unlink(db_path)
        
        print("🎉 All tests passed! Scar functionality is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_scar_basic()
    sys.exit(0 if success else 1)