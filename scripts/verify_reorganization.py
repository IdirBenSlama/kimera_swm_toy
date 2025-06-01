#!/usr/bin/env python3
"""
Verify the repository reorganization is complete and working
"""
import os
import sys
import subprocess

def check_directory_structure():
    """Verify the expected directory structure exists"""
    print("📁 Checking directory structure...")
    
    required_dirs = [
        "src/kimera",
        "tests/unit",
        "tests/integration", 
        "tests/functional",
        "docs",
        "docs/ARCHIVE",
        "scripts",
        ".github/workflows"
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
        else:
            print(f"✅ {dir_path}")
    
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
    
    print("✅ All required directories exist")
    return True

def check_key_files():
    """Verify key files are in the right places"""
    print("\n📄 Checking key files...")
    
    key_files = [
        "README.md",
        "pyproject.toml",
        "src/kimera/__init__.py",
        "src/kimera/identity.py",
        "src/kimera/storage.py",
        "tests/conftest.py",
        "tests/unit/test_identity.py",
        "tests/unit/test_storage.py",
        "tests/integration/test_scar_functionality.py",
        "docs/SCAR_IMPLEMENTATION_GUIDE.md",
        "docs/TEST_SUITE_README.md",
        "scripts/verify_scar_implementation.py",
        ".github/workflows/ci.yml"
    ]
    
    missing_files = []
    for file_path in key_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All key files exist")
    return True

def check_imports():
    """Verify imports work correctly"""
    print("\n🔍 Checking imports...")
    
    try:
        sys.path.insert(0, 'src')
        
        from kimera.identity import Identity
        print("✅ kimera.identity import successful")
        
        from kimera.storage import LatticeStorage
        print("✅ kimera.storage import successful")
        
        from kimera.cls import CLS
        print("✅ kimera.cls import successful")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def check_test_structure():
    """Verify test files are properly organized"""
    print("\n🧪 Checking test organization...")
    
    # Check unit tests
    unit_tests = [f for f in os.listdir("tests/unit") if f.endswith(".py")]
    print(f"✅ Unit tests: {len(unit_tests)} files")
    
    # Check integration tests  
    integration_tests = [f for f in os.listdir("tests/integration") if f.endswith(".py")]
    print(f"✅ Integration tests: {len(integration_tests)} files")
    
    # Check functional tests
    functional_dir = "tests/functional"
    if os.path.exists(functional_dir):
        functional_tests = [f for f in os.listdir(functional_dir) if f.endswith(".py")]
        print(f"✅ Functional tests: {len(functional_tests)} files")
    else:
        print("⚠️  Functional tests directory empty")
    
    return True

def check_documentation():
    """Verify documentation is properly organized"""
    print("\n📚 Checking documentation...")
    
    # Check main docs
    docs_files = [f for f in os.listdir("docs") if f.endswith(".md")]
    print(f"✅ Main docs: {len(docs_files)} files")
    
    # Check archived docs
    if os.path.exists("docs/ARCHIVE"):
        archive_files = [f for f in os.listdir("docs/ARCHIVE") if f.endswith(".md")]
        print(f"✅ Archived docs: {len(archive_files)} files")
    
    return True

def check_scripts():
    """Verify scripts are properly organized"""
    print("\n🔧 Checking scripts...")
    
    script_files = [f for f in os.listdir("scripts") if f.endswith(".py")]
    print(f"✅ Scripts: {len(script_files)} files")
    
    # Check for key scripts
    key_scripts = [
        "verify_scar_implementation.py",
        "cleanup_workflows.py",
        "reorganize_repository.py"
    ]
    
    for script in key_scripts:
        if os.path.exists(f"scripts/{script}"):
            print(f"✅ {script}")
        else:
            print(f"⚠️  Missing script: {script}")
    
    return True

def run_basic_tests():
    """Run basic tests to verify functionality"""
    print("\n🧪 Running basic tests...")
    
    try:
        # Try to run pytest on the unit tests
        result = subprocess.run(
            ["python", "-m", "pytest", "tests/unit/", "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✅ Unit tests passed")
            return True
        else:
            print(f"❌ Unit tests failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("⚠️  Tests timed out")
        return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def check_root_cleanliness():
    """Verify root directory is clean"""
    print("\n🧹 Checking root directory cleanliness...")
    
    root_files = os.listdir(".")
    
    # Files that should be in root
    allowed_root_files = {
        "README.md",
        "pyproject.toml", 
        "poetry.lock",
        "CHANGELOG.md",
        ".gitignore",
        ".codespellrc",
        "LICENSE"
    }
    
    # Directories that should be in root
    allowed_root_dirs = {
        "src",
        "tests", 
        "docs",
        "scripts",
        "vault",
        "benchmarks",
        "examples",
        "data",
        "static",
        "tools",
        ".github",
        ".vscode",
        "__pycache__",
        "_nocache_temp"
    }
    
    unexpected_files = []
    for item in root_files:
        if os.path.isfile(item) and item not in allowed_root_files:
            # Allow some temporary files
            if not (item.endswith('.db') or item.endswith('.csv') or 
                   item.endswith('.png') or item.endswith('.json') or
                   item.endswith('.yaml') or item.endswith('.yml') or
                   item.endswith('.ps1') or item.endswith('.bat') or
                   item.startswith('.')):
                unexpected_files.append(item)
        elif os.path.isdir(item) and item not in allowed_root_dirs:
            unexpected_files.append(f"{item}/")
    
    if unexpected_files:
        print(f"⚠️  Unexpected files in root: {unexpected_files}")
        print("   Consider moving these to appropriate directories")
    else:
        print("✅ Root directory is clean")
    
    return len(unexpected_files) == 0

def main():
    """Run all verification checks"""
    print("🚀 Verifying repository reorganization...")
    print("=" * 60)
    
    checks = [
        ("Directory Structure", check_directory_structure),
        ("Key Files", check_key_files),
        ("Imports", check_imports),
        ("Test Organization", check_test_structure),
        ("Documentation", check_documentation),
        ("Scripts", check_scripts),
        ("Root Cleanliness", check_root_cleanliness),
        ("Basic Tests", run_basic_tests)
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, check_func in checks:
        print(f"\n🔍 {check_name}...")
        try:
            if check_func():
                passed += 1
            else:
                print(f"❌ {check_name} failed")
        except Exception as e:
            print(f"❌ {check_name} error: {e}")
    
    print("\n" + "=" * 60)
    print(f"🎯 Verification Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("✅ Repository reorganization successful!")
        print("\n📋 Ready for:")
        print("  • Development work")
        print("  • CI/CD pipeline")
        print("  • Production deployment")
        return True
    else:
        print("❌ Some verification checks failed")
        print("   Please address the issues above")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)