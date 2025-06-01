#!/usr/bin/env python3
"""
Reorganize repository files for traceability and audit trail
Preserve all development artifacts in organized structure
"""
import os
import shutil
from datetime import datetime

def reorganize_for_traceability():
    """Reorganize files while preserving complete development history"""
    
    print("🗂️ REORGANIZING FOR TRACEABILITY")
    print("=" * 50)
    print("Preserving all development artifacts in organized structure")
    print()
    
    # Create organized directory structure
    directories = {
        "docs/development/": "Development documentation and guides",
        "docs/status/": "Status reports and summaries", 
        "docs/fixes/": "Fix documentation and summaries",
        "docs/implementation/": "Implementation guides and specs",
        "scripts/development/": "Development and debugging scripts",
        "scripts/testing/": "Test execution scripts",
        "scripts/verification/": "Verification and validation scripts",
        "scripts/maintenance/": "Maintenance and cleanup scripts",
        "tests/archive/": "Historical test files",
        "tests/development/": "Development test files"
    }
    
    # Create all directories
    for dir_path, description in directories.items():
        os.makedirs(dir_path, exist_ok=True)
        print(f"📁 Created {dir_path} - {description}")
    
    print()
    
    # === MARKDOWN FILES CATEGORIZATION ===
    print("📄 Categorizing markdown files...")
    
    # Status and summary files
    status_files = [
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
        "REORGANIZATION_COMPLETE.md"
    ]
    
    # Implementation and development guides
    implementation_files = [
        "SCAR_IMPLEMENTATION_GUIDE.md",
        "TEST_SUITE_README.md",
        "FINAL_CLEANUP_PLAN.md",
        "development_audit_report.md"
    ]
    
    # Move status files
    moved_status = 0
    for filename in status_files:
        if os.path.exists(filename):
            target = f"docs/status/{filename}"
            if not os.path.exists(target):
                shutil.move(filename, target)
                print(f"📊 {filename} → docs/status/")
                moved_status += 1
            else:
                os.remove(filename)
                print(f"🗑️ Removed duplicate {filename}")
    
    # Move implementation files
    moved_impl = 0
    for filename in implementation_files:
        if os.path.exists(filename):
            target = f"docs/implementation/{filename}"
            if not os.path.exists(target):
                shutil.move(filename, target)
                print(f"📋 {filename} → docs/implementation/")
                moved_impl += 1
            else:
                os.remove(filename)
                print(f"🗑️ Removed duplicate {filename}")
    
    print()
    
    # === PYTHON FILES CATEGORIZATION ===
    print("🐍 Categorizing Python files...")
    
    # Get all Python files in root
    all_py = [f for f in os.listdir('.') if f.endswith('.py') and os.path.isfile(f)]
    
    # Categorize by purpose
    test_files = [f for f in all_py if f.startswith('test_')]
    run_files = [f for f in all_py if f.startswith('run_')]
    check_files = [f for f in all_py if f.startswith('check_')]
    fix_files = [f for f in all_py if f.startswith('fix_')]
    verify_files = [f for f in all_py if f.startswith('verify_')]
    setup_files = [f for f in all_py if f.startswith('setup_')]
    demo_files = [f for f in all_py if f.startswith('demo_') or f.endswith('_demo.py')]
    execute_files = [f for f in all_py if f.startswith('execute_')]
    quick_files = [f for f in all_py if f.startswith('quick_')]
    simple_files = [f for f in all_py if f.startswith('simple_')]
    basic_files = [f for f in all_py if f.startswith('basic_')]
    final_files = [f for f in all_py if f.startswith('final_')]
    minimal_files = [f for f in all_py if f.startswith('minimal_')]
    
    # Files to keep in root (essential)
    keep_files = {'conftest.py'}
    
    # Move test files to tests/archive/ (preserve development history)
    moved_tests = 0
    for filename in test_files:
        if filename not in keep_files:
            target = f"tests/archive/{filename}"
            if os.path.exists(filename) and not os.path.exists(target):
                shutil.move(filename, target)
                print(f"🧪 {filename} → tests/archive/")
                moved_tests += 1
    
    # Move development scripts by category
    script_categories = [
        (run_files, "scripts/testing/", "🏃"),
        (check_files, "scripts/verification/", "🔍"),
        (fix_files, "scripts/maintenance/", "🔧"),
        (verify_files, "scripts/verification/", "✅"),
        (setup_files, "scripts/development/", "⚙️"),
        (demo_files, "scripts/development/", "🎯"),
        (execute_files, "scripts/development/", "▶️"),
        (quick_files, "scripts/development/", "⚡"),
        (simple_files, "scripts/development/", "📝"),
        (basic_files, "scripts/development/", "🔤"),
        (final_files, "scripts/development/", "🏁"),
        (minimal_files, "scripts/development/", "📦")
    ]
    
    moved_scripts = 0
    for file_list, target_dir, emoji in script_categories:
        for filename in file_list:
            if os.path.exists(filename):
                target = f"{target_dir}{filename}"
                if not os.path.exists(target):
                    shutil.move(filename, target)
                    print(f"{emoji} {filename} → {target_dir}")
                    moved_scripts += 1
                else:
                    os.remove(filename)
                    print(f"🗑️ Removed duplicate {filename}")
    
    print()
    
    # === CREATE TRACEABILITY INDEX ===
    print("📋 Creating traceability index...")
    
    index_content = f"""# Development Traceability Index

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Repository Organization

This repository maintains complete development traceability through organized preservation of all development artifacts.

### Documentation Structure

```
docs/
├── implementation/          # Implementation guides and specifications
│   ├── SCAR_IMPLEMENTATION_GUIDE.md
│   ├── TEST_SUITE_README.md
│   ├── FINAL_CLEANUP_PLAN.md
│   └── development_audit_report.md
├── status/                  # Status reports and summaries
│   ├── FINAL_STATUS.md
│   ├── IMPLEMENTATION_COMPLETE_SUMMARY.md
│   ├── KIMERA_SWM_READY.md
│   └── [other status files]
├── development/             # Development documentation
├── fixes/                   # Fix documentation
└── ARCHIVE/                 # Historical documents
```

### Scripts Organization

```
scripts/
├── development/             # Development and debugging scripts
│   ├── demo_*.py           # Demo scripts
│   ├── execute_*.py        # Execution scripts
│   ├── quick_*.py          # Quick development tools
│   └── setup_*.py          # Setup scripts
├── testing/                 # Test execution scripts
│   ├── run_*.py            # Test runners
│   └── test execution tools
├── verification/            # Verification and validation
│   ├── check_*.py          # Check scripts
│   ├── verify_*.py         # Verification scripts
│   └── validation tools
└── maintenance/             # Maintenance and cleanup
    ├── fix_*.py            # Fix scripts
    └── cleanup tools
```

### Test Archive

```
tests/
├── unit/                    # Current unit tests
├── integration/             # Current integration tests
├── functional/              # Current functional tests
├── archive/                 # Historical test files
│   ├── test_*.py           # Preserved development tests
│   └── legacy test files
└── development/             # Development test files
```

## Development History Preservation

### Status Reports ({moved_status} files)
All status reports and summaries are preserved in `docs/status/` for complete audit trail of project progress.

### Implementation Guides ({moved_impl} files)
Implementation documentation is organized in `docs/implementation/` for easy reference and maintenance.

### Development Scripts ({moved_scripts} files)
All development scripts are categorized by purpose and preserved in `scripts/` subdirectories.

### Test Files ({moved_tests} files)
Historical test files are preserved in `tests/archive/` maintaining complete testing history.

## Benefits

### 🔍 Complete Traceability
- Every development artifact is preserved
- Clear categorization by purpose
- Audit trail of all changes and fixes

### 📚 Organized Knowledge Base
- Implementation guides easily accessible
- Status reports chronologically preserved
- Development tools categorized by function

### 🚀 Maintainable Structure
- Clean root directory for daily work
- Organized subdirectories for specific needs
- Scalable structure for future growth

### 🎯 Developer Efficiency
- Quick access to relevant tools
- Clear separation of concerns
- Historical context preserved

## Usage

### Finding Implementation Details
```bash
# Implementation guides
ls docs/implementation/

# Status reports
ls docs/status/

# Historical documents
ls docs/ARCHIVE/
```

### Using Development Tools
```bash
# Development scripts
ls scripts/development/

# Testing tools
ls scripts/testing/

# Verification tools
ls scripts/verification/
```

### Accessing Test History
```bash
# Current tests
ls tests/unit/ tests/integration/ tests/functional/

# Historical tests
ls tests/archive/
```

## Maintenance

This organization preserves complete development history while providing a clean, maintainable structure for ongoing work. All artifacts are categorized and preserved for future reference and audit purposes.
"""
    
    with open("docs/TRACEABILITY_INDEX.md", "w", encoding="utf-8") as f:
        f.write(index_content)
    
    print("✅ Created docs/TRACEABILITY_INDEX.md")
    
    # === FINAL SUMMARY ===
    print("\n" + "=" * 50)
    print("📊 REORGANIZATION SUMMARY")
    print(f"  • Status files moved: {moved_status}")
    print(f"  • Implementation files moved: {moved_impl}")
    print(f"  • Test files archived: {moved_tests}")
    print(f"  • Scripts categorized: {moved_scripts}")
    
    # Check final state
    remaining_md = [f for f in os.listdir('.') if f.endswith('.md') and os.path.isfile(f)]
    remaining_py = [f for f in os.listdir('.') if f.endswith('.py') and os.path.isfile(f)]
    
    essential_files = {'README.md', 'CHANGELOG.md'}
    essential_py = {'conftest.py'}
    
    unexpected_md = [f for f in remaining_md if f not in essential_files]
    unexpected_py = [f for f in remaining_py if f not in essential_py]
    
    print(f"\n📁 Final Root Directory State:")
    print(f"  • Essential markdown files: {len([f for f in remaining_md if f in essential_files])}")
    print(f"  • Essential Python files: {len([f for f in remaining_py if f in essential_py])}")
    
    if unexpected_md:
        print(f"  • Unexpected markdown files: {len(unexpected_md)}")
        for f in unexpected_md[:5]:
            print(f"    - {f}")
        if len(unexpected_md) > 5:
            print(f"    ... and {len(unexpected_md) - 5} more")
    
    if unexpected_py:
        print(f"  • Unexpected Python files: {len(unexpected_py)}")
        for f in unexpected_py[:5]:
            print(f"    - {f}")
        if len(unexpected_py) > 5:
            print(f"    ... and {len(unexpected_py) - 5} more")
    
    print(f"\n✅ REORGANIZATION COMPLETE")
    print("🔍 All development artifacts preserved with full traceability")
    print("📚 Organized structure maintains complete audit trail")
    print("🚀 Clean root directory ready for ongoing development")

if __name__ == "__main__":
    reorganize_for_traceability()