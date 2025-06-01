#!/usr/bin/env python3
"""
Clean up all remaining markdown files from root directory
"""
import os
import shutil

def cleanup_markdown_files():
    """Move all remaining status/summary markdown files to docs/ARCHIVE/"""
    
    # Files that should be moved to docs/ARCHIVE/
    markdown_files_to_archive = [
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
    
    # Files that should be moved to docs/ (main documentation)
    markdown_files_to_docs = [
        "SCAR_IMPLEMENTATION_GUIDE.md",
        "TEST_SUITE_README.md"
    ]
    
    # Files that should be deleted (duplicates or temporary)
    markdown_files_to_delete = [
        "REORGANIZATION_COMPLETE.md"  # This was just a summary, not needed long-term
    ]
    
    # Ensure target directories exist
    os.makedirs("docs/ARCHIVE", exist_ok=True)
    
    moved_to_archive = 0
    moved_to_docs = 0
    deleted = 0
    
    print("🧹 Cleaning up markdown files from root directory...")
    print("=" * 50)
    
    # Move files to archive
    for filename in markdown_files_to_archive:
        if os.path.exists(filename):
            target_path = f"docs/ARCHIVE/{filename}"
            if not os.path.exists(target_path):
                try:
                    shutil.move(filename, target_path)
                    print(f"✅ Moved {filename} to docs/ARCHIVE/")
                    moved_to_archive += 1
                except Exception as e:
                    print(f"❌ Error moving {filename}: {e}")
            else:
                print(f"⚠️  {filename} already exists in docs/ARCHIVE/, removing from root")
                os.remove(filename)
                moved_to_archive += 1
    
    # Move files to main docs
    for filename in markdown_files_to_docs:
        if os.path.exists(filename):
            target_path = f"docs/{filename}"
            if not os.path.exists(target_path):
                try:
                    shutil.move(filename, target_path)
                    print(f"✅ Moved {filename} to docs/")
                    moved_to_docs += 1
                except Exception as e:
                    print(f"❌ Error moving {filename}: {e}")
            else:
                print(f"⚠️  {filename} already exists in docs/, removing from root")
                os.remove(filename)
                moved_to_docs += 1
    
    # Delete temporary files
    for filename in markdown_files_to_delete:
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"🗑️  Deleted {filename}")
                deleted += 1
            except Exception as e:
                print(f"❌ Error deleting {filename}: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Summary:")
    print(f"  • Moved to docs/ARCHIVE/: {moved_to_archive} files")
    print(f"  • Moved to docs/: {moved_to_docs} files") 
    print(f"  • Deleted: {deleted} files")
    
    # Check what markdown files remain in root
    remaining_md = [f for f in os.listdir('.') if f.endswith('.md') and os.path.isfile(f)]
    
    # Files that should stay in root
    allowed_in_root = ['README.md', 'CHANGELOG.md', 'LICENSE.md']
    unexpected_md = [f for f in remaining_md if f not in allowed_in_root]
    
    if unexpected_md:
        print(f"\n⚠️  Unexpected markdown files still in root:")
        for f in unexpected_md:
            print(f"    • {f}")
        print("   Consider moving these to docs/ or docs/ARCHIVE/")
    else:
        print(f"\n✅ Root directory is clean! Only essential files remain:")
        for f in remaining_md:
            print(f"    • {f}")

if __name__ == "__main__":
    cleanup_markdown_files()