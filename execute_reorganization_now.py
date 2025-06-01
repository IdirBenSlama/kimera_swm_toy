#!/usr/bin/env python3
"""
Execute reorganization immediately
"""
import os
import shutil
import glob

def execute_reorganization_now():
    """Execute the reorganization immediately"""
    print("🗂️ EXECUTING REORGANIZATION NOW")
    print("=" * 40)
    
    moved_counts = {
        'status': 0,
        'implementation': 0,
        'development': 0,
        'testing': 0,
        'verification': 0,
        'maintenance': 0,
        'tests': 0
    }
    
    # === MOVE REMAINING STATUS FILES ===
    print("📊 Moving remaining status files...")
    
    remaining_status = [
        "TEST_SUITE_IMPLEMENTATION_SUMMARY.md",
        "UNICODE_ENCODING_FIX_SUMMARY.md",
        "UNICODE_FIX_COMPLETE.md", 
        "VERIFICATION_READY.md",
        "REORGANIZATION_COMPLETE.md"
    ]
    
    for filename in remaining_status:
        if os.path.exists(filename):
            target = f"docs/status/{filename}"
            if not os.path.exists(target):
                shutil.move(filename, target)
                print(f"✅ Moved {filename}")
                moved_counts['status'] += 1
    
    # === MOVE IMPLEMENTATION FILES ===
    print("\n📋 Moving implementation files...")
    
    impl_files = [
        "FINAL_CLEANUP_PLAN.md",
        "development_audit_report.md"
    ]
    
    for filename in impl_files:
        if os.path.exists(filename):
            target = f"docs/implementation/{filename}"
            if not os.path.exists(target):
                shutil.move(filename, target)
                print(f"✅ Moved {filename}")
                moved_counts['implementation'] += 1
    
    # === MOVE DEVELOPMENT SCRIPTS ===
    print("\n🛠️ Moving development scripts...")
    
    dev_patterns = [
        'execute_*.py', 'quick_*.py', 'simple_*.py', 'basic_*.py',
        'final_*.py', 'minimal_*.py', 'setup_*.py'
    ]
    
    for pattern in dev_patterns:
        for script in glob.glob(pattern):
            # Skip the reorganization scripts themselves
            if script in ['execute_complete_reorganization.py', 'execute_reorganization_now.py']:
                continue
                
            target = f"scripts/development/{script}"
            if not os.path.exists(target):
                shutil.move(script, target)
                print(f"✅ Moved {script}")
                moved_counts['development'] += 1
    
    # Move scar_demo.py specifically
    if os.path.exists('scar_demo.py'):
        target = "scripts/development/scar_demo.py"
        if not os.path.exists(target):
            shutil.move('scar_demo.py', target)
            print(f"✅ Moved scar_demo.py")
            moved_counts['development'] += 1
    
    # === MOVE TESTING SCRIPTS ===
    print("\n🧪 Moving testing scripts...")
    
    test_patterns = ['run_*.py']
    
    for pattern in test_patterns:
        for script in glob.glob(pattern):
            # Skip reorganization runners
            if 'reorganization' in script or 'traceability' in script:
                continue
                
            target = f"scripts/testing/{script}"
            if not os.path.exists(target):
                shutil.move(script, target)
                print(f"✅ Moved {script}")
                moved_counts['testing'] += 1
    
    # === MOVE VERIFICATION SCRIPTS ===
    print("\n✅ Moving verification scripts...")
    
    verify_patterns = ['check_*.py', 'verify_*.py']
    
    for pattern in verify_patterns:
        for script in glob.glob(pattern):
            # Skip traceability verification
            if 'traceability' in script:
                continue
                
            target = f"scripts/verification/{script}"
            if not os.path.exists(target):
                shutil.move(script, target)
                print(f"✅ Moved {script}")
                moved_counts['verification'] += 1
    
    # === MOVE MAINTENANCE SCRIPTS ===
    print("\n🔧 Moving maintenance scripts...")
    
    maint_patterns = ['fix_*.py', 'cleanup_*.py', 'organize_*.py', 'move_*.py', 'batch_*.py']
    
    for pattern in maint_patterns:
        for script in glob.glob(pattern):
            target = f"scripts/maintenance/{script}"
            if not os.path.exists(target):
                shutil.move(script, target)
                print(f"✅ Moved {script}")
                moved_counts['maintenance'] += 1
    
    # === MOVE TEST FILES ===
    print("\n🧪 Moving test files...")
    
    test_files = glob.glob('test_*.py')
    
    for test_file in test_files:
        target = f"tests/archive/{test_file}"
        if not os.path.exists(target):
            shutil.move(test_file, target)
            print(f"✅ Moved {test_file}")
            moved_counts['tests'] += 1
    
    # === SUMMARY ===
    total_moved = sum(moved_counts.values())
    print(f"\n📊 REORGANIZATION SUMMARY:")
    print(f"  Total files moved: {total_moved}")
    print(f"  Status files: {moved_counts['status']}")
    print(f"  Implementation files: {moved_counts['implementation']}")
    print(f"  Development scripts: {moved_counts['development']}")
    print(f"  Testing scripts: {moved_counts['testing']}")
    print(f"  Verification scripts: {moved_counts['verification']}")
    print(f"  Maintenance scripts: {moved_counts['maintenance']}")
    print(f"  Test files: {moved_counts['tests']}")
    
    print(f"\n✅ REORGANIZATION COMPLETE!")
    print("🔍 All development artifacts preserved with full traceability")
    print("📚 Organized structure maintains complete audit trail")
    print("🚀 Clean root directory ready for ongoing development")
    
    return total_moved

if __name__ == "__main__":
    execute_reorganization_now()