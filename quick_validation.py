#!/usr/bin/env python3
"""
Quick validation of key fixes
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test basic imports work"""
    try:
        # Test A: Benchmark CLI
        print("Testing benchmark CLI import...")
        from benchmarks.llm_compare import main
        print("✅ Benchmark CLI imports")
        
        # Test B: init_geoid import
        print("Testing init_geoid import...")
        from kimera.echoform import init_geoid
        print("✅ init_geoid imports")
        
        # Test C: Storage imports
        print("Testing storage imports...")
        from kimera.storage import LatticeStorage
        print("✅ Storage imports")
        
        # Test D: Migration script
        print("Testing migration script...")
        from scripts.migrate_lattice_to_db import safe_print
        print("✅ Migration script imports")
        
        # Test E: Reactor MP
        print("Testing reactor MP...")
        from kimera.reactor_mp import Geoid
        print("✅ Reactor MP imports")
        
        print("\n🎉 All critical imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)