#!/usr/bin/env python3
import subprocess
import sys
import os

# Test if make is available
try:
    result = subprocess.run(["make", "help"], capture_output=True, text=True, cwd=".")
    print("Make help output:")
    print(result.stdout)
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    print(f"Return code: {result.returncode}")
except FileNotFoundError:
    print("❌ Make not available, trying direct pytest...")
    
    # Try direct pytest
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/unit/test_echoform_core.py", "-v"], 
                          capture_output=True, text=True, cwd=".")
    print("Pytest output:")
    print(result.stdout)
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    print(f"Return code: {result.returncode}")