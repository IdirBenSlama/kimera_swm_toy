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

def cleanup_workflows():
    """Remove duplicate workflow files"""
    removed_count = 0
    
    print("🧹 Cleaning up duplicate workflow files...")
    
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"✅ Removed {file_path}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Error removing {file_path}: {e}")
        else:
            print(f"⚠️  File not found: {file_path}")
    
    # Check for any other ci_*.yml files
    workflow_dir = ".github/workflows"
    if os.path.exists(workflow_dir):
        ci_files = glob.glob(f"{workflow_dir}/ci_*.yml")
        for ci_file in ci_files:
            if ci_file != f"{workflow_dir}/ci.yml":
                print(f"⚠️  Found additional CI file: {ci_file}")
    
    print(f"\n🎯 Cleanup complete! Removed {removed_count} files")
    print("✅ Only .github/workflows/ci.yml should remain")

if __name__ == "__main__":
    cleanup_workflows()