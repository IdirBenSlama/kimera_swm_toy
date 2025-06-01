#!/usr/bin/env python3
"""
Move test files to archive
"""
import os
import shutil
import glob

def move_test_files():
    """Move test files to tests/archive/"""
    print("🧪 MOVING TEST FILES TO ARCHIVE")
    print("=" * 35)
    
    # Create archive directory
    os.makedirs("tests/archive", exist_ok=True)
    print("📁 Created tests/archive/")
    
    # Find test files in root
    test_patterns = [
        'test_*.py',
        '*_test.py'
    ]
    
    test_files = []
    for pattern in test_patterns:
        test_files.extend(glob.glob(pattern))
    
    # Remove duplicates
    test_files = list(set(test_files))
    
    moved_count = 0
    for test_file in test_files:
        target_path = f"tests/archive/{test_file}"
        
        if not os.path.exists(target_path):
            shutil.move(test_file, target_path)
            print(f"📦 Moved {test_file} → tests/archive/")
            moved_count += 1
        else:
            print(f"⚠️ {test_file} already exists in archive")
    
    # Summary
    print(f"\n📊 TEST FILE ARCHIVE SUMMARY:")
    print(f"  Files moved: {moved_count}")
    
    # List archive contents
    if os.path.exists("tests/archive"):
        archive_files = [f for f in os.listdir("tests/archive") if f.endswith('.py')]
        print(f"  Archive contains: {len(archive_files)} test files")
        
        for test_file in archive_files[:5]:  # Show first 5
            print(f"    • {test_file}")
        if len(archive_files) > 5:
            print(f"    ... and {len(archive_files) - 5} more")
    
    return moved_count

if __name__ == "__main__":
    move_test_files()