#!/usr/bin/env python3
"""
Quick runner for P0 integration tests
"""

import subprocess
import sys
from pathlib import Path

def run_p0_tests():
    """Run the P0 integration test suite"""
    print("🚀 Running P0 Integration Tests...")
    
    try:
        # Run the P0 integration test
        result = subprocess.run([
            sys.executable, "test_p0_integration.py"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ P0 tests completed successfully!")
        else:
            print("❌ P0 tests failed!")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running P0 tests: {e}")
        return False

def run_migration_markers():
    """Run the pytest migration markers"""
    print("\n🧪 Running Migration Marker Tests...")
    
    try:
        result = subprocess.run([
            sys.executable, "pytest_migration_marker.py"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ Migration marker tests completed successfully!")
        else:
            print("❌ Migration marker tests failed!")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running migration marker tests: {e}")
        return False

if __name__ == "__main__":
    success = True
    
    success &= run_p0_tests()
    success &= run_migration_markers()
    
    if success:
        print("\n🎉 All P0 tests passed! Ready for next phase.")
    else:
        print("\n💥 Some P0 tests failed. Check output above.")
    
    sys.exit(0 if success else 1)