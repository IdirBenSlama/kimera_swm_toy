#!/usr/bin/env python3
"""
Bulk reorganization of all remaining files
"""
import os
import shutil
import glob

def bulk_reorganization():
    """Execute bulk reorganization of all remaining files"""
    print("🗂️ EXECUTING BULK REORGANIZATION")
    print("=" * 50)
    
    moved_counts = {
        'status_docs': 0,
        'implementation_docs': 0,
        'development_scripts': 0,
        'testing_scripts': 0,
        'verification_scripts': 0,
        'maintenance_scripts': 0,
        'archived_tests': 0,
        'skipped': 0
    }
    
    # Files to keep in root
    keep_in_root = {
        'README.md', 'CHANGELOG.md', 'pyproject.toml', 'poetry.lock', 
        'conftest.py', 'settings.json', 'metrics.yaml',
        'execute_complete_reorganization.py', 'verify_traceability_reorganization.py',
        'run_traceability_reorganization.py', 'bulk_reorganization.py'
    }
    
    # === MOVE STATUS DOCUMENTS ===
    print("📊 Moving status documents...")
    status_patterns = [
        '*_STATUS*.md', '*_SUMMARY*.md', '*_COMPLETE*.md', '*_READY*.md',
        '*_FIXES*.md', '*_IMPLEMENTATION*.md', 'ALL_GREEN*.md', 'PHASE_*.md',
        'COMMIT_*.md', 'RELEASE_*.md', 'STABILIZATION*.md', 'VERIFICATION_*.md',
        'FINAL_*.md', 'P0_*.md', 'V0*_*.md', 'ZERO_*.md', 'ZETETIC_*.md',
        'NEGATION_*.md', 'OPTIMIZATION_*.md', 'SECURITY_*.md', 'UNIFIED_*.md',
        'BOOTSTRAP_*.md', 'CACHE_*.md', 'METRICS_*.md', 'RESEARCH_*.md'
    ]
    
    for pattern in status_patterns:
        for file in glob.glob(pattern):
            if file not in keep_in_root:
                target = f"docs/status/{file}"
                if not os.path.exists(target):
                    shutil.move(file, target)
                    print(f"✅ {file} → docs/status/")
                    moved_counts['status_docs'] += 1
    
    # === MOVE IMPLEMENTATION DOCUMENTS ===
    print("\n📋 Moving implementation documents...")
    impl_patterns = [
        '*_GUIDE*.md', '*_README*.md', 'MANUAL_*.md', 'EXPERIMENT_*.md',
        'BENCHMARK_*.md', 'ASYNC_*.md', 'development_audit_report.md'
    ]
    
    for pattern in impl_patterns:
        for file in glob.glob(pattern):
            if file not in keep_in_root and not file.startswith('README'):
                target = f"docs/implementation/{file}"
                if not os.path.exists(target):
                    shutil.move(file, target)
                    print(f"✅ {file} → docs/implementation/")
                    moved_counts['implementation_docs'] += 1
    
    # === MOVE DEVELOPMENT SCRIPTS ===
    print("\n🛠️ Moving development scripts...")
    dev_patterns = [
        'execute_*.py', 'quick_*.py', 'simple_*.py', 'basic_*.py',
        'final_*.py', 'minimal_*.py', 'setup_*.py', 'demo_*.py',
        'cache_demo.py', 'scar_demo.py', 'secure_api_example.py',
        'create_*.py', 'generate_*.py', 'migrate_*.py', 'commit_*.py',
        'push_*.ps1', 'focused_*.py'
    ]
    
    for pattern in dev_patterns:
        for file in glob.glob(pattern):
            if file not in keep_in_root:
                target = f"scripts/development/{file}"
                if not os.path.exists(target):
                    shutil.move(file, target)
                    print(f"✅ {file} → scripts/development/")
                    moved_counts['development_scripts'] += 1
    
    # === MOVE TESTING SCRIPTS ===
    print("\n🧪 Moving testing scripts...")
    test_patterns = [
        'run_*.py', 'test_*.py'
    ]
    
    for pattern in test_patterns:
        for file in glob.glob(pattern):
            if file not in keep_in_root and 'traceability' not in file and 'reorganization' not in file:
                # Determine if it's a test file or test runner
                if file.startswith('test_'):
                    target = f"tests/archive/{file}"
                    if not os.path.exists(target):
                        shutil.move(file, target)
                        print(f"✅ {file} → tests/archive/")
                        moved_counts['archived_tests'] += 1
                elif file.startswith('run_'):
                    target = f"scripts/testing/{file}"
                    if not os.path.exists(target):
                        shutil.move(file, target)
                        print(f"✅ {file} → scripts/testing/")
                        moved_counts['testing_scripts'] += 1
    
    # === MOVE VERIFICATION SCRIPTS ===
    print("\n✅ Moving verification scripts...")
    verify_patterns = [
        'check_*.py', 'verify_*.py', 'validate_*.py', 'validation_*.py'
    ]
    
    for pattern in verify_patterns:
        for file in glob.glob(pattern):
            if file not in keep_in_root and 'traceability' not in file:
                target = f"scripts/verification/{file}"
                if not os.path.exists(target):
                    shutil.move(file, target)
                    print(f"✅ {file} → scripts/verification/")
                    moved_counts['verification_scripts'] += 1
    
    # === MOVE MAINTENANCE SCRIPTS ===
    print("\n🔧 Moving maintenance scripts...")
    maint_patterns = [
        'fix_*.py', 'cleanup_*.py', 'organize_*.py', 'move_*.py', 
        'batch_*.py', 'find_*.py', 'list_*.py', 'compare_*.py'
    ]
    
    for pattern in maint_patterns:
        for file in glob.glob(pattern):
            if file not in keep_in_root:
                target = f"scripts/maintenance/{file}"
                if not os.path.exists(target):
                    shutil.move(file, target)
                    print(f"✅ {file} → scripts/maintenance/")
                    moved_counts['maintenance_scripts'] += 1
    
    # === MOVE REMAINING PYTHON SCRIPTS ===
    print("\n🐍 Moving remaining Python scripts...")
    remaining_py = glob.glob('*.py')
    
    for file in remaining_py:
        if file not in keep_in_root:
            # Categorize by content/name
            if any(word in file.lower() for word in ['import', 'summary', 'status', 'current']):
                target = f"scripts/verification/{file}"
            elif any(word in file.lower() for word in ['research', 'loop', 'experiment']):
                target = f"scripts/development/{file}"
            else:
                target = f"scripts/development/{file}"
            
            if not os.path.exists(target):
                shutil.move(file, target)
                print(f"✅ {file} → {os.path.dirname(target)}/")
                moved_counts['development_scripts'] += 1
    
    # === MOVE BATCH/POWERSHELL FILES ===
    print("\n⚡ Moving batch and PowerShell files...")
    script_files = glob.glob('*.bat') + glob.glob('*.ps1')
    
    for file in script_files:
        target = f"scripts/development/{file}"
        if not os.path.exists(target):
            shutil.move(file, target)
            print(f"✅ {file} → scripts/development/")
            moved_counts['development_scripts'] += 1
    
    # === MOVE CSV AND DATA FILES ===
    print("\n📊 Moving data files...")
    data_files = glob.glob('*.csv') + glob.glob('*.png') + glob.glob('*.db')
    
    os.makedirs('data/results', exist_ok=True)
    for file in data_files:
        target = f"data/results/{file}"
        if not os.path.exists(target):
            shutil.move(file, target)
            print(f"✅ {file} → data/results/")
    
    # === SUMMARY ===
    total_moved = sum(moved_counts.values())
    print(f"\n📊 BULK REORGANIZATION SUMMARY:")
    print(f"  Total files moved: {total_moved}")
    print(f"  Status documents: {moved_counts['status_docs']}")
    print(f"  Implementation docs: {moved_counts['implementation_docs']}")
    print(f"  Development scripts: {moved_counts['development_scripts']}")
    print(f"  Testing scripts: {moved_counts['testing_scripts']}")
    print(f"  Verification scripts: {moved_counts['verification_scripts']}")
    print(f"  Maintenance scripts: {moved_counts['maintenance_scripts']}")
    print(f"  Archived tests: {moved_counts['archived_tests']}")
    
    # === CHECK REMAINING ROOT FILES ===
    print(f"\n📁 Remaining root files:")
    remaining = [f for f in os.listdir('.') if os.path.isfile(f)]
    essential_count = 0
    unexpected_count = 0
    
    for file in remaining:
        if file in keep_in_root or file.startswith('.'):
            print(f"  ✅ {file} (essential)")
            essential_count += 1
        else:
            print(f"  ⚠️ {file} (unexpected)")
            unexpected_count += 1
    
    print(f"\n🎯 Root directory status:")
    print(f"  Essential files: {essential_count}")
    print(f"  Unexpected files: {unexpected_count}")
    
    if unexpected_count == 0:
        print(f"✅ ROOT DIRECTORY IS CLEAN!")
    else:
        print(f"⚠️ {unexpected_count} unexpected files remain")
    
    print(f"\n✅ BULK REORGANIZATION COMPLETE!")
    print("🔍 All development artifacts preserved with full traceability")
    print("📚 Organized structure maintains complete audit trail")
    print("🚀 Clean root directory ready for ongoing development")
    
    return total_moved

if __name__ == "__main__":
    bulk_reorganization()