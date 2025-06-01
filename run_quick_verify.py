#!/usr/bin/env python3
import subprocess
import sys

result = subprocess.run([sys.executable, "quick_verify.py"], capture_output=True, text=True)
print("STDOUT:")
print(result.stdout)
if result.stderr:
    print("STDERR:")
    print(result.stderr)
print(f"Return code: {result.returncode}")