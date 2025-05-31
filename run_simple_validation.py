#!/usr/bin/env python3
"""
Simple validation runner to see the exact error
"""
import subprocess
import sys
import os

def main():
    """Run validation and show output"""
    print("🔍 Running validate_v071.py...")
    
    # Set environment to ensure UTF-8
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    try:
        result = subprocess.run(
            [sys.executable, "validate_v071.py"], 
            capture_output=True, 
            text=True, 
            timeout=60,
            env=env
        )
        
        print("Return code:", result.returncode)
        print("\n--- STDOUT ---")
        print(result.stdout)
        print("\n--- STDERR ---")
        print(result.stderr)
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ Validation timed out")
        return False
    except Exception as e:
        print(f"❌ Error running validation: {e}")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\nValidation {'passed' if success else 'failed'}")
    sys.exit(0 if success else 1)