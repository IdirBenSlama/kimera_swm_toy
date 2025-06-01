#!/usr/bin/env python3
"""
Run the quick verification test
"""

import subprocess
import sys
import os
from pathlib import Path

def run_quick_test():
    """Run the quick verification test"""
    print("🚀 Running Quick Verification Test")
    print("=" * 40)
    
    # Change to the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    try:
        # Run the quick test script
        result = subprocess.run([
            sys.executable, "quick_verification_test.py"
        ], capture_output=True, text=True, timeout=60)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)
        
        print(f"\nExit code: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ Quick test passed!")
        else:
            print("❌ Quick test failed!")
            
        return result.returncode
        
    except subprocess.TimeoutExpired:
        print("❌ Test timed out after 1 minute")
        return 1
    except Exception as e:
        print(f"❌ Failed to run test: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run_quick_test())