#!/usr/bin/env python3
"""
Run the scar functionality test.
"""

import subprocess
import sys
import os

def main():
    """Run the scar test"""
    print("🚀 Running Scar Functionality Test")
    
    # Set environment variable for clean database
    env = os.environ.copy()
    env["KIMERA_DB_PATH"] = ":memory:"
    
    try:
        result = subprocess.run([
            sys.executable, "test_scar_functionality.py"
        ], env=env, capture_output=True, text=True, timeout=30)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ Scar test passed!")
        else:
            print(f"❌ Scar test failed with return code {result.returncode}")
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ Test timed out")
        return False
    except Exception as e:
        print(f"❌ Error running test: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)