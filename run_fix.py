#!/usr/bin/env python3
"""Quick script to run the comprehensive fix."""

import subprocess
import sys

if __name__ == "__main__":
    print("Running comprehensive fix...")
    result = subprocess.run([sys.executable, "fix_critical_issues.py"])
    sys.exit(result.returncode)