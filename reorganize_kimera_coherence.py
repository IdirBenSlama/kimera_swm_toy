#!/usr/bin/env python3
"""
Comprehensive Kimera SWM Repository Reorganization Script
Implements the coherence check recommendations from the analysis.
"""

import os
import shutil
import glob
from pathlib import Path

def safe_move(src, dst):
    """Safely move a file, creating destination directory if needed."""
    dst_path = Path(dst)
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    
    if Path(src).exists():
        if dst_path.exists():
            print(f"Warning: {dst} already exists, skipping {src}")
            return False
        shutil.move(src, dst)
        print(f"Moved: {src} -> {dst}")
        return True
    else:
        print(f"Warning: {src} does not exist")
        return False

def reorganize_documentation():
    """Reorganize documentation according to the coherence plan."""
    print("=== Reorganizing Documentation ===")
    
    # Move guides to docs/guides/
    guides_to_move = [
        ("SCAR_IMPLEMENTATION_GUIDE.md", "docs/guides/scar_guide.md"),
        ("docs/SCAR_IMPLEMENTATION_GUIDE.md", "docs/guides/scar_guide.md"),
        ("docs/echoform_params.md", "docs/guides/echoform_guide.md"),
        ("BENCHMARK_FEATURES.md", "docs/guides/benchmark_guide.md"),
        ("METRICS_IMPLEMENTATION_SUMMARY.md", "docs/guides/metrics_guide.md"),
    ]
    
    for src, dst in guides_to_move:
        safe_move(src, dst)
    
    # Move status files to docs/status/ (many are already there)
    status_files = [
        "ALL_GREEN_STATUS_CONFIRMED.md",
        "ALL_GREEN_SUMMARY.md", 
        "FINAL_STATUS.md",
        "FINAL_STATUS_SUMMARY.md",
        "IMPLEMENTATION_COMPLETE_SUMMARY.md",
        "IMPORT_FIXES_COMPLETE.md",
        "ISSUES_RESOLVED_SUMMARY.md",
        "KIMERA_SWM_READY.md",
        "P0_STATUS_SUMMARY.md",
        "SCAR_FIXES_SUMMARY.md",
        "UNICODE_FIX_COMPLETE.md",
        "VERIFICATION_READY.md",
        "STABILIZATION_COMPLETE.md",
        "REORGANIZATION_COMPLETE.md",
    ]
    
    for status_file in status_files:
        if os.path.exists(status_file):
            safe_move(status_file, f"docs/status/{status_file}")

def reorganize_scripts():
    """Move ad-hoc scripts to scripts/ directory."""
    print("=== Reorganizing Scripts ===")
    
    # Scripts to move to scripts/
    scripts_to_move = [
        "fix_critical_issues.py",
        "fix_all_issues.py", 
        "fix_dependencies.py",
        "fix_import_paths.py",
        "fix_poetry_lock.py",
        "fix_unicode_encoding.py",
        "cleanup_workflows.py",
        "organize_scripts.py",
        "bulk_reorganization.py",
        "execute_complete_reorganization.py",
        "execute_final_cleanup.py",
        "execute_fix.py",
        "execute_markdown_cleanup.py",
        "execute_reorganization_now.py",
        "execute_traceability_reorganization.py",
        "execute_verification.py",
        "migrate_to_echo_form.py",
    ]
    
    for script in scripts_to_move:
        if os.path.exists(script):
            safe_move(script, f"scripts/{script}")

def reorganize_tests():
    """Reorganize tests into unit/integration/functional structure."""
    print("=== Reorganizing Tests ===")
    
    # Unit tests (pure unit tests, no external dependencies)
    unit_tests = [
        "test_unified_identity.py",
        "tests/test_geoid.py", 
        "test_basic_functionality.py",
        "simple_identity_test.py",
        "simple_test.py",
    ]
    
    # Integration tests (multiple components working together)
    integration_tests = [
        "test_scar_functionality.py",
        "test_storage_metrics.py", 
        "test_vault_and_scar.py",
        "test_metrics_integration.py",
        "test_p0_integration.py",
        "test_mixed_workflow.py",
    ]
    
    # Functional tests (end-to-end, benchmarks, full system tests)
    functional_tests = [
        "test_benchmark_quick.py",
        "test_reactor_mp.py",
        "test_v073_storage.py",
        "test_v075_final.py",
        "test_streaming_benchmark.py",
        "test_performance_comparison.py",
        "tests/test_reactor_mp.py",
    ]
    
    # Move unit tests
    for test in unit_tests:
        if os.path.exists(test):
            basename = os.path.basename(test)
            safe_move(test, f"tests/unit/{basename}")
    
    # Move integration tests  
    for test in integration_tests:
        if os.path.exists(test):
            basename = os.path.basename(test)
            safe_move(test, f"tests/integration/{basename}")
    
    # Move functional tests
    for test in functional_tests:
        if os.path.exists(test):
            basename = os.path.basename(test)
            safe_move(test, f"tests/functional/{basename}")

