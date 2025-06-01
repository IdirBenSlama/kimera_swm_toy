#!/usr/bin/env python3
"""
Quick cleanup of obvious files
"""
import os
import shutil

# Remove files that already exist in archive
files_to_remove = [
    "ALL_GREEN_STATUS_CONFIRMED.md",  # We just updated it in archive
    "KIMERA_SWM_READY.md",           # Already in archive
    "SCAR_FIXES_SUMMARY.md",         # Already in archive
    "FINAL_STATUS.md",               # Already in archive
    "IMPLEMENTATION_COMPLETE_SUMMARY.md",  # Already in archive
    "IMPORT_FIXES_COMPLETE.md",      # Already in archive
    "ISSUES_RESOLVED_SUMMARY.md",    # Already in archive
    "P0_STATUS_SUMMARY.md"           # Already in archive
]

# Move these to docs/ (main documentation)
move_to_docs = [
    "SCAR_IMPLEMENTATION_GUIDE.md",
    "TEST_SUITE_README.md"
]

# Move the cleanup plan we just created
if os.path.exists("FINAL_CLEANUP_PLAN.md"):
    shutil.move("FINAL_CLEANUP_PLAN.md", "docs/FINAL_CLEANUP_PLAN.md")
    print("✅ Moved FINAL_CLEANUP_PLAN.md to docs/")

print("Removing duplicate files...")
removed = 0
for f in files_to_remove:
    if os.path.exists(f):
        os.remove(f)
        print(f"🗑️ Removed {f}")
        removed += 1

print("Moving documentation files...")
moved = 0
for f in move_to_docs:
    if os.path.exists(f):
        target = f"docs/{f}"
        if not os.path.exists(target):
            shutil.move(f, target)
            print(f"📄 Moved {f} to docs/")
            moved += 1
        else:
            os.remove(f)
            print(f"🗑️ Removed duplicate {f}")

print(f"\n✅ Removed {removed} duplicate files")
print(f"✅ Moved {moved} documentation files")

# Quick count of remaining files
remaining_md = [f for f in os.listdir('.') if f.endswith('.md') and os.path.isfile(f)]
remaining_py = [f for f in os.listdir('.') if f.endswith('.py') and os.path.isfile(f)]

print(f"\nRemaining in root:")
print(f"  • {len(remaining_md)} markdown files")
print(f"  • {len(remaining_py)} Python files")

if len(remaining_md) <= 5:
    print(f"  Markdown files: {remaining_md}")
else:
    print(f"  Still need to clean up {len(remaining_md) - 2} status files (keeping README.md, CHANGELOG.md)")