#!/usr/bin/env python3
"""
Check current reorganization status
"""
import os

def check_reorganization_status():
    """Check the current state of reorganization"""
    print("🔍 CHECKING REORGANIZATION STATUS")
    print("=" * 40)
    
    # Check docs/status
    if os.path.exists('docs/status'):
        status_files = [f for f in os.listdir('docs/status') if f.endswith('.md')]
        print(f"📊 docs/status: {len(status_files)} files")
        for f in status_files:
            print(f"  ✅ {f}")
    else:
        print("📊 docs/status: NOT FOUND")
    
    # Check docs/implementation
    if os.path.exists('docs/implementation'):
        impl_files = [f for f in os.listdir('docs/implementation') if f.endswith('.md')]
        print(f"\n📋 docs/implementation: {len(impl_files)} files")
        for f in impl_files:
            print(f"  ✅ {f}")
    else:
        print("\n📋 docs/implementation: NOT FOUND")
    
    # Check scripts organization
    script_dirs = ['scripts/development', 'scripts/testing', 'scripts/verification', 'scripts/maintenance']
    
    for dir_path in script_dirs:
        if os.path.exists(dir_path):
            scripts = [f for f in os.listdir(dir_path) if f.endswith('.py')]
            print(f"\n🔧 {dir_path}: {len(scripts)} scripts")
            for script in scripts[:3]:
                print(f"  ✅ {script}")
            if len(scripts) > 3:
                print(f"  ... and {len(scripts) - 3} more")
        else:
            print(f"\n🔧 {dir_path}: NOT FOUND")
    
    # Check tests/archive
    if os.path.exists('tests/archive'):
        test_files = [f for f in os.listdir('tests/archive') if f.endswith('.py')]
        print(f"\n🧪 tests/archive: {len(test_files)} files")
        for f in test_files[:3]:
            print(f"  ✅ {f}")
        if len(test_files) > 3:
            print(f"  ... and {len(test_files) - 3} more")
    else:
        print("\n🧪 tests/archive: NOT FOUND")
    
    # Check root directory
    root_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    md_files = [f for f in root_files if f.endswith('.md')]
    py_files = [f for f in root_files if f.endswith('.py')]
    
    print(f"\n📁 Root directory:")
    print(f"  Markdown files: {len(md_files)}")
    for f in md_files:
        print(f"    • {f}")
    
    print(f"  Python files: {len(py_files)}")
    for f in py_files[:5]:
        print(f"    • {f}")
    if len(py_files) > 5:
        print(f"    ... and {len(py_files) - 5} more")
    
    return {
        'status_docs': len(status_files) if os.path.exists('docs/status') else 0,
        'root_md': len(md_files),
        'root_py': len(py_files)
    }

if __name__ == "__main__":
    check_reorganization_status()