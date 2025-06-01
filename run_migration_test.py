#!/usr/bin/env python3
"""
Run migration test with proper error handling
"""

import subprocess
import sys
import os
from pathlib import Path

def run_migration_test():
    """Run the migration test with dual-write"""
    print("🚀 Running migration test with dual-write...")
    
    # Set environment variable
    env = os.environ.copy()
    env["KIMERA_ID_DUAL_WRITE"] = "1"
    
    try:
        result = subprocess.run([
            sys.executable, "test_migration_dev.py"
        ], capture_output=True, text=True, env=env, cwd=Path(__file__).parent)
        
        print("=== STDOUT ===")
        print(result.stdout)
        
        if result.stderr:
            print("=== STDERR ===")
            print(result.stderr)
        
        print(f"=== Return Code: {result.returncode} ===")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running migration test: {e}")
        return False

if __name__ == "__main__":
    success = run_migration_test()
    if success:
        print("✅ Migration test completed successfully!")
    else:
        print("❌ Migration test failed!")
    sys.exit(0 if success else 1)