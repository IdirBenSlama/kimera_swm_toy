#!/usr/bin/env python3
"""
Quick fix utility for common issues
"""
import os
import sys

def quick_fix():
    """Apply quick fixes for common issues"""
    print("🔧 QUICK FIX")
    print("=" * 15)
    
    fixes_applied = []
    
    # Fix 1: Ensure src is in Python path
    src_path = os.path.abspath('src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
        fixes_applied.append("Added src to Python path")
    
    # Fix 2: Check core imports
    try:
        import kimera.identity
        fixes_applied.append("✅ kimera.identity import working")
    except ImportError as e:
        fixes_applied.append(f"❌ kimera.identity import failed: {e}")
    
    try:
        import kimera.storage
        fixes_applied.append("✅ kimera.storage import working")
    except ImportError as e:
        fixes_applied.append(f"❌ kimera.storage import failed: {e}")
    
    # Fix 3: Check vault imports
    try:
        import vault.core.vault
        fixes_applied.append("✅ vault.core.vault import working")
    except ImportError as e:
        fixes_applied.append(f"❌ vault.core.vault import failed: {e}")
    
    # Fix 4: Create missing directories
    required_dirs = [
        'docs/status',
        'docs/implementation', 
        'scripts/development',
        'scripts/testing',
        'scripts/verification',
        'scripts/maintenance',
        'tests/archive'
    ]
    
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            fixes_applied.append(f"Created directory: {dir_path}")
    
    print(f"📊 Quick fix completed: {len(fixes_applied)} items")
    for fix in fixes_applied:
        print(f"  • {fix}")
    
    return len(fixes_applied)

if __name__ == "__main__":
    quick_fix()