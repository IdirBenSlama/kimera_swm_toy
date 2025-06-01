#!/usr/bin/env python3
import subprocess
import sys

print("🚀 Executing final comprehensive test run...")
result = subprocess.run([sys.executable, "final_test_run.py"], capture_output=True, text=True)

print("STDOUT:")
print(result.stdout)

if result.stderr:
    print("STDERR:")
    print(result.stderr)

print(f"Return code: {result.returncode}")

if result.returncode == 0:
    print("\n🎉 SUCCESS: All API compatibility fixes are working!")
    print("✅ The original unit tests now pass without any modifications!")
else:
    print("\n⚠️  Some tests may still need attention - check output above.")