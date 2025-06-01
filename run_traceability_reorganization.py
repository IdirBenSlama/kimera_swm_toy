#!/usr/bin/env python3
"""
Execute the complete traceability reorganization
"""
import os
import shutil

def main():
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
                print(f"🔄 {filename} already in docs/status/")
    
    # Handle FINAL_STATUS.md (check if duplicate exists)
    if os.path.exists("FINAL_STATUS.md") and os.path.exists("docs/status/FINAL_STATUS.md"):
        os.remove("FINAL_STATUS.md")
        print("🗑️ Removed duplicate FINAL_STATUS.md")
    elif os.path.exists("FINAL_STATUS.md"):
        shutil.move("FINAL_STATUS.md", "docs/status/FINAL_STATUS.md")
        print("✅ FINAL_STATUS.md")
        moved_status += 1
    
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
                print(f"🔄 {filename} already in docs/implementation/")
    
    # Handle SCAR_IMPLEMENTATION_GUIDE.md
    if os.path.exists("SCAR_IMPLEMENTATION_GUIDE.md") and os.path.exists("docs/implementation/SCAR_IMPLEMENTATION_GUIDE.md"):
        os.remove("SCAR_IMPLEMENTATION_GUIDE.md")
        print("🗑️ Removed duplicate SCAR_IMPLEMENTATION_GUIDE.md")
    elif os.path.exists("SCAR_IMPLEMENTATION_GUIDE.md"):
        shutil.move("SCAR_IMPLEMENTATION_GUIDE.md", "docs/implementation/SCAR_IMPLEMENTATION_GUIDE.md")
        print("✅ SCAR_IMPLEMENTATION_GUIDE.md")
        moved_impl += 1
    
    # === MOVE DEVELOPMENT SCRIPTS ===
    print("\n🔧 Moving development scripts...")
    
    # Get all Python files in root
    all_py = [f for f in os.listdir('.') if f.endswith('.py') and os.path.isfile(f)]
    
    # Categorize scripts
    development_scripts = []
    testing_scripts = []
    verification_scripts = []
    maintenance_scripts = []
    
    for f in all_py:
        if any(f.startswith(prefix) for prefix in [
            'demo_', 'execute_', 'quick_', 'simple_', 'basic_', 'final_', 'minimal_', 'setup_', 'scar_demo'
        ]):
            development_scripts.append(f)
        elif f.startswith('run_'):
            testing_scripts.append(f)
        elif any(f.startswith(prefix) for prefix in ['check_', 'verify_']):
            verification_scripts.append(f)
        elif any(f.startswith(prefix) for prefix in ['fix_', 'cleanup_', 'organize_', 'move_', 'batch_']):
            maintenance_scripts.append(f)
        elif any(keyword in f for keyword in ['import', 'status', 'current', 'project']):
            development_scripts.append(f)
        else:
            # Default to development for uncategorized scripts
            development_scripts.append(f)
    
    # Move scripts by category
    script_moves = [
        (development_scripts, "scripts/development/", "🛠️"),
        (testing_scripts, "scripts/testing/", "🧪"),
        (verification_scripts, "scripts/verification/", "✅"),
        (maintenance_scripts, "scripts/maintenance/", "🔧")
    ]
    
    moved_scripts = 0
    for script_list, target_dir, emoji in script_moves:
        if script_list:
            print(f"\n{emoji} Moving to {target_dir}:")
            for filename in script_list:
                if os.path.exists(filename):
                    target = f"{target_dir}{filename}"
                    if not os.path.exists(target):
                        shutil.move(filename, target)
                        print(f"  ✅ {filename}")
                        moved_scripts += 1
                    else:
                        print(f"  🔄 {filename} already exists")
    
    # === MOVE TEST FILES ===
    print("\n🧪 Moving test files to tests/archive/...")
    
    test_files = [f for f in os.listdir('.') if f.startswith('test_') and f.endswith('.py') and os.path.isfile(f)]
    moved_tests = 0
    
    for filename in test_files:
        if os.path.exists(filename):
            target = f"tests/archive/{filename}"
            if not os.path.exists(target):
                shutil.move(filename, target)
                print(f"📦 {filename}")
                moved_tests += 1
            else:
                print(f"🔄 {filename} already in tests/archive/")
    
    # === CLEAN UP DUPLICATES ===
    print("\n🧹 Cleaning up duplicates...")
    
    # Remove duplicate docs files in root
    docs_duplicates = [
        "docs/SCAR_IMPLEMENTATION_GUIDE.md",  # We have it in docs/implementation/
        "docs/TEST_SUITE_README.md"  # We have it in docs/implementation/
    ]
    
    for dup_file in docs_duplicates:
        if os.path.exists(dup_file):
            os.remove(dup_file)
            print(f"🗑️ Removed duplicate {dup_file}")
    
    # === FINAL SUMMARY ===
    print("\n" + "=" * 50)
    print("📊 REORGANIZATION SUMMARY")
    print(f"  • Status files moved: {moved_status}")
    print(f"  • Implementation files moved: {moved_impl}")
    print(f"  • Development scripts moved: {moved_scripts}")
    print(f"  • Test files archived: {moved_tests}")
    
    # Check final state
    remaining_md = [f for f in os.listdir('.') if f.endswith('.md') and os.path.isfile(f)]
    remaining_py = [f for f in os.listdir('.') if f.endswith('.py') and os.path.isfile(f)]
    
    print(f"\n📁 Final Root Directory State:")
    print(f"  • Remaining markdown files: {remaining_md}")
    print(f"  • Remaining Python files: {remaining_py}")
    
    # Count organized files
    try:
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
    except FileNotFoundError as e:
        print(f"Note: Some directories may not exist yet: {e}")
    
    print(f"\n✅ TRACEABILITY REORGANIZATION COMPLETE")
    print("🔍 All development artifacts preserved with full traceability")
    print("📚 Organized structure maintains complete audit trail")
    print("🚀 Clean root directory ready for ongoing development")
    print("\n📋 See docs/TRACEABILITY_INDEX.md for complete organization guide")

if __name__ == "__main__":
    main()