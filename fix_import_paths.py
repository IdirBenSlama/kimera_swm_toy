#!/usr/bin/env python3
"""
Fix import path issues in Kimera SWM project.
Addresses architectural drift where tests reference non-existent kimera.core modules.
"""

import os
import sys
import re
import glob
from pathlib import Path

def fix_imports_in_file(file_path):
    """Fix import statements in a single file."""
    print(f"🔧 Fixing imports in {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix common import patterns
        replacements = [
            # kimera.core.scar -> kimera.scar
            (r'from kimera\.core\.scar import', 'from kimera.scar import'),
            (r'import kimera\.core\.scar', 'import kimera.scar'),
            
            # kimera.core -> kimera (for other modules)
            (r'from kimera\.core\.([a-zA-Z_]+) import', r'from kimera.\1 import'),
            (r'import kimera\.core\.([a-zA-Z_]+)', r'import kimera.\1'),
            
            # Fix specific common imports
            (r'from kimera\.core import', 'from kimera import'),
            
            # Vault imports (already correct)
            # vault.core.vault should stay as is
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        # Add sys.path fix at the top if it's a test file and doesn't have it
        if ('test_' in file_path or file_path.endswith('_test.py')) and 'sys.path.insert' not in content:
            lines = content.split('\n')
            
            # Find where to insert sys.path fix (after imports, before main code)
            insert_pos = 0
            for i, line in enumerate(lines):
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    insert_pos = i + 1
                elif line.strip() and not line.strip().startswith('#'):
                    break
            
            # Insert sys.path fix
            sys_path_fix = [
                '',
                '# Fix import paths',
                'import sys',
                'import os',
                'sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))',
                ''
            ]
            
            lines[insert_pos:insert_pos] = sys_path_fix
            content = '\n'.join(lines)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Fixed imports in {file_path}")
            return True
        else:
            print(f"  ⏭️  No changes needed in {file_path}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error fixing {file_path}: {e}")
        return False

def find_python_files():
    """Find all Python files that might need import fixes."""
    patterns = [
        'test_*.py',
        '*_test.py',
        'run_*.py',
        'verify_*.py',
        'check_*.py',
        'fix_*.py',
        'execute_*.py',
        'quick_*.py',
        'final_*.py',
        'minimal_*.py',
        'simple_*.py',
        'basic_*.py',
        'scar_*.py'
    ]
    
    files = []
    for pattern in patterns:
        files.extend(glob.glob(pattern))
    
    return files

def main():
    """Main execution function."""
    print("🚀 Fixing import path issues in Kimera SWM project...")
    print()
    
    # Find files to fix
    files_to_fix = find_python_files()
    
    if not files_to_fix:
        print("❌ No Python files found to fix")
        return False
    
    print(f"📁 Found {len(files_to_fix)} files to check:")
    for f in files_to_fix:
        print(f"  - {f}")
    print()
    
    # Fix imports in each file
    fixed_count = 0
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            if fix_imports_in_file(file_path):
                fixed_count += 1
    
    print()
    print(f"📊 Results: Fixed imports in {fixed_count}/{len(files_to_fix)} files")
    
    # Create a quick test to verify the fixes
    print()
    print("🧪 Creating verification test...")
    
    test_content = '''#!/usr/bin/env python3
"""Quick test to verify import fixes."""

# Fix import paths
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

def test_imports():
    """Test that all imports work correctly."""
    print("🧪 Testing imports after fixes...")
    
    try:
        # Test kimera.scar import (the main issue)
        from kimera.scar import Scar, create_scar
        print("  ✅ kimera.scar imports working")
        
        # Test other kimera imports
        from kimera.identity import Identity, create_scar_identity
        print("  ✅ kimera.identity imports working")
        
        from kimera.storage import LatticeStorage
        print("  ✅ kimera.storage imports working")
        
        # Test vault import
        from vault.core.vault import Vault
        print("  ✅ vault.core.vault imports working")
        
        print("  🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"  ❌ Import test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
'''
    
    with open('test_import_fixes.py', 'w') as f:
        f.write(test_content)
    
    print("  ✅ Created test_import_fixes.py")
    print()
    print("🎯 Import path fixes complete!")
    print()
    print("Next steps:")
    print("1. Run: python test_import_fixes.py")
    print("2. Run: python test_system_quick.py")
    print("3. Run: python test_vault_and_scar.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)