#!/usr/bin/env python3
"""
Comprehensive repository reorganization script
"""
import os
import shutil
import glob

def cleanup_root_directory():
    """Remove files that have been moved to other locations"""
    
    # Files that should be removed from root (moved to docs/ARCHIVE/)
    files_to_remove = [
        "FINAL_STATUS.md",
        "P0_STATUS_SUMMARY.md", 
        "IMPLEMENTATION_COMPLETE_SUMMARY.md",
        "IMPORT_FIXES_COMPLETE.md",
        "ISSUES_RESOLVED_SUMMARY.md",
        "SCAR_IMPLEMENTATION_GUIDE.md",  # moved to docs/
        "TEST_SUITE_README.md",  # moved to docs/
        
        # Test files that should be in tests/ subdirectories
        "test_basic_quick.py",
        "test_config.py",
        "test_import_fixes.py",
        "test_p0_integration.py",
        "test_quick_run.py",
        "test_scar_functionality.py",
        "test_scar_quick.py",
        "test_storage_fix.py",
        "test_suite.py",
        "test_suite_demo.py",
        "test_system_quick.py",
        "test_unicode_fix.py",
        "test_unified_identity.py",
        "test_v073_storage.py",
        "test_vault_and_scar.py",
        "test_verification_runner.py",
        
        # Utility scripts that should be in scripts/
        "cleanup_workflows.py",
        "verify_scar_implementation.py",
        "run_cleanup.py",
        "quick_fix.py",
        "quick_validation.py",
        "execute_fix.py",
        "execute_verification.py",
        
        # Temporary/development files
        "move_status_files.py",
        "organize_scripts.py",
        "find_md_files.py",
        "list_test_files.py",
        "organize_scripts.py"
    ]
    
    removed_count = 0
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"✅ Removed {file_path}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Error removing {file_path}: {e}")
    
    print(f"🧹 Removed {removed_count} files from root directory")

def cleanup_test_files():
    """Remove test files from root that should be in tests/ subdirectories"""
    
    # Find all test_*.py files in root
    test_files = glob.glob("test_*.py")
    
    removed_count = 0
    for test_file in test_files:
        # Skip if it's already been moved or is a special case
        if os.path.exists(test_file):
            try:
                os.remove(test_file)
                print(f"✅ Removed test file {test_file}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Error removing {test_file}: {e}")
    
    print(f"🧪 Removed {removed_count} test files from root")

def cleanup_run_scripts():
    """Remove run_*.py scripts from root"""
    
    run_scripts = glob.glob("run_*.py")
    
    removed_count = 0
    for script in run_scripts:
        if os.path.exists(script):
            try:
                os.remove(script)
                print(f"✅ Removed run script {script}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Error removing {script}: {e}")
    
    print(f"🏃 Removed {removed_count} run scripts from root")

def cleanup_status_files():
    """Remove remaining status and summary files"""
    
    # Find all remaining .md files that look like status files
    md_files = glob.glob("*.md")
    status_patterns = [
        "*_STATUS*.md",
        "*_SUMMARY*.md", 
        "*_COMPLETE*.md",
        "*_FIXES*.md",
        "*_IMPLEMENTATION*.md",
        "PHASE_*.md",
        "FINAL_*.md",
        "ALL_GREEN*.md",
        "VERIFICATION_*.md",
        "UNICODE_*.md",
        "STABILIZATION_*.md"
    ]
    
    files_to_remove = []
    for pattern in status_patterns:
        files_to_remove.extend(glob.glob(pattern))
    
    # Remove duplicates and exclude README.md, CHANGELOG.md
    files_to_remove = list(set(files_to_remove))
    files_to_keep = ["README.md", "CHANGELOG.md"]
    files_to_remove = [f for f in files_to_remove if f not in files_to_keep]
    
    removed_count = 0
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"✅ Removed status file {file_path}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Error removing {file_path}: {e}")
    
    print(f"📋 Removed {removed_count} status files from root")

def cleanup_misc_files():
    """Remove miscellaneous development files"""
    
    misc_files = [
        "basic_import_test.py",
        "minimal_test.py",
        "simple_test.py",
        "scar_demo.py",
        "cache_demo.py",
        "demo_async.py",
        "demo_metrics.py",
        "demo_metrics_safe.py",
        "conftest.py",  # Should only be in tests/
        "check_*.py",
        "fix_*.py",
        "validate_*.py",
        "verify_*.py",
        "final_*.py",
        "simple_*.py",
        "quick_*.py"
    ]
    
    # Expand glob patterns
    all_files = []
    for pattern in misc_files:
        if "*" in pattern:
            all_files.extend(glob.glob(pattern))
        else:
            all_files.append(pattern)
    
    removed_count = 0
    for file_path in all_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"✅ Removed misc file {file_path}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Error removing {file_path}: {e}")
    
    print(f"🗂️  Removed {removed_count} miscellaneous files from root")

def show_final_structure():
    """Show the final directory structure"""
    print("\n📁 Final repository structure:")
    print("=" * 50)
    
    # Show key directories and files
    key_items = [
        "README.md",
        "pyproject.toml",
        "src/kimera/",
        "tests/unit/",
        "tests/integration/", 
        "tests/functional/",
        "docs/",
        "docs/ARCHIVE/",
        "scripts/",
        "vault/",
        ".github/workflows/ci.yml"
    ]
    
    for item in key_items:
        if os.path.exists(item):
            if os.path.isdir(item):
                file_count = len([f for f in os.listdir(item) if not f.startswith('.')])
                print(f"📁 {item} ({file_count} items)")
            else:
                print(f"📄 {item}")
        else:
            print(f"❌ {item} (missing)")

def main():
    """Run the complete repository reorganization"""
    print("🚀 Starting repository reorganization...")
    print("=" * 50)
    
    # Run cleanup steps
    cleanup_root_directory()
    print()
    
    cleanup_test_files()
    print()
    
    cleanup_run_scripts()
    print()
    
    cleanup_status_files()
    print()
    
    cleanup_misc_files()
    print()
    
    show_final_structure()
    
    print("\n" + "=" * 50)
    print("✅ Repository reorganization complete!")
    print("\n📋 Next steps:")
    print("1. Run: python -m pytest tests/ -v")
    print("2. Check: git status")
    print("3. Commit: git add . && git commit -m 'Reorganize repository structure'")

if __name__ == "__main__":
    main()