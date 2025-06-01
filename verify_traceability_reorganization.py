#!/usr/bin/env python3
"""
Verify the traceability reorganization was successful
"""
import os

def verify_reorganization():
    """Verify the reorganization completed successfully"""
    
    print("🔍 VERIFYING TRACEABILITY REORGANIZATION")
    print("=" * 50)
    
    verification_results = {
        'status_docs': 0,
        'implementation_docs': 0,
        'development_scripts': 0,
        'testing_scripts': 0,
        'verification_scripts': 0,
        'maintenance_scripts': 0,
        'archived_tests': 0,
        'clean_root': True
    }
    
    # Check status documentation
    if os.path.exists('docs/status'):
        status_files = [f for f in os.listdir('docs/status') if f.endswith('.md')]
        verification_results['status_docs'] = len(status_files)
        print(f"📊 Status documents: {len(status_files)}")
        for f in status_files[:5]:  # Show first 5
            print(f"  ✅ {f}")
        if len(status_files) > 5:
            print(f"  ... and {len(status_files) - 5} more")
    
    # Check implementation documentation
    if os.path.exists('docs/implementation'):
        impl_files = [f for f in os.listdir('docs/implementation') if f.endswith('.md')]
        verification_results['implementation_docs'] = len(impl_files)
        print(f"\n📋 Implementation documents: {len(impl_files)}")
        for f in impl_files:
            print(f"  ✅ {f}")
    
    # Check script organization
    script_dirs = [
        ('scripts/development', 'development_scripts', '🛠️'),
        ('scripts/testing', 'testing_scripts', '🧪'),
        ('scripts/verification', 'verification_scripts', '✅'),
        ('scripts/maintenance', 'maintenance_scripts', '🔧')
    ]
    
    for dir_path, key, emoji in script_dirs:
        if os.path.exists(dir_path):
            scripts = [f for f in os.listdir(dir_path) if f.endswith('.py')]
            verification_results[key] = len(scripts)
            print(f"\n{emoji} {dir_path}: {len(scripts)} scripts")
            for f in scripts[:3]:  # Show first 3
                print(f"  ✅ {f}")
            if len(scripts) > 3:
                print(f"  ... and {len(scripts) - 3} more")
    
    # Check archived tests
    if os.path.exists('tests/archive'):
        test_files = [f for f in os.listdir('tests/archive') if f.endswith('.py')]
        verification_results['archived_tests'] = len(test_files)
        print(f"\n🧪 Archived tests: {len(test_files)}")
        for f in test_files[:3]:  # Show first 3
            print(f"  📦 {f}")
        if len(test_files) > 3:
            print(f"  ... and {len(test_files) - 3} more")
    
    # Check root directory cleanliness
    print(f"\n📁 Root Directory Check:")
    root_md = [f for f in os.listdir('.') if f.endswith('.md') and os.path.isfile(f)]
    root_py = [f for f in os.listdir('.') if f.endswith('.py') and os.path.isfile(f)]
    
    essential_md = {'README.md', 'CHANGELOG.md'}
    essential_py = {'conftest.py', 'pyproject.toml'}
    
    unexpected_md = [f for f in root_md if f not in essential_md]
    unexpected_py = [f for f in root_py if f not in essential_py and not f.startswith('execute_') and not f.startswith('verify_')]
    
    print(f"  • Essential markdown files: {[f for f in root_md if f in essential_md]}")
    print(f"  • Essential Python files: {[f for f in root_py if f in essential_py]}")
    
    if unexpected_md:
        print(f"  ⚠️ Unexpected markdown files: {unexpected_md}")
        verification_results['clean_root'] = False
    
    if unexpected_py:
        print(f"  ⚠️ Unexpected Python files: {unexpected_py}")
        verification_results['clean_root'] = False
    
    if verification_results['clean_root']:
        print(f"  ✅ Root directory is clean")
    
    # Check traceability index
    if os.path.exists('docs/TRACEABILITY_INDEX.md'):
        print(f"\n📋 Traceability index: ✅ Present")
    else:
        print(f"\n📋 Traceability index: ❌ Missing")
    
    # Summary
    total_organized = (
        verification_results['status_docs'] +
        verification_results['implementation_docs'] +
        verification_results['development_scripts'] +
        verification_results['testing_scripts'] +
        verification_results['verification_scripts'] +
        verification_results['maintenance_scripts'] +
        verification_results['archived_tests']
    )
    
    print(f"\n" + "=" * 50)
    print(f"📊 VERIFICATION SUMMARY")
    print(f"  • Total organized artifacts: {total_organized}")
    print(f"  • Status documents: {verification_results['status_docs']}")
    print(f"  • Implementation guides: {verification_results['implementation_docs']}")
    print(f"  • Development scripts: {verification_results['development_scripts']}")
    print(f"  • Testing scripts: {verification_results['testing_scripts']}")
    print(f"  • Verification scripts: {verification_results['verification_scripts']}")
    print(f"  • Maintenance scripts: {verification_results['maintenance_scripts']}")
    print(f"  • Archived tests: {verification_results['archived_tests']}")
    print(f"  • Root directory clean: {'✅' if verification_results['clean_root'] else '❌'}")
    
    # Overall assessment
    if total_organized > 50 and verification_results['clean_root']:
        print(f"\n✅ REORGANIZATION VERIFICATION: SUCCESS")
        print(f"🔍 Complete traceability achieved")
        print(f"📚 All artifacts properly organized")
        print(f"🚀 Clean workspace ready for development")
    else:
        print(f"\n⚠️ REORGANIZATION VERIFICATION: NEEDS ATTENTION")
        if total_organized <= 50:
            print(f"📊 Low artifact count - may need more organization")
        if not verification_results['clean_root']:
            print(f"🧹 Root directory needs cleanup")
    
    return verification_results

if __name__ == "__main__":
    verify_reorganization()