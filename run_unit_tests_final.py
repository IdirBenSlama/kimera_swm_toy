#!/usr/bin/env python3
import subprocess
import sys
import os

print("Running original unit tests to verify fixes...")

# Set up environment
env = os.environ.copy()
env['PYTHONPATH'] = 'src'

# Test individual unit test files
test_files = [
    'tests/unit/test_echoform_core.py',
    'tests/unit/test_identity.py'
]

for test_file in test_files:
    if os.path.exists(test_file):
        print(f"\n🧪 Running {test_file}...")
        result = subprocess.run(
            [sys.executable, '-m', 'pytest', test_file, '-v'],
            capture_output=True,
            text=True,
            env=env
        )
        
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
            
        if result.returncode == 0:
            print(f"✅ {test_file} PASSED")
        else:
            print(f"❌ {test_file} FAILED")
    else:
        print(f"⚠️  {test_file} not found")

print("\n🏁 Unit test run complete!")