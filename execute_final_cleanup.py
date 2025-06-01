#!/usr/bin/env python3
"""
Execute final cleanup of all markdown files
"""
import os
import shutil

# Get all markdown files in root
all_md = [f for f in os.listdir('.') if f.endswith('.md') and os.path.isfile(f)]

# Files to keep in root
keep_in_root = {'README.md', 'CHANGELOG.md'}

# Files to move to docs/ (main documentation)
move_to_docs = {'SCAR_IMPLEMENTATION_GUIDE.md', 'TEST_SUITE_README.md'}

# Everything else goes to archive
move_to_archive = [f for f in all_md if f not in keep_in_root and f not in move_to_docs]

print(f"Found {len(all_md)} markdown files")
print(f"Moving {len(move_to_archive)} files to archive...")

# Ensure directories exist
os.makedirs("docs/ARCHIVE", exist_ok=True)

moved = 0
for filename in move_to_archive:
    if os.path.exists(filename):
        target = f"docs/ARCHIVE/{filename}"
        try:
            if not os.path.exists(target):
                shutil.move(filename, target)
                print(f"✅ {filename}")
                moved += 1
            else:
                # Already exists, just remove from root
                os.remove(filename)
                print(f"🗑️ {filename} (duplicate)")
                moved += 1
        except Exception as e:
            print(f"❌ {filename}: {e}")

# Move docs files
for filename in move_to_docs:
    if os.path.exists(filename):
        target = f"docs/{filename}"
        try:
            if not os.path.exists(target):
                shutil.move(filename, target)
                print(f"📄 {filename} → docs/")
            else:
                os.remove(filename)
                print(f"🗑️ {filename} (duplicate in docs)")
        except Exception as e:
            print(f"❌ {filename}: {e}")

print(f"\n✅ Moved {moved} files")

# Check final state
remaining = [f for f in os.listdir('.') if f.endswith('.md') and os.path.isfile(f)]
print(f"Remaining in root: {remaining}")

archive_count = len([f for f in os.listdir('docs/ARCHIVE') if f.endswith('.md')])
print(f"Archive now has {archive_count} markdown files")