#!/usr/bin/env python3
"""Run the cleanup script to remove old CI files"""

import subprocess
import sys

def main():
    print("🧹 Running workflow cleanup...")
    
    try:
        result = subprocess.run([
            sys.executable, "cleanup_workflows.py"
        ], capture_output=True, text=True)
        
        print("=== Cleanup Output ===")
        print(result.stdout)
        
        if result.stderr:
            print("=== Errors ===")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    print(f"Cleanup {'completed successfully' if success else 'failed'}")