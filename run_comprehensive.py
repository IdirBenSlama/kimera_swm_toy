#!/usr/bin/env python3
import subprocess
import sys

print("Running comprehensive compatibility test...")
result = subprocess.run([sys.executable, "comprehensive_test.py"], capture_output=True, text=True)

print("STDOUT:")
print(result.stdout)

if result.stderr:
    print("\nSTDERR:")
    print(result.stderr)

print(f"\nReturn code: {result.returncode}")

if result.returncode == 0:
    print("\n🎉 SUCCESS: All compatibility fixes are working!")
else:
    print("\n❌ FAILURE: Some issues remain to be fixed.")