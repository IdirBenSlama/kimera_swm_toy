#!/usr/bin/env python3
"""
Final comprehensive cleanup of root directory
"""
import os
import shutil

def final_root_cleanup():
    """Clean up all remaining clutter from root directory"""
    
    print("🧹 FINAL ROOT DIRECTORY CLEANUP")
    print("=" * 50)
    
    # === MARKDOWN FILES ===
    print("\n📄 Cleaning up markdown files...")
    
    # Get all markdown files
    all_md = [f for f in os.listdir('.') if f.endswith('.md') and os.path.isfile(f)]
    
    # Files to keep in root
    keep_md = {'README.md', 'CHANGELOG.md', 'LICENSE.md'}
    
    # Files to move to docs/
    docs_md = {'SCAR_IMPLEMENTATION_GUIDE.md', 'TEST_SUITE_README.md'}
    
    # Everything else to archive
    archive_md = [f for f in all_md if f not in keep_md and f not in docs_md]
    
    # Ensure directories exist
    os.makedirs("docs", exist_ok=True)
    os.makedirs("docs/ARCHIVE", exist_ok=True)
    
    # Move markdown files
    md_moved = 0
    for filename in archive_md:
        if os.path.exists(filename):
            target = f"docs/ARCHIVE/{filename}"
            try:
                if not os.path.exists(target):
                    shutil.move(filename, target)
                    md_moved += 1
                else:
                    os.remove(filename)
                    md_moved += 1
            except Exception as e:
                print(f"❌ Error with {filename}: {e}")
    
    for filename in docs_md:
        if os.path.exists(filename):
            target = f"docs/{filename}"
            try:
                if not os.path.exists(target):
                    shutil.move(filename, target)
                else:
                    os.remove(filename)
            except Exception as e:
                print(f"❌ Error with {filename}: {e}")
    
    print(f"✅ Moved {md_moved} markdown files to archive")
    
    # === PYTHON FILES ===
    print("\n🐍 Cleaning up Python files...")
    
    # Get all Python files
    all_py = [f for f in os.listdir('.') if f.endswith('.py') and os.path.isfile(f)]
    
    # Files to keep in root (essential project files)
    keep_py = {
        'conftest.py',
        'pyproject.toml',  # Not .py but related
        'poetry.lock'      # Not .py but related
    }
    
    # Categorize files to move
    test_files = [f for f in all_py if f.startswith('test_')]
    script_files = [f for f in all_py if any(f.startswith(prefix) for prefix in [
        'run_', 'check_', 'fix_', 'verify_', 'validate_', 'setup_', 'demo_',
        'execute_', 'quick_', 'simple_', 'basic_', 'final_', 'minimal_'
    ])]
    
    # Move test files to tests/
    py_moved = 0
    for filename in test_files:
        if os.path.exists(filename):
            # Determine target directory based on test type
            if any(keyword in filename.lower() for keyword in ['integration', 'p0', 'scar', 'storage']):
                target_dir = "tests/integration"
            elif any(keyword in filename.lower() for keyword in ['unit', 'basic', 'simple']):
                target_dir = "tests/unit"
            else:
                target_dir = "tests/functional"
            
            os.makedirs(target_dir, exist_ok=True)
            target = f"{target_dir}/{filename}"
            
            try:
                if not os.path.exists(target):
                    shutil.move(filename, target)
                    py_moved += 1
                else:
                    os.remove(filename)
                    py_moved += 1
            except Exception as e:
                print(f"❌ Error with {filename}: {e}")
    
    # Move script files to scripts/
    for filename in script_files:
        if os.path.exists(filename):
            target = f"scripts/{filename}"
            try:
                if not os.path.exists(target):
                    shutil.move(filename, target)
                    py_moved += 1
                else:
                    os.remove(filename)
                    py_moved += 1
            except Exception as e:
                print(f"❌ Error with {filename}: {e}")
    
    print(f"✅ Moved {py_moved} Python files to appropriate directories")
    
    # === FINAL STATUS ===
    print("\n📊 Final Status:")
    
    # Check remaining files
    remaining_md = [f for f in os.listdir('.') if f.endswith('.md') and os.path.isfile(f)]
    remaining_py = [f for f in os.listdir('.') if f.endswith('.py') and os.path.isfile(f)]
    
    print(f"  • Markdown files in root: {len(remaining_md)} {remaining_md}")
    print(f"  • Python files in root: {len(remaining_py)}")
    
    # Count files in organized directories
    archive_count = len([f for f in os.listdir('docs/ARCHIVE') if f.endswith('.md')])
    docs_count = len([f for f in os.listdir('docs') if f.endswith('.md')])
    scripts_count = len([f for f in os.listdir('scripts') if f.endswith('.py')])
    
    print(f"  • Files in docs/ARCHIVE/: {archive_count}")
    print(f"  • Files in docs/: {docs_count}")
    print(f"  • Files in scripts/: {scripts_count}")
    
    # Check for unexpected files
    all_files = os.listdir('.')
    expected_files = {
        'README.md', 'CHANGELOG.md', 'pyproject.toml', 'poetry.lock', 'conftest.py'
    }
    expected_dirs = {
        'src', 'tests', 'docs', 'scripts', 'vault', 'data', 'examples', 
        'benchmarks', 'static', 'tools', '.github', '.vscode', '__pycache__',
        '_nocache_temp', 'test_vault'
    }
    
    unexpected_files = [f for f in all_files if os.path.isfile(f) and f not in expected_files and not f.startswith('.')]
    
    if unexpected_files:
        print(f"\n⚠️  Unexpected files still in root:")
        for f in unexpected_files[:10]:  # Show first 10
            print(f"    • {f}")
        if len(unexpected_files) > 10:
            print(f"    ... and {len(unexpected_files) - 10} more")
    else:
        print(f"\n✅ Root directory is clean!")
    
    print(f"\n🎯 Cleanup complete! Repository is now organized and maintainable.")

if __name__ == "__main__":
    final_root_cleanup()