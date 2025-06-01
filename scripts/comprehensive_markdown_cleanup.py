#!/usr/bin/env python3
"""
Comprehensive cleanup of all markdown files from root directory
"""
import os
import shutil

def comprehensive_markdown_cleanup():
    """Move all status/summary markdown files to docs/ARCHIVE/"""
    
    # Files that should stay in root
    keep_in_root = {
        'README.md',
        'CHANGELOG.md',
        'LICENSE.md'
    }
    
    # Files that should go to main docs/ (not archive)
    move_to_docs = {
        'SCAR_IMPLEMENTATION_GUIDE.md',
        'TEST_SUITE_README.md'
    }
    
    # Get all markdown files in root
    all_md_files = [f for f in os.listdir('.') if f.endswith('.md') and os.path.isfile(f)]
    
    # Files to move to archive (everything else)
    move_to_archive = [f for f in all_md_files if f not in keep_in_root and f not in move_to_docs]
    
    # Ensure directories exist
    os.makedirs("docs", exist_ok=True)
    os.makedirs("docs/ARCHIVE", exist_ok=True)
    
    moved_to_archive = 0
    moved_to_docs = 0
    skipped = 0
    
    print("🧹 Comprehensive markdown cleanup...")
    print("=" * 60)
    print(f"Found {len(all_md_files)} markdown files in root directory")
    print(f"  • Keep in root: {len(keep_in_root)} files")
    print(f"  • Move to docs/: {len(move_to_docs)} files")
    print(f"  • Move to archive: {len(move_to_archive)} files")
    print()
    
    # Move files to main docs
    for filename in move_to_docs:
        if os.path.exists(filename):
            target_path = f"docs/{filename}"
            if not os.path.exists(target_path):
                try:
                    shutil.move(filename, target_path)
                    print(f"📄 {filename} → docs/")
                    moved_to_docs += 1
                except Exception as e:
                    print(f"❌ Error moving {filename}: {e}")
            else:
                print(f"⚠️  {filename} already exists in docs/, removing from root")
                os.remove(filename)
                moved_to_docs += 1
    
    # Move files to archive
    for filename in move_to_archive:
        if os.path.exists(filename):
            target_path = f"docs/ARCHIVE/{filename}"
            if not os.path.exists(target_path):
                try:
                    shutil.move(filename, target_path)
                    print(f"📁 {filename} → docs/ARCHIVE/")
                    moved_to_archive += 1
                except Exception as e:
                    print(f"❌ Error moving {filename}: {e}")
            else:
                print(f"⚠️  {filename} already exists in archive, removing from root")
                os.remove(filename)
                moved_to_archive += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Cleanup Summary:")
    print(f"  • Moved to docs/: {moved_to_docs} files")
    print(f"  • Moved to docs/ARCHIVE/: {moved_to_archive} files")
    print(f"  • Kept in root: {len([f for f in os.listdir('.') if f.endswith('.md') and f in keep_in_root])} files")
    
    # Verify final state
    remaining_md = [f for f in os.listdir('.') if f.endswith('.md') and os.path.isfile(f)]
    unexpected = [f for f in remaining_md if f not in keep_in_root]
    
    if unexpected:
        print(f"\n⚠️  Unexpected markdown files still in root:")
        for f in unexpected:
            print(f"    • {f}")
    else:
        print(f"\n✅ Root directory is clean! Only essential files remain:")
        for f in remaining_md:
            print(f"    • {f}")
    
    print(f"\n📁 Archive now contains {len(os.listdir('docs/ARCHIVE'))} files")
    print(f"📄 Main docs contains {len([f for f in os.listdir('docs') if f.endswith('.md')])} markdown files")

if __name__ == "__main__":
    comprehensive_markdown_cleanup()