#!/usr/bin/env python3
"""
Run the unified identity test to verify our fixes
"""

import subprocess
import sys
import os
from pathlib import Path

def run_test():
    """Run the unified identity test"""
    print("🧪 Running Unified Identity Test")
    print("=" * 40)
    
    # Change to the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    try:
        # Run the test script
        result = subprocess.run([
            sys.executable, "test_unified_identity.py"
        ], capture_output=True, text=True, timeout=120)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)
        
        print(f"\nExit code: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ Test passed!")
        else:
            print("❌ Test failed!")
            
        return result.returncode
        
    except subprocess.TimeoutExpired:
        print("❌ Test timed out after 2 minutes")
        return 1
    except Exception as e:
        print(f"❌ Failed to run test: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run_test())