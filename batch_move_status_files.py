#!/usr/bin/env python3
"""
Batch move all status/summary markdown files to archive
"""
import os
import shutil

# Status and summary files to move to archive
status_files = [
    "ALL_GREEN_STATUS_CONFIRMED.md",
    "ALL_GREEN_SUMMARY.md", 
    "BENCHMARK_FEATURES.md",
    "BOOTSTRAP_CI_FIX_SUMMARY.md",
    "CACHE_FIXES_APPLIED.md",
    "CACHE_IMPLEMENTATION_SUMMARY.md",
    "COMMIT_SUMMARY.md",
    "COMPLETE_TEST_RESULTS.md",
    "EXPERIMENT_COMMANDS.md",
    "FINAL_FIXES_APPLIED.md",
    "FINAL_FIXES_SUMMARY.md",
    "FINAL_PIPELINE_STATUS.md",
    "FINAL_RESOLUTION_SUMMARY.md",
    "FINAL_STABILIZATION_STATUS.md",
    "FINAL_STATUS.md",
    "FINAL_STATUS_SUMMARY.md",
    "FIXES_APPLIED.md",
    "IMPLEMENTATION_COMPLETE_SUMMARY.md",
    "IMPORT_FIXES_COMPLETE.md",
    "ISSUES_RESOLVED_SUMMARY.md",
    "KIMERA_SWM_READY.md",
    "MANUAL_FIX_COMMANDS.md",
    "METRICS_IMPLEMENTATION_SUMMARY.md",
    "NEGATION_FIX_IMPLEMENTATION.md",
    "OPTIMIZATION_ROADMAP.md",
    "P0_IMPLEMENTATION_SUMMARY.md",
    "P0_STATUS_SUMMARY.md",
    "PHASE_19_1_COMPLETE.md",
    "PHASE_19_2_COMPLETE.md",
    "PHASE_19_3_ACTUAL_IMPLEMENTATION.md",
    "PHASE_19_3_COMPLETE.md",
    "PHASE_2_1_SUMMARY.md",
    "PHASE_2_2_SUMMARY.md",
    "PHASE_2_3_SUMMARY.md",
    "PHASE_2_4_SUMMARY.md",
    "QUICK_FIX_README.md",
    "RELEASE_v075_SUMMARY.md",
    "REORGANIZATION_COMPLETE.md",
    "RESEARCH_LOOP_COMPLETE.md",
    "SCAR_FIXES_SUMMARY.md",
    "SECURITY_AND_NEXT_STEPS.md",
    "STABILIZATION_COMPLETE.md",
    "STABILIZATION_STATUS.md",
    "STABILIZATION_TEST_SUMMARY.md",
    "TEST_SUITE_IMPLEMENTATION_SUMMARY.md",
    "UNICODE_ENCODING_FIX_SUMMARY.md",
    "UNICODE_FIX_COMPLETE.md",
    "UNIFIED_IDENTITY_IMPLEMENTATION_SUMMARY.md",
    "V073_FIXES_SUMMARY.md",
    "V07X_STABILIZATION_FIXES_APPLIED.md",
    "VERIFICATION_COMPLETE.md",
    "VERIFICATION_READY.md",
    "ZERO_FOG_FIXES_SUMMARY.md",
    "ZETETIC_FIXES_APPLIED.md",
    "ZETETIC_PIPELINE_FIX.md",
    "development_audit_report.md",
    "summary_report.md"
]

# Implementation files to move to docs/
implementation_files = [
    "ASYNC_IMPLEMENTATION.md"
]

# Ensure directories exist
os.makedirs("docs/ARCHIVE", exist_ok=True)

moved_count = 0
print("Moving status files to archive...")

# Move status files to archive
for filename in status_files:
    if os.path.exists(filename):
        target = f"docs/ARCHIVE/{filename}"
        if not os.path.exists(target):
            try:
                shutil.move(filename, target)
                print(f"✅ {filename}")
                moved_count += 1
            except Exception as e:
                print(f"❌ Error moving {filename}: {e}")
        else:
            # File already exists in archive, just remove from root
            os.remove(filename)
            print(f"🗑️ Removed duplicate {filename}")
            moved_count += 1

# Move implementation files to docs/
for filename in implementation_files:
    if os.path.exists(filename):
        target = f"docs/{filename}"
        if not os.path.exists(target):
            try:
                shutil.move(filename, target)
                print(f"📄 {filename} → docs/")
            except Exception as e:
                print(f"❌ Error moving {filename}: {e}")
        else:
            os.remove(filename)
            print(f"🗑️ Removed duplicate {filename}")

print(f"\n✅ Moved {moved_count} files to archive")

# Check remaining markdown files
remaining = [f for f in os.listdir('.') if f.endswith('.md') and os.path.isfile(f)]
keep_files = ['README.md', 'CHANGELOG.md']
unexpected = [f for f in remaining if f not in keep_files]

if unexpected:
    print(f"\n⚠️ Remaining markdown files in root:")
    for f in unexpected:
        print(f"  • {f}")
else:
    print(f"\n✅ Root directory clean! Only essential files remain: {remaining}")