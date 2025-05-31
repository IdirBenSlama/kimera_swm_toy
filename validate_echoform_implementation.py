#!/usr/bin/env python3
"""
Comprehensive validation of EchoForm v0.7.1 implementation
Validates all deliverables from Phase 19.1
"""
import subprocess
import sys
from pathlib import Path


def validate_file_exists(filepath, description):
    """Validate that a file exists"""
    path = Path(filepath)
    if path.exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} missing: {filepath}")
        return False


def run_test_file(filepath):
    """Run a test file and return success status"""
    try:
        result = subprocess.run([sys.executable, filepath], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f"✅ {filepath} - All tests passed")
            return True
        else:
            print(f"❌ {filepath} - Tests failed")
            print("STDERR:", result.stderr[-200:])  # Last 200 chars of error
            return False
    except subprocess.TimeoutExpired:
        print(f"⏰ {filepath} - Timed out")
        return False
    except Exception as e:
        print(f"💥 {filepath} - Error: {e}")
        return False


def validate_imports():
    """Validate that all modules can be imported"""
    print("\n🔍 Validating imports...")
    
    try:
        sys.path.insert(0, 'src')
        
        # Test EchoForm import
        from kimera.echoform import EchoForm
        print("✅ EchoForm import successful")
        
        # Test CLS import
        from kimera.cls import lattice_resolve, create_lattice_form
        print("✅ CLS module import successful")
        
        # Test basic functionality
        echo = EchoForm(anchor="test")
        assert echo.anchor == "test"
        assert echo.intensity_sum() == 0.0
        print("✅ EchoForm basic functionality works")
        
        return True
        
    except Exception as e:
        print(f"❌ Import validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_parameters():
    """Validate parameter documentation"""
    print("\n📋 Validating parameter documentation...")
    
    param_file = Path("docs/P-KGM05.md")
    if not param_file.exists():
        print("❌ Parameter documentation missing")
        return False
    
    content = param_file.read_text()
    
    # Check for required parameters
    required_params = [
        "extra_domains: []",
        "topology_backend: json", 
        "trace_signature: sha256"
    ]
    
    all_found = True
    for param in required_params:
        if param in content:
            print(f"✅ Parameter documented: {param}")
        else:
            print(f"❌ Parameter missing: {param}")
            all_found = False
    
    return all_found


def main():
    """Run comprehensive validation"""
    print("🔍 EchoForm v0.7.1 Implementation Validation")
    print("=" * 50)
    
    # Track validation results
    validations = []
    
    # 1. File existence validation
    print("\n📁 Validating file deliverables...")
    files_to_check = [
        ("docs/P-KGM05.md", "Parameter documentation"),
        ("src/kimera/echoform.py", "EchoForm core class"),
        ("src/kimera/cls.py", "CLS lattice integration"),
        ("tests/test_echoform_core.py", "EchoForm unit tests"),
        ("tests/test_echoform_flow.py", "EchoForm smoke tests"),
        ("tests/test_cls_integration.py", "CLS integration tests"),
        ("examples/echoform_playground.py", "Interactive playground")
    ]
    
    file_validation = all(validate_file_exists(filepath, desc) for filepath, desc in files_to_check)
    validations.append(("File deliverables", file_validation))
    
    # 2. Parameter validation
    param_validation = validate_parameters()
    validations.append(("Parameter documentation", param_validation))
    
    # 3. Import validation
    import_validation = validate_imports()
    validations.append(("Module imports", import_validation))
    
    # 4. Test execution validation
    print("\n🧪 Running test suites...")
    test_files = [
        "tests/test_echoform_core.py",
        "tests/test_echoform_flow.py", 
        "tests/test_cls_integration.py"
    ]
    
    test_results = [run_test_file(test_file) for test_file in test_files]
    test_validation = all(test_results)
    validations.append(("Test execution", test_validation))
    
    # 5. Playground validation
    print("\n🎮 Validating playground...")
    playground_validation = run_test_file("examples/echoform_playground.py")
    validations.append(("Playground demo", playground_validation))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(validations)
    
    for name, result in validations:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} validations passed")
    
    if passed == total:
        print("\n🎉 ALL VALIDATIONS PASSED!")
        print("EchoForm v0.7.1 implementation is complete and ready for use.")
        print("\nNext steps:")
        print("1. Commit changes: git add . && git commit -m 'Phase 19.1: EchoForm core implementation'")
        print("2. Run benchmarks to test integration")
        print("3. Proceed to Phase 19.2 for advanced features")
        return 0
    else:
        print(f"\n❌ {total - passed} validations failed.")
        print("Please fix the issues above before proceeding.")
        return 1


if __name__ == "__main__":
    sys.exit(main())