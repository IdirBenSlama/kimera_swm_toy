"""
Fix imports in example scripts to use working components
"""
from pathlib import Path
import re

def fix_imports(content):
    """Fix broken imports in content."""
    # Fix contradiction imports
    content = re.sub(
        r'from kimera\.contradiction import detect_contradiction',
        'from kimera.contradiction_v2_fixed import analyze_contradiction',
        content
    )
    
    # Fix thermodynamics imports
    content = re.sub(
        r'from kimera\.thermodynamics import ThermodynamicSystem',
        'from kimera.thermodynamics_v3 import ThermodynamicSystemV3 as ThermodynamicSystem',
        content
    )
    
    # Fix usage of detect_contradiction
    content = re.sub(
        r'detect_contradiction\s*\(',
        'analyze_contradiction(',
        content
    )
    
    return content

def main():
    """Fix all example files."""
    print("Fixing Example Imports")
    print("=" * 60)
    
    examples_dir = Path("examples")
    if not examples_dir.exists():
        print("No examples directory found")
        return
    
    fixed_count = 0
    for py_file in examples_dir.glob("*.py"):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                original = f.read()
            
            fixed = fix_imports(original)
            
            if fixed != original:
                with open(py_file, 'w', encoding='utf-8') as f:
                    f.write(fixed)
                print(f"✓ Fixed {py_file.name}")
                fixed_count += 1
        except Exception as e:
            print(f"✗ Error fixing {py_file.name}: {e}")
    
    print(f"\nFixed {fixed_count} files")

if __name__ == "__main__":
    main()