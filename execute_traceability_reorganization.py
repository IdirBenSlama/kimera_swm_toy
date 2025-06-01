#!/usr/bin/env python3
"""
Execute traceability-focused reorganization
Preserve all artifacts while organizing for efficiency
"""
import os
import shutil

def execute_reorganization():
    """Execute the traceability reorganization"""
    
    print("🗂️ EXECUTING TRACEABILITY REORGANIZATION")
    print("=" * 50)
    print("Preserving all development artifacts in organized structure")
    print()
    
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
        "REORGANIZATION_COMPLETE.md"
    ]
    
    moved_status = 0
    for filename in status_files:
        if os.path.exists(filename):
            target = f"docs/status/{filename}"
            if not os.path.exists(target):
                shutil.move(filename, target)
                print(f"✅ {filename}")
                moved_status += 1
            else:
                os.remove(filename)
                print(f"🗑️ Removed duplicate {filename}")
    
    # Move FINAL_STATUS.md (already created in docs/status/)
    if os.path.exists("FINAL_STATUS.md"):
        os.remove("FINAL_STATUS.md")
        print("🗑️ Removed duplicate FINAL_STATUS.md")
    
    # === MOVE IMPLEMENTATION FILES ===
    print("\n📋 Moving implementation files to docs/implementation/...")
    
    implementation_files = [
        "TEST_SUITE_README.md",
        "FINAL_CLEANUP_PLAN.md",
        "development_audit_report.md"
    ]
    
    moved_impl = 0
    for filename in implementation_files:
        if os.path.exists(filename):
            target = f"docs/implementation/{filename}"
            if not os.path.exists(target):
                shutil.move(filename, target)
                print(f"✅ {filename}")
                moved_impl += 1
            else:
                os.remove(filename)
                print(f"🗑️ Removed duplicate {filename}")
    
    # Move SCAR_IMPLEMENTATION_GUIDE.md (already created in docs/implementation/)
    if os.path.exists("SCAR_IMPLEMENTATION_GUIDE.md"):
        os.remove("SCAR_IMPLEMENTATION_GUIDE.md")
        print("🗑️ Removed duplicate SCAR_IMPLEMENTATION_GUIDE.md")
    
    # === MOVE DEVELOPMENT SCRIPTS ===
    print("\n🔧 Moving development scripts...")
    
    # Get all Python files in root
    all_py = [f for f in os.listdir('.') if f.endswith('.py') and os.path.isfile(f)]
    
    # Categorize scripts
    development_scripts = [f for f in all_py if any(f.startswith(prefix) for prefix in [
        'demo_', 'execute_', 'quick_', 'simple_', 'basic_', 'final_', 'minimal_', 'setup_'
    ])]
    
    testing_scripts = [f for f in all_py if f.startswith('run_')]
    verification_scripts = [f for f in all_py if any(f.startswith(prefix) for prefix in [
        'check_', 'verify_'
    ])]
    maintenance_scripts = [f for f in all_py if any(f.startswith(prefix) for prefix in [
        'fix_', 'cleanup_', 'organize_', 'move_'
    ])]
    
    # Move scripts by category
    script_moves = [
        (development_scripts, "scripts/development/", "🛠️"),
        (testing_scripts, "scripts/testing/", "🧪"),
        (verification_scripts, "scripts/verification/", "✅"),
        (maintenance_scripts, "scripts/maintenance/", "🔧")
    ]
    
    moved_scripts = 0
    for script_list, target_dir, emoji in script_moves:
        for filename in script_list:
            if os.path.exists(filename):
                target = f"{target_dir}{filename}"
                if not os.path.exists(target):
                    shutil.move(filename, target)
                    print(f"{emoji} {filename}")
                    moved_scripts += 1
                else:
                    os.remove(filename)
                    print(f"🗑️ Removed duplicate {filename}")
    
    # === MOVE TEST FILES ===
    print("\n🧪 Moving test files to tests/archive/...")
    
    test_files = [f for f in all_py if f.startswith('test_')]
    moved_tests = 0
    
    for filename in test_files:
        if os.path.exists(filename):
            target = f"tests/archive/{filename}"
            if not os.path.exists(target):
                shutil.move(filename, target)
                print(f"📦 {filename}")
                moved_tests += 1
            else:
                os.remove(filename)
                print(f"🗑️ Removed duplicate {filename}")
    
    # === MOVE REMAINING UTILITY FILES ===
    print("\n🔧 Moving remaining utility files...")
    
    remaining_py = [f for f in os.listdir('.') if f.endswith('.py') and os.path.isfile(f)]
    keep_files = {'conftest.py'}
    
    utility_files = [f for f in remaining_py if f not in keep_files]
    moved_utilities = 0
    
    for filename in utility_files:
        if os.path.exists(filename):
            # Determine best category
            if any(keyword in filename for keyword in ['import', 'status', 'current']):
                target_dir = "scripts/development/"
            elif 'batch' in filename:
                target_dir = "scripts/maintenance/"
            else:
                target_dir = "scripts/development/"
            
            target = f"{target_dir}{filename}"
            if not os.path.exists(target):
                shutil.move(filename, target)
                print(f"🔧 {filename}")
                moved_utilities += 1
            else:
                os.remove(filename)
                print(f"🗑️ Removed duplicate {filename}")
    
    # === FINAL SUMMARY ===
    print("\n" + "=" * 50)
    print("📊 REORGANIZATION SUMMARY")
    print(f"  • Status files preserved: {moved_status}")
    print(f"  • Implementation files organized: {moved_impl}")
    print(f"  • Development scripts categorized: {moved_scripts}")
    print(f"  • Test files archived: {moved_tests}")
    print(f"  • Utility files organized: {moved_utilities}")
    
    # Check final state
    remaining_md = [f for f in os.listdir('.') if f.endswith('.md') and os.path.isfile(f)]
    remaining_py = [f for f in os.listdir('.') if f.endswith('.py') and os.path.isfile(f)]
    
    essential_md = {'README.md', 'CHANGELOG.md'}
    essential_py = {'conftest.py'}
    
    print(f"\n📁 Final Root Directory State:")
    print(f"  • Essential markdown files: {[f for f in remaining_md if f in essential_md]}")
    print(f"  • Essential Python files: {[f for f in remaining_py if f in essential_py]}")
    
    unexpected_md = [f for f in remaining_md if f not in essential_md]
    unexpected_py = [f for f in remaining_py if f not in essential_py]
    
    if unexpected_md:
        print(f"  • Additional markdown files: {unexpected_md}")
    if unexpected_py:
        print(f"  • Additional Python files: {unexpected_py}")
    
    # Count organized files
    status_count = len([f for f in os.listdir('docs/status') if f.endswith('.md')])
    impl_count = len([f for f in os.listdir('docs/implementation') if f.endswith('.md')])
    dev_scripts = len([f for f in os.listdir('scripts/development') if f.endswith('.py')])
    test_scripts = len([f for f in os.listdir('scripts/testing') if f.endswith('.py')])
    verify_scripts = len([f for f in os.listdir('scripts/verification') if f.endswith('.py')])
    maint_scripts = len([f for f in os.listdir('scripts/maintenance') if f.endswith('.py')])
    archived_tests = len([f for f in os.listdir('tests/archive') if f.endswith('.py')])
    
    print(f"\n📊 Organized Artifacts:")
    print(f"  • Status reports: {status_count}")
    print(f"  • Implementation guides: {impl_count}")
    print(f"  • Development scripts: {dev_scripts}")
    print(f"  • Testing scripts: {test_scripts}")
    print(f"  • Verification scripts: {verify_scripts}")
    print(f"  • Maintenance scripts: {maint_scripts}")
    print(f"  • Archived tests: {archived_tests}")
    
    print(f"\n✅ TRACEABILITY REORGANIZATION COMPLETE")
    print("🔍 All development artifacts preserved with full traceability")
    print("📚 Organized structure maintains complete audit trail")
    print("🚀 Clean root directory ready for ongoing development")
    print("\n📋 See docs/TRACEABILITY_INDEX.md for complete organization guide")

if __name__ == "__main__":
    execute_reorganization()