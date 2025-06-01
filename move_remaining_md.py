#!/usr/bin/env python3
"""
Move remaining markdown files to appropriate locations
"""
import os
import shutil

# Files to move to docs/ARCHIVE/
archive_files = [
    "IMPORT_FIXES_COMPLETE.md",
    "ISSUES_RESOLVED_SUMMARY.md", 
    "TEST_SUITE_IMPLEMENTATION_SUMMARY.md",
    "UNICODE_ENCODING_FIX_SUMMARY.md",
    "UNICODE_FIX_COMPLETE.md",
    "VERIFICATION_READY.md",
    "development_audit_report.md"
]

# Files to delete (duplicates already exist in docs/)
delete_files = [
    "SCAR_IMPLEMENTATION_GUIDE.md",  # Already in docs/
    "TEST_SUITE_README.md",          # Already in docs/
    "REORGANIZATION_COMPLETE.md"     # Temporary file
]

print("Moving remaining markdown files...")

# Move to archive
for filename in archive_files:
    if os.path.exists(filename):
        target = f"docs/ARCHIVE/{filename}"
        if not os.path.exists(target):
            # Read content and create in archive
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(target, 'w', encoding='utf-8') as f:
                f.write(content)
            os.remove(filename)
            print(f"✅ Moved {filename} to docs/ARCHIVE/")
        else:
            os.remove(filename)
            print(f"✅ Removed duplicate {filename}")

# Delete duplicates
for filename in delete_files:
    if os.path.exists(filename):
        os.remove(filename)
        print(f"🗑️ Deleted {filename}")

# Also remove the files we already moved manually
manual_moved = ["KIMERA_SWM_READY.md", "SCAR_FIXES_SUMMARY.md"]
for filename in manual_moved:
    if os.path.exists(filename):
        os.remove(filename)
        print(f"✅ Removed {filename} (already in archive)")

print("✅ Markdown cleanup complete!")

# Check remaining files
remaining = [f for f in os.listdir('.') if f.endswith('.md') and os.path.isfile(f)]
print(f"\nRemaining .md files in root: {remaining}")