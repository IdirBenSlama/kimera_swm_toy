#!/usr/bin/env python3
"""
Script to move status and summary files to docs/ARCHIVE/
"""

import shutil
import os
from pathlib import Path

# First, let's check what files actually exist
def check_existing_files():
    """Check which files exist in the current directory"""
    all_files = os.listdir('.')
    md_files = [f for f in all_files if f.endswith('.md')]
    return md_files

# Files to move to docs/ARCHIVE/
status_files = [
    "ISSUES_RESOLVED_SUMMARY.md",
    "KIMERA_SWM_READY.md", 
    "SCAR_FIXES_SUMMARY.md",
    "TEST_SUITE_IMPLEMENTATION_SUMMARY.md",
    "UNICODE_ENCODING_FIX_SUMMARY.md",
    "UNICODE_FIX_COMPLETE.md",
    "VERIFICATION_READY.md",
    "ALL_GREEN_STATUS_CONFIRMED.md",
    "ALL_GREEN_SUMMARY.md",
    "ASYNC_IMPLEMENTATION.md",
    "BOOTSTRAP_CI_FIX_SUMMARY.md",
    "CACHE_FIXES_APPLIED.md",
    "CACHE_IMPLEMENTATION_SUMMARY.md",
    "COMMIT_SUMMARY.md",
    "COMPLETE_TEST_RESULTS.md",
    "FINAL_FIXES_APPLIED.md",
    "FINAL_FIXES_SUMMARY.md",
    "FINAL_PIPELINE_STATUS.md",
    "FINAL_RESOLUTION_SUMMARY.md",
    "FINAL_STABILIZATION_STATUS.md",
    "FINAL_STATUS_SUMMARY.md",
    "FIXES_APPLIED.md",
    "METRICS_IMPLEMENTATION_SUMMARY.md",
    "NEGATION_FIX_IMPLEMENTATION.md",
    "P0_IMPLEMENTATION_SUMMARY.md",
    "PHASE_19_1_COMPLETE.md",
    "PHASE_19_2_COMPLETE.md", 
    "PHASE_19_3_ACTUAL_IMPLEMENTATION.md",
    "PHASE_19_3_COMPLETE.md",
    "PHASE_2_1_SUMMARY.md",
    "PHASE_2_2_SUMMARY.md",
    "PHASE_2_3_SUMMARY.md",
    "PHASE_2_4_SUMMARY.md",
    "RELEASE_v075_SUMMARY.md",
    "RESEARCH_LOOP_COMPLETE.md",
    "STABILIZATION_COMPLETE.md",
    "STABILIZATION_STATUS.md",
    "STABILIZATION_TEST_SUMMARY.md",
    "UNIFIED_IDENTITY_IMPLEMENTATION_SUMMARY.md",
    "V073_FIXES_SUMMARY.md",
    "V07X_STABILIZATION_FIXES_APPLIED.md",
    "VERIFICATION_COMPLETE.md",
    "ZERO_FOG_FIXES_SUMMARY.md",
    "ZETETIC_FIXES_APPLIED.md",
    "ZETETIC_PIPELINE_FIX.md"
]

# Files to move to docs/ (main documentation)
docs_files = [
    "SCAR_IMPLEMENTATION_GUIDE.md",
    "TEST_SUITE_README.md",
    "OPTIMIZATION_ROADMAP.md",
    "EXPERIMENT_COMMANDS.md",
    "MANUAL_FIX_COMMANDS.md",
    "QUICK_FIX_README.md",
    "SECURITY_AND_NEXT_STEPS.md"
]

def move_files():
    """Move files to their appropriate locations"""
    
    # Ensure target directories exist
    os.makedirs("docs/ARCHIVE", exist_ok=True)
    
    # Move status files to archive
    for filename in status_files:
        if os.path.exists(filename):
            try:
                shutil.move(filename, f"docs/ARCHIVE/{filename}")
                print(f"✅ Moved {filename} to docs/ARCHIVE/")
            except Exception as e:
                print(f"❌ Error moving {filename}: {e}")
        else:
            print(f"⚠️  File not found: {filename}")
    
    # Move documentation files to docs/
    for filename in docs_files:
        if os.path.exists(filename):
            try:
                shutil.move(filename, f"docs/{filename}")
                print(f"✅ Moved {filename} to docs/")
            except Exception as e:
                print(f"❌ Error moving {filename}: {e}")
        else:
            print(f"⚠️  File not found: {filename}")

if __name__ == "__main__":
    move_files()
    print("\n🎯 File reorganization complete!")