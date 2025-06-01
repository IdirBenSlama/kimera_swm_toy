#!/usr/bin/env python3
"""
Test the storage connection fix we applied
"""

import sys
import os
import tempfile
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_storage_connection_management():
    """Test that storage connections are properly managed"""
    print("🧪 Testing Storage Connection Management")
    print("=" * 45)
    
    try:
        from kimera.storage import LatticeStorage
        from kimera.echoform import EchoForm
        print("✅ Imports successful")
        
        # Create temporary database using the fixed pattern
        def fresh_duckdb_path():
            fd, path = tempfile.mkstemp(suffix=".db")
            os.close(fd)        # close handle
            os.unlink(path)     # remove file so DuckDB can create it
            return path
        
        db_path = fresh_duckdb_path()
        print(f"✅ Created temp DB path: {db_path}")
        
        storage = None
        
        try:
            # Test storage creation
            storage = LatticeStorage(db_path)
            print("✅ Storage created successfully")
            
            # Test basic operation
            initial_count = storage.get_form_count()
            print(f"✅ Initial form count: {initial_count}")
            
            # Create and store a test form
            form = EchoForm(
                anchor="connection_test",
                domain="test",
                terms=[{"symbol": "test", "role": "test_role", "intensity": 0.5}],
                phase="test_phase"
            )
            storage.store_form(form)
            print("✅ Form stored successfully")
            
            # Verify storage works
            count = storage.get_form_count()
            print(f"✅ Form count after storage: {count}")
            
            assert count == initial_count + 1, f"Expected {initial_count + 1} forms, got {count}"
            print("✅ Storage verification successful")
            
        finally:
            # Test the connection management fix
            if storage:
                storage.close()
                print("✅ Storage connection closed")
            
            if os.path.exists(db_path):
                os.remove(db_path)
                print("✅ Temp database file removed")
        
        print("\n🎉 Storage connection management test PASSED!")
        return 0
        
    except Exception as e:
        print(f"\n❌ Storage connection management test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(test_storage_connection_management())