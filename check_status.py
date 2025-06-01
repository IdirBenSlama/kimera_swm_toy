#!/usr/bin/env python3
"""
Quick status check for P0 verification
"""

import sys
import os
from pathlib import Path

def check_files():
    """Check if all required files exist"""
    print("📁 Checking file structure...")
    
    required_files = [
        "src/kimera/__init__.py",
        "src/kimera/storage.py", 
        "src/kimera/identity.py",
        "src/kimera/echoform.py",
        "src/kimera/geoid.py",
        "conftest.py",
        ".github/workflows/ci.yml"
    ]
    
    missing = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing:
        print(f"\n❌ Missing files:")
        for file_path in missing:
            print(f"   - {file_path}")
        return False
    
    print("✅ All required files present")
    return True

def check_imports():
    """Check if basic imports work"""
    print("\n🔍 Checking basic imports...")
    
    # Add src to path
    sys.path.insert(0, str(Path(__file__).parent / "src"))
    
    imports_to_test = [
        ("kimera", "Core package"),
        ("kimera.storage", "Storage module"),
        ("kimera.identity", "Identity module"),
        ("kimera.echoform", "EchoForm module"),
        ("kimera.geoid", "Geoid module"),
    ]
    
    failed_imports = []
    
    for module_name, description in imports_to_test:
        try:
            __import__(module_name)
            print(f"✅ {module_name} - {description}")
        except Exception as e:
            print(f"❌ {module_name} - {description}: {e}")
            failed_imports.append((module_name, str(e)))
    
    if failed_imports:
        print(f"\n❌ Failed imports:")
        for module_name, error in failed_imports:
            print(f"   - {module_name}: {error}")
        return False
    
    print("✅ All basic imports successful")
    return True

def check_dependencies():
    """Check if required dependencies are available"""
    print("\n📦 Checking dependencies...")
    
    dependencies = [
        ("duckdb", "Database backend"),
        ("numpy", "Numerical operations"),
        ("pathlib", "Path operations"),
    ]
    
    missing_deps = []
    
    for dep_name, description in dependencies:
        try:
            __import__(dep_name)
            print(f"✅ {dep_name} - {description}")
        except ImportError:
            print(f"❌ {dep_name} - {description}: Not installed")
            missing_deps.append(dep_name)
    
    if missing_deps:
        print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
        return False
    
    print("✅ All dependencies available")
    return True

def main():
    """Run status check"""
    print("🔍 P0 Status Check")
    print("=" * 40)
    
    checks = [
        ("File Structure", check_files),
        ("Dependencies", check_dependencies), 
        ("Basic Imports", check_imports),
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} check crashed: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Status Check Summary")
    print("=" * 40)
    
    passed = 0
    total = len(results)
    
    for check_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {check_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 System ready for testing!")
        return 0
    else:
        print("⚠️  System has issues that need to be resolved.")
        return 1

if __name__ == "__main__":
    sys.exit(main())