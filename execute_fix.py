#!/usr/bin/env python3

# Import and run the fix functions directly
import os
import re
import ast
import subprocess
from pathlib import Path
from typing import List, Set

def fix_trailing_newlines():
    """Fix missing trailing newlines in markdown files."""
    print("🔧 Fixing trailing newlines in markdown files...")
    
    md_files = [
        "README.md",
        "KIMERA_SWM_READY.md",
        "docs/ARCHITECTURE.md",
        "docs/SCAR_SPECIFICATION.md"
    ]
    
    for md_file in md_files:
        if Path(md_file).exists():
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.endswith('\n'):
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content + '\n')
                print(f"  ✅ Fixed {md_file}")
            else:
                print(f"  ✅ {md_file} already has trailing newline")

def create_vault_infrastructure():
    """Create basic vault infrastructure if missing."""
    print("🔧 Creating vault infrastructure...")
    
    vault_dirs = [
        "vault",
        "vault/core",
        "vault/storage"
    ]
    
    for vault_dir in vault_dirs:
        Path(vault_dir).mkdir(parents=True, exist_ok=True)
        print(f"  📁 Created directory: {vault_dir}")
    
    # Create __init__.py files
    init_files = [
        "vault/__init__.py",
        "vault/core/__init__.py", 
        "vault/storage/__init__.py"
    ]
    
    for init_file in init_files:
        init_path = Path(init_file)
        if not init_path.exists():
            init_path.write_text('"""Vault module."""\n')
            print(f"  📄 Created: {init_file}")
        else:
            print(f"  ✅ Already exists: {init_file}")

# Run the fixes
print("🚀 Running critical fixes...")
fix_trailing_newlines()
create_vault_infrastructure()
print("✅ Critical fixes completed!")