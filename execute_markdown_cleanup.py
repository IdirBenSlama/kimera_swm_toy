#!/usr/bin/env python3
"""
Execute the markdown cleanup directly
"""
import os
import shutil

# Files to move to docs/ARCHIVE/
files_to_archive = [
    "FINAL_STATUS.md",
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
    "development_audit_report.md"
]

# Files to move to docs/
files_to_docs = [
    "SCAR_IMPLEMENTATION_GUIDE.md",
    "TEST_SUITE_README.md"
]

# Files to delete
files_to_delete = [
    "REORGANIZATION_COMPLETE.md"
]

print("Moving markdown files...")

# Move to archive
for f in files_to_archive:
    if os.path.exists(f):
        target = f"docs/ARCHIVE/{f}"
        if not os.path.exists(target):
            shutil.move(f, target)
            print(f"✅ {f} → docs/ARCHIVE/")
        else:
            os.remove(f)
            print(f"✅ Removed duplicate {f}")

# Move to docs
for f in files_to_docs:
    if os.path.exists(f):
        target = f"docs/{f}"
        if not os.path.exists(target):
            shutil.move(f, target)
            print(f"✅ {f} → docs/")
        else:
            os.remove(f)
            print(f"✅ Removed duplicate {f}")

# Delete temporary files
for f in files_to_delete:
    if os.path.exists(f):
        os.remove(f)
        print(f"🗑️ Deleted {f}")

print("✅ Markdown cleanup complete!")