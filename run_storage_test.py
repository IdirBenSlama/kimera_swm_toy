#!/usr/bin/env python3
import subprocess
import sys
import os

# Set up environment
env = os.environ.copy()
env['PYTHONPATH'] = 'src'

print("🧪 Running Storage unit tests...")

# Run the Storage test with pytest
result = subprocess.run(
    [sys.executable, '-m', 'pytest', 'tests/unit/test_storage.py', '-v'],
    capture_output=True,
    text=True,
    env=env
)

print("STDOUT:")
print(result.stdout)

if result.stderr:
    print("STDERR:")
    print(result.stderr)

print(f"Return code: {result.returncode}")

if result.returncode == 0:
    print("✅ Storage tests PASSED!")
else:
    print("❌ Storage tests FAILED!")