#!/usr/bin/env python3
"""
Quick cleanup utility for development
"""
import os
import shutil
import glob

def quick_cleanup():
    """Perform quick cleanup of development artifacts"""
    print("🧹 QUICK CLEANUP")
    print("=" * 20)
    
    cleanup_items = []
    
    # Clean up Python cache
    cache_dirs = []
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            cache_dirs.append(os.path.join(root, '__pycache__'))
    
    for cache_dir in cache_dirs:
        try:
            shutil.rmtree(cache_dir)
            cleanup_items.append(f"Removed {cache_dir}")
        except Exception as e:
            cleanup_items.append(f"Failed to remove {cache_dir}: {e}")
    
    # Clean up .pyc files
    pyc_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                pyc_files.append(os.path.join(root, file))
    
    for pyc_file in pyc_files:
        try:
            os.remove(pyc_file)
            cleanup_items.append(f"Removed {pyc_file}")
        except Exception as e:
            cleanup_items.append(f"Failed to remove {pyc_file}: {e}")
    
    # Clean up temporary files
    temp_patterns = ['*.tmp', '*.temp', '.DS_Store', 'Thumbs.db']
    for pattern in temp_patterns:
        temp_files = glob.glob(pattern)
        for temp_file in temp_files:
            try:
                os.remove(temp_file)
                cleanup_items.append(f"Removed {temp_file}")
            except Exception as e:
                cleanup_items.append(f"Failed to remove {temp_file}: {e}")
    
    print(f"📊 Cleanup completed: {len(cleanup_items)} items processed")
    for item in cleanup_items[:10]:  # Show first 10
        print(f"  • {item}")
    if len(cleanup_items) > 10:
        print(f"  ... and {len(cleanup_items) - 10} more")
    
    return len(cleanup_items)

if __name__ == "__main__":
    quick_cleanup()