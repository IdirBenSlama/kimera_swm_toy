#!/usr/bin/env python3
"""Clean up duplicate workflow files and phantom references"""
import os
import glob

# Files that might exist and should be removed
files_to_remove = [
    ".github/workflows/ci_fixed.yml",
    ".github/workflows/ci_final.yml", 
    ".github/workflows/ci_new.yml",
    ".github/workflows/ci_clean.yml",
    ".github/workflows/ci_backup.yml"
]

print("Checking for workflow files to remove...")
removed_count = 0

for file_path in files_to_remove:
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"✅ Removed {file_path}")
            removed_count += 1
        except Exception as e:
            print(f"❌ Failed to remove {file_path}: {e}")
    else:
        print(f"ℹ️  File {file_path} does not exist")

# Also check for any other ci_*.yml files that might exist
workflow_dir = ".github/workflows"
if os.path.exists(workflow_dir):
    ci_files = glob.glob(os.path.join(workflow_dir, "ci_*.yml"))
    for ci_file in ci_files:
        if ci_file != ".github/workflows/ci.yml":  # Keep the main ci.yml
            try:
                os.remove(ci_file)
                print(f"✅ Removed extra CI file: {ci_file}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Failed to remove {ci_file}: {e}")

print(f"\n🎯 Workflow cleanup complete! Removed {removed_count} files.")
print("Only .github/workflows/ci.yml should remain.")

if __name__ == "__main__":
    # Also check current directory for any stray CI files
    current_ci_files = glob.glob("ci_*.yml")
    for ci_file in current_ci_files:
        try:
            os.remove(ci_file)
            print(f"✅ Removed stray CI file: {ci_file}")
            removed_count += 1
        except Exception as e:
            print(f"❌ Failed to remove {ci_file}: {e}")
    
    print(f"\nFinal cleanup count: {removed_count} files removed")