def clean_root_directory():
    """Remove obsolete files from root directory."""
    print("=== Cleaning Root Directory ===")
    
    # Files to remove (obsolete run_* scripts)
    obsolete_files = [
        "run_all_tests.py",
        "run_all_verifications.py", 
        "run_baseline_benchmark.py",
        "run_baseline_experiment.py",
        "run_basic_p0.py",
        "run_cache_tests.py",
        "run_cleanup.py",
        "run_clean_tests.py",
        "run_complete_p0_suite.py",
        "run_complete_reorganization.py",
        "run_complete_test_suite.py",
        "run_complete_verification.py",
        "run_comprehensive_fix.py",
        "run_comprehensive_test.py",
        "run_echoform_tests.py",
        "run_final_summary.py",
        "run_final_test.py",
        "run_fix.py",
        "run_focus_tests.py",
        "run_full_validation.py",
        "run_import_test.py",
        "run_metrics_tests.py",
        "run_migration_test.py",
        "run_mixed_benchmark.py",
        "run_mixed_generation.py",
        "run_negation_benchmark.py",
        "run_negation_test.py",
        "run_p0_tests.py",
        "run_phase_192_tests.py",
        "run_pytest_tests.py",
        "run_quick_status.py",
        "run_quick_test.py",
        "run_quick_validation.py",
        "run_quick_verification.py",
        "run_scar_test.py",
        "run_simple_identity_test.py",
        "run_simple_p0.py",
        "run_simple_validation.py",
        "run_status_check.py",
        "run_tests.py",
        "run_test_now.py",
        "run_test_suite.py",
        "run_test_unified_identity.py",
        "run_traceability_reorganization.py",
        "run_unicode_test.py",
        "run_validation.py",
        "run_validation_test.py",
        "run_verification.py",
        "run_verification_now.py",
        "run_verification_suite.py",
    ]
    
    for file in obsolete_files:
        if os.path.exists(file):
            print(f"Removing obsolete file: {file}")
            os.remove(file)

def create_makefile():
    """Create a Makefile to replace all the run_* scripts."""
    print("=== Creating Makefile ===")
    
    makefile_content = """# Kimera SWM Makefile
# Replaces the numerous run_* scripts with a single entry point

.PHONY: help install lint test test-unit test-integration test-functional format clean

help:
	@echo "Kimera SWM Development Commands:"
	@echo "  install     - Install dependencies"
	@echo "  lint        - Run linting (ruff)"
	@echo "  test        - Run all tests"
	@echo "  test-unit   - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  test-functional  - Run functional tests only"
	@echo "  format      - Format code (black)"
	@echo "  clean       - Clean cache and temp files"

install:
	poetry install --with dev

lint:
	ruff check src tests scripts
	ruff format --check src tests scripts

test:
	pytest -v

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

test-functional:
	pytest tests/functional/ -v

format:
	ruff format src tests scripts
	black src tests scripts

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf _nocache_temp
	rm -f *.db
"""
    
    with open("Makefile", "w") as f:
        f.write(makefile_content)
    print("Created Makefile")

def update_pyproject_toml():
    """Update pyproject.toml with proper extras and dependencies."""
    print("=== Updating pyproject.toml ===")
    
    # Read current content
    with open("pyproject.toml", "r") as f:
        content = f.read()
    
    # Add extras section if not present
    if "[tool.poetry.group.dev.dependencies]" not in content:
        extras_section = """
[tool.poetry.group.dev.dependencies]
ruff = "^0.1.0"
black = "^23.0"
pytest-cov = "^4.0"

[tool.poetry.group.benchmarks.dependencies]
matplotlib = "^3.7"
pandas = "^2.0"
"""
        # Insert before [tool.pytest.ini_options]
        content = content.replace("[tool.pytest.ini_options]", extras_section + "\n[tool.pytest.ini_options]")
        
        with open("pyproject.toml", "w") as f:
            f.write(content)
        print("Updated pyproject.toml with dev and benchmark extras")

def main():
    """Execute the full reorganization."""
    print("Starting Kimera SWM Repository Reorganization...")
    print("This implements the coherence check recommendations.")
    print()
    
    reorganize_documentation()
    print()
    
    reorganize_scripts() 
    print()
    
    reorganize_tests()
    print()
    
    clean_root_directory()
    print()
    
    create_makefile()
    print()
    
    update_pyproject_toml()
    print()
    
    print("=== Reorganization Complete ===")
    print("Next steps:")
    print("1. Run 'make test' to verify all tests still pass")
    print("2. Run 'make lint' to check code quality")
    print("3. Update any remaining import paths in moved files")
    print("4. Review and commit the changes")

if __name__ == "__main__":
    main()