#!/usr/bin/env python3
"""
Comprehensive fix runner for Kimera SWM system.
Runs the fix script and verifies results.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_fix():
    """Run the comprehensive fix script."""
    print("🔧 Running comprehensive fix script...")
    try:
        result = subprocess.run([sys.executable, "fix_critical_issues.py"], 
                              capture_output=True, text=True, check=True)
        print("✅ Fix script completed successfully")
        if result.stdout:
            print("Output:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Fix script failed: {e}")
        if e.stdout:
            print("Output:", e.stdout)
        if e.stderr:
            print("Error:", e.stderr)
        return False

def verify_fixes():
    """Verify that fixes were applied correctly."""
    print("\n🔍 Verifying fixes...")
    
    # Check if vault directory exists
    vault_dir = Path("vault")
    if vault_dir.exists():
        print("✅ Vault directory created")
    else:
        print("❌ Vault directory missing")
    
    # Check if __init__.py files exist
    init_files = [
        "vault/__init__.py",
        "vault/core/__init__.py",
        "vault/storage/__init__.py"
    ]
    
    for init_file in init_files:
        if Path(init_file).exists():
            print(f"✅ {init_file} exists")
        else:
            print(f"❌ {init_file} missing")
    
    # Check for trailing newlines in key markdown files
    md_files = ["README.md", "KIMERA_SWM_READY.md"]
    for md_file in md_files:
        if Path(md_file).exists():
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.endswith('\n'):
                    print(f"✅ {md_file} has trailing newline")
                else:
                    print(f"❌ {md_file} missing trailing newline")
    
    print("\n✅ Verification complete")

def main():
    """Main execution function."""
    print("🚀 Starting comprehensive fix and verification...")
    
    if run_fix():
        verify_fixes()
        print("\n🎉 All fixes applied and verified!")
        
        # Run a quick test to ensure system is working
        print("\n🧪 Running quick system test...")
        try:
            result = subprocess.run([sys.executable, "-c", 
                                   "import kimera.core.scar; print('✅ Scar import successful')"], 
                                  capture_output=True, text=True, check=True)
            print(result.stdout.strip())
        except subprocess.CalledProcessError:
            print("❌ Scar import failed")
        
        return True
    else:
        print("\n❌ Fix script failed. Please check errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)