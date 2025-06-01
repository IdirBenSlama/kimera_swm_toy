#!/usr/bin/env python3
"""
Quick check of current repository state
"""
import os

def check_structure():
    """Check the current directory structure"""
    print("📁 Current repository structure:")
    print("=" * 40)
    
    # Check key directories
    dirs_to_check = [
        "src/kimera",
        "tests/unit", 
        "tests/integration",
        "tests/functional",
        "docs",
        "docs/ARCHIVE",
        "scripts"
    ]
    
    for dir_path in dirs_to_check:
        if os.path.exists(dir_path):
            files = [f for f in os.listdir(dir_path) if not f.startswith('.') and not f.startswith('__')]
            print(f"✅ {dir_path} ({len(files)} items)")
        else:
            print(f"❌ {dir_path} (missing)")
    
    # Check root directory cleanliness
    print("\n📄 Root directory files:")
    root_files = [f for f in os.listdir('.') if os.path.isfile(f) and not f.startswith('.')]
    
    # Categorize files
    important_files = ['README.md', 'pyproject.toml', 'poetry.lock', 'CHANGELOG.md']
    test_files = [f for f in root_files if f.startswith('test_')]
    run_files = [f for f in root_files if f.startswith('run_')]
    status_files = [f for f in root_files if any(x in f.upper() for x in ['STATUS', 'SUMMARY', 'COMPLETE', 'FIXES'])]
    
    print(f"  Important: {len([f for f in root_files if f in important_files])}")
    print(f"  Test files: {len(test_files)}")
    print(f"  Run scripts: {len(run_files)}")
    print(f"  Status files: {len(status_files)}")
    print(f"  Total files: {len(root_files)}")
    
    if test_files:
        print(f"  ⚠️  Test files still in root: {test_files[:5]}{'...' if len(test_files) > 5 else ''}")
    
    if run_files:
        print(f"  ⚠️  Run scripts still in root: {run_files[:5]}{'...' if len(run_files) > 5 else ''}")
    
    if status_files:
        print(f"  ⚠️  Status files still in root: {status_files[:5]}{'...' if len(status_files) > 5 else ''}")

if __name__ == "__main__":
    check_structure()