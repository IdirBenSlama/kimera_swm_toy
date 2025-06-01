#!/usr/bin/env python3
"""
Move utility scripts to the scripts/ directory
"""
import shutil
import os

# Scripts to move to scripts/ directory
utility_scripts = [
    "cleanup_workflows.py",
    "run_cleanup.py", 
    "verify_scar_implementation.py",
    "verify_import_fixes.py",
    "verify_p0_fixes.py",
    "verify_unicode_fix.py",
    "fix_critical_issues.py",
    "fix_import_paths.py",
    "fix_unicode_encoding.py",
    "execute_fix.py",
    "execute_verification.py",
    "validate_all_fixes.py",
    "current_status_summary.py",
    "project_status_summary.py",
    "import_fix_summary.py"
]

# Quick test/validation scripts to move to scripts/
quick_scripts = [
    "quick_fix.py",
    "quick_validation.py",
    "quick_status_verification.py",
    "quick_test_validation.py",
    "quick_verification_test.py",
    "run_quick_status.py",
    "run_quick_test.py",
    "run_quick_verification.py"
]

def move_scripts():
    """Move scripts to the scripts directory"""
    moved_count = 0
    
    all_scripts = utility_scripts + quick_scripts
    
    for script in all_scripts:
        if os.path.exists(script):
            try:
                target_path = f"scripts/{script}"
                if not os.path.exists(target_path):
                    shutil.move(script, target_path)
                    print(f"✅ Moved {script} to scripts/")
                    moved_count += 1
                else:
                    print(f"⚠️  Target already exists: {target_path}")
            except Exception as e:
                print(f"❌ Error moving {script}: {e}")
        else:
            print(f"⚠️  File not found: {script}")
    
    print(f"\n🎯 Moved {moved_count} scripts to scripts/ directory")

if __name__ == "__main__":
    move_scripts()