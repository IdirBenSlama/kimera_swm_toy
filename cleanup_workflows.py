#!/usr/bin/env python3
"""Clean up duplicate workflow files"""
import os

files_to_remove = [
    ".github/workflows/ci_fixed.yml",
    ".github/workflows/ci_final.yml"
]

for file_path in files_to_remove:
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Removed {file_path}")
    else:
        print(f"File {file_path} does not exist")

print("Workflow cleanup complete!")