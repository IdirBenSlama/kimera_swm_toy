#!/usr/bin/env python3
"""
Check Python files in root directory
"""
import os

# Get all Python files in root
py_files = [f for f in os.listdir('.') if f.endswith('.py') and os.path.isfile(f)]

# Categorize files
test_files = [f for f in py_files if f.startswith('test_')]
run_files = [f for f in py_files if f.startswith('run_')]
check_files = [f for f in py_files if f.startswith('check_')]
fix_files = [f for f in py_files if f.startswith('fix_')]
verify_files = [f for f in py_files if f.startswith('verify_')]
validate_files = [f for f in py_files if f.startswith('validate_')]
setup_files = [f for f in py_files if f.startswith('setup_')]
demo_files = [f for f in py_files if f.startswith('demo_') or f.endswith('_demo.py')]

print(f"Python files in root directory: {len(py_files)}")
print(f"  • Test files: {len(test_files)}")
print(f"  • Run scripts: {len(run_files)}")
print(f"  • Check scripts: {len(check_files)}")
print(f"  • Fix scripts: {len(fix_files)}")
print(f"  • Verify scripts: {len(verify_files)}")
print(f"  • Validate scripts: {len(validate_files)}")
print(f"  • Setup scripts: {len(setup_files)}")
print(f"  • Demo scripts: {len(demo_files)}")

print(f"\nTotal utility scripts: {len(run_files + check_files + fix_files + verify_files + validate_files + setup_files + demo_files)}")

# Files that should probably stay in root
core_files = [
    'pyproject.toml',
    'poetry.lock', 
    'conftest.py'
]

# Show some examples
if test_files:
    print(f"\nExample test files: {test_files[:5]}")
if run_files:
    print(f"Example run files: {run_files[:5]}")

print(f"\nThese should be moved to scripts/ or tests/ directories")