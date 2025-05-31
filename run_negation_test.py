#!/usr/bin/env python3
"""
Run the negation test safely
"""
import subprocess
import sys

try:
    result = subprocess.run([sys.executable, "test_negation_fix.py"], 
                          capture_output=True, text=True, timeout=30)
    print("STDOUT:")
    print(result.stdout)
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    print(f"Return code: {result.returncode}")
except Exception as e:
    print(f"Error running test: {e}")