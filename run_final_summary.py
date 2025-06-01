#!/usr/bin/env python3
"""Run the final status summary."""

import subprocess
import sys

def main():
    """Run the current status summary."""
    try:
        result = subprocess.run([
            sys.executable, "current_status_summary.py"
        ], text=True)
        
        return result.returncode
        
    except Exception as e:
        print(f"❌ Error running summary: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())