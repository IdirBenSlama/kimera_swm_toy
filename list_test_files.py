#!/usr/bin/env python3
import os

# Find all test files in current directory
test_files = [f for f in os.listdir('.') if f.startswith('test_') and f.endswith('.py')]
print("Test files in root directory:")
for f in sorted(test_files):
    print(f"  {f}")

print(f"\nTotal: {len(test_files)} test files")