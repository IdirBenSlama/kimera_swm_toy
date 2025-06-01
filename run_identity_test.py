#!/usr/bin/env python3
import subprocess
import sys
import os

# Set up environment
env = os.environ.copy()
env['PYTHONPATH'] = 'src'

print("🧪 Running Identity unit tests...")

# Run the Identity test directly
result = subprocess.run(
    [sys.executable, 'tests/unit/test_identity.py'],
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
    print("✅ Identity tests PASSED!")
else:
    print("❌ Identity tests FAILED!")