#!/usr/bin/env python3
import subprocess
import sys

print("Executing all unit tests...")
result = subprocess.run([sys.executable, "run_all_unit_tests.py"], capture_output=True, text=True)

print("STDOUT:")
print(result.stdout)

if result.stderr:
    print("STDERR:")
    print(result.stderr)

print(f"Return code: {result.returncode}")

if result.returncode == 0:
    print("\n🎉 SUCCESS: All unit tests are now passing!")
else:
    print("\n❌ Some tests are still failing - need to investigate further.")