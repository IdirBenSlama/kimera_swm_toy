#!/usr/bin/env python3
"""
Batch move status files to organized locations
"""
import os
import shutil

def batch_move_status_files():
    """Move status files to docs/status/"""
    
    status_files = [
        "IMPLEMENTATION_COMPLETE_SUMMARY.md",
        "IMPORT_FIXES_COMPLETE.md",
        "ISSUES_RESOLVED_SUMMARY.md",
        "KIMERA_SWM_READY.md",
        "P0_STATUS_SUMMARY.md",
        "SCAR_FIXES_SUMMARY.md",
        "TEST_SUITE_IMPLEMENTATION_SUMMARY.md",
        "UNICODE_ENCODING_FIX_SUMMARY.md",
        "UNICODE_FIX_COMPLETE.md",
        "VERIFICATION_READY.md",
        "REORGANIZATION_COMPLETE.md"
    ]
    
    moved = 0
    for filename in status_files:
        if os.path.exists(filename):
            target = f"docs/status/{filename}"
            if not os.path.exists(target):
                shutil.move(filename, target)
                print(f"✅ Moved {filename}")
                moved += 1
            else:
                print(f"🔄 {filename} already exists in target")
    
    print(f"📊 Moved {moved} status files")
    return moved

if __name__ == "__main__":
    batch_move_status_files()