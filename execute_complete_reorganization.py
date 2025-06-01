#!/usr/bin/env python3
"""
Execute complete traceability reorganization
Move all files to their proper organized locations
"""
import os
import shutil
import glob

def execute_complete_reorganization():
    """Execute the complete reorganization"""
    
    print("🗂️ EXECUTING COMPLETE TRACEABILITY REORGANIZATION")
    print("=" * 60)
    print("Preserving all development artifacts in organized structure")
    print()
    
    moved_counts = {
        'status': 0,
        'implementation': 0,
        'development': 0,
        'testing': 0,
        'verification': 0,
        'maintenance': 0,
        'tests': 0
    }
    
    # === MOVE STATUS FILES ===
    print("📊 Moving status files to docs/status/...")
    
    status_files = [
        "IMPLEMENTATION_COMPLETE_SUMMARY.md",
        "IMPORT_FIXES_COMPLETE.md", 
        "ISSUES_RESOLVED_SUMMARY.md",
        "KIMERA_SWM_READY.md",
        "P0_STATUS_SUMMARY.md",
        "SCAR_FIXES_SUMMARY.md",
        "TEST_SUITE_IMPLEMENTATION_SUMMARY.md",
        "UNICODE_ENCODING_FIX_SUMMARY.md",
        "UNICODE_FIX_COMPLETE.md",
        "VERIFICATION_READY.md",
        "REORGANIZATION_COMPLETE.md",
        "FINAL_STATUS.md"
    ]
    
    for filename in status_files:
        if os.path.exists(filename):
            target = f"docs/status/{filename}"
            if not os.path.exists(target):
                shutil.move(filename, target)
                print(f"✅ {filename}")
                moved_counts['status'] += 1
    
    # === MOVE IMPLEMENTATION FILES ===
    print("\n📋 Moving implementation files to docs/implementation/...")
    
    implementation_files = [
        "TEST_SUITE_README.md",
        "FINAL_CLEANUP_PLAN.md",
        "development_audit_report.md",
        "SCAR_IMPLEMENTATION_GUIDE.md"
    ]
    
    for filename in implementation_files:
        if os.path.exists(filename):
            target = f"docs/implementation/{filename}"
            if not os.path.exists(target):
                shutil.move(filename, target)
                print(f"✅ {filename}")
                moved_counts['implementation'] += 1
    
    # === MOVE PYTHON SCRIPTS BY CATEGORY ===
    print("\n🔧 Moving Python scripts by category...")
    
    # Get all Python files in root
    all_py = [f for f in os.listdir('.') if f.endswith('.py') and os.path.isfile(f)]
    
    # Development scripts
    development_patterns = [
        'demo_*', 'execute_*', 'quick_*', 'simple_*', 'basic_*', 
        'final_*', 'minimal_*', 'setup_*', 'scar_demo*',
        'current_status*', 'project_status*', 'import_fix*'
    ]
    
    development_scripts = []
    for pattern in development_patterns:
        development_scripts.extend(glob.glob(pattern))
    
    # Testing scripts
    testing_scripts = [f for f in all_py if f.startswith('run_')]
    
    # Verification scripts  
    verification_scripts = []
    verification_patterns = ['check_*', 'verify_*', 'validate_*']
    for pattern in verification_patterns:
        verification_scripts.extend(glob.glob(pattern))
    
    # Maintenance scripts
    maintenance_scripts = []
    maintenance_patterns = ['fix_*', 'cleanup_*', 'organize_*', 'move_*', 'batch_*']
    for pattern in maintenance_patterns:
        maintenance_scripts.extend(glob.glob(pattern))
    
    # Move scripts by category
    script_categories = [
        (development_scripts, "scripts/development/", "🛠️", 'development'),
        (testing_scripts, "scripts/testing/", "🧪", 'testing'),
        (verification_scripts, "scripts/verification/", "✅", 'verification'),
        (maintenance_scripts, "scripts/maintenance/", "🔧", 'maintenance')
    ]
    
    for script_list, target_dir, emoji, category in script_categories:
        if script_list:
            print(f"\n{emoji} Moving to {target_dir}:")
            for filename in script_list:
                if os.path.exists(filename):
                    target = f"{target_dir}{filename}"
                    if not os.path.exists(target):
                        shutil.move(filename, target)
                        print(f"  ✅ {filename}")
                        moved_counts[category] += 1
    
    # === MOVE TEST FILES ===
    print("\n🧪 Moving test files to tests/archive/...")
    
    test_files = [f for f in os.listdir('.') if f.startswith('test_') and f.endswith('.py')]
    
    for filename in test_files:
        if os.path.exists(filename):
            target = f"tests/archive/{filename}"
            if not os.path.exists(target):
                shutil.move(filename, target)
                print(f"📦 {filename}")
                moved_counts['tests'] += 1
    
    # === CLEAN UP REMAINING SCRIPTS ===
    print("\n🧹 Moving remaining utility scripts...")
    
    remaining_py = [f for f in os.listdir('.') if f.endswith('.py') and os.path.isfile(f)]
    keep_files = {'conftest.py', 'run_traceability_reorganization.py', 'execute_complete_reorganization.py'}
    
    for filename in remaining_py:
        if filename not in keep_files:
            # Categorize remaining files
            if any(keyword in filename for keyword in ['test', 'validation', 'check']):
                target_dir = "scripts/verification/"
            elif any(keyword in filename for keyword in ['run', 'execute']):
                target_dir = "scripts/testing/"
            else:
                target_dir = "scripts/development/"
            
            target = f"{target_dir}{filename}"
            if not os.path.exists(target):
                shutil.move(filename, target)
                print(f"🔧 {filename} → {target_dir}")
                moved_counts['development'] += 1
    
    # === FINAL SUMMARY ===
    print("\n" + "=" * 60)
    print("📊 REORGANIZATION SUMMARY")
    print(f"  • Status files moved: {moved_counts['status']}")
    print(f"  • Implementation files moved: {moved_counts['implementation']}")
    print(f"  • Development scripts moved: {moved_counts['development']}")
    print(f"  • Testing scripts moved: {moved_counts['testing']}")
    print(f"  • Verification scripts moved: {moved_counts['verification']}")
    print(f"  • Maintenance scripts moved: {moved_counts['maintenance']}")
    print(f"  • Test files archived: {moved_counts['tests']}")
    
    total_moved = sum(moved_counts.values())
    print(f"\n📈 Total files organized: {total_moved}")
    
    # Check final state
    remaining_md = [f for f in os.listdir('.') if f.endswith('.md') and os.path.isfile(f)]
    remaining_py = [f for f in os.listdir('.') if f.endswith('.py') and os.path.isfile(f)]
    
    print(f"\n📁 Final Root Directory State:")
    print(f"  • Remaining markdown files: {len(remaining_md)}")
    print(f"  • Remaining Python files: {len(remaining_py)}")
    
    if remaining_md:
        print(f"    MD files: {remaining_md}")
    if remaining_py:
        print(f"    PY files: {remaining_py}")
    
    # Count organized files
    try:
        status_count = len([f for f in os.listdir('docs/status') if f.endswith('.md')])
        impl_count = len([f for f in os.listdir('docs/implementation') if f.endswith('.md')])
        dev_scripts = len([f for f in os.listdir('scripts/development') if f.endswith('.py')])
        test_scripts = len([f for f in os.listdir('scripts/testing') if f.endswith('.py')])
        verify_scripts = len([f for f in os.listdir('scripts/verification') if f.endswith('.py')])
        maint_scripts = len([f for f in os.listdir('scripts/maintenance') if f.endswith('.py')])
        archived_tests = len([f for f in os.listdir('tests/archive') if f.endswith('.py')])
        
        print(f"\n📊 Final Organized Structure:")
        print(f"  • Status reports: {status_count}")
        print(f"  • Implementation guides: {impl_count}")
        print(f"  • Development scripts: {dev_scripts}")
        print(f"  • Testing scripts: {test_scripts}")
        print(f"  • Verification scripts: {verify_scripts}")
        print(f"  • Maintenance scripts: {maint_scripts}")
        print(f"  • Archived tests: {archived_tests}")
        
        total_organized = status_count + impl_count + dev_scripts + test_scripts + verify_scripts + maint_scripts + archived_tests
        print(f"\n📈 Total organized artifacts: {total_organized}")
        
    except FileNotFoundError as e:
        print(f"Note: Some directories may not exist yet: {e}")
    
    print(f"\n✅ TRACEABILITY REORGANIZATION COMPLETE")
    print("🔍 All development artifacts preserved with full traceability")
    print("📚 Organized structure maintains complete audit trail")
    print("🚀 Clean root directory ready for ongoing development")
    print("\n📋 See docs/TRACEABILITY_INDEX.md for complete organization guide")
    
    return total_moved

if __name__ == "__main__":
    execute_complete_reorganization()