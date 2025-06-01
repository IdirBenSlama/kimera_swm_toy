#!/usr/bin/env python3
"""
Comprehensive Test Suite for Kimera SWM Toy Repository
=====================================================

This test suite provides systematic testing for the Kimera project,
addressing the real issues found in the repository while ignoring
phantom errors and non-critical warnings.
"""

import sys
import os
import subprocess
import traceback
import tempfile
from pathlib import Path
from datetime import datetime
import importlib.util


class TestSuite:
    """Main test suite coordinator."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.results = []
        
    def run_test(self, test_name, test_func):
        """Run a single test and record results."""
        print(f"\n🧪 Running: {test_name}")
        print("=" * 60)
        
        try:
            result = test_func()
            if result:
                print(f"✅ PASSED: {test_name}")
                self.passed += 1
                self.results.append(("PASS", test_name, None))
            else:
                print(f"❌ FAILED: {test_name}")
                self.failed += 1
                self.results.append(("FAIL", test_name, "Test returned False"))
        except Exception as e:
            print(f"💥 ERROR: {test_name}")
            print(f"   Error: {str(e)}")
            print(f"   Traceback: {traceback.format_exc()}")
            self.failed += 1
            self.results.append(("ERROR", test_name, str(e)))
    
    def skip_test(self, test_name, reason):
        """Skip a test with a reason."""
        print(f"\n⏭️  SKIPPED: {test_name}")
        print(f"   Reason: {reason}")
        self.skipped += 1
        self.results.append(("SKIP", test_name, reason))
    
    def print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 80)
        print("[TARGET] TEST SUITE SUMMARY")
        print("=" * 80)
        print(f"✅ Passed:  {self.passed}")
        print(f"❌ Failed:  {self.failed}")
        print(f"⏭️  Skipped: {self.skipped}")
        print(f"📊 Total:   {self.passed + self.failed + self.skipped}")
        
        if self.failed > 0:
            print("\n❌ FAILED TESTS:")
            for status, name, error in self.results:
                if status in ["FAIL", "ERROR"]:
                    print(f"   • {name}: {error}")
        
        print("\n🎉 SUCCESS RATE: {:.1f}%".format(
            (self.passed / (self.passed + self.failed) * 100) if (self.passed + self.failed) > 0 else 100
        ))


class ImportTests:
    """Test import functionality."""
    
    @staticmethod
    def test_basic_imports():
        """Test basic Python imports work."""
        try:
            import sys
            import os
            import subprocess
            import tempfile
            from pathlib import Path
            from datetime import datetime
            print("[OK] Basic Python imports successful")
            return True
        except ImportError as e:
            print(f"[FAIL] Basic import failed: {e}")
            return False
    
    @staticmethod
    def test_kimera_core_imports():
        """Test core Kimera module imports."""
        try:
            # Test if kimera package can be imported
            sys.path.insert(0, str(Path.cwd() / "src"))
            
            from kimera.identity import Identity, create_geoid_identity
            from kimera.storage import LatticeStorage
            from kimera.reactor_mp import adaptive_tau, decay_factor
            
            print("[OK] Core Kimera imports successful")
            return True
        except ImportError as e:
            print(f"[FAIL] Kimera core import failed: {e}")
            return False
        except Exception as e:
            print(f"[FAIL] Kimera core import error: {e}")
            return False
    
    @staticmethod
    def test_vault_imports():
        """Test vault module imports."""
        try:
            from vault.core.vault import Vault
            print("[OK] Vault imports successful")
            return True
        except ImportError as e:
            print(f"[FAIL] Vault import failed: {e}")
            return False
        except Exception as e:
            print(f"[FAIL] Vault import error: {e}")
            return False


class FunctionalityTests:
    """Test core functionality."""
    
    @staticmethod
    def test_identity_creation():
        """Test identity creation functionality."""
        try:
            sys.path.insert(0, str(Path.cwd() / "src"))
            from kimera.identity import create_geoid_identity
            
            # Create a test identity
            identity = create_geoid_identity()
            
            if identity is not None:
                print("[OK] Identity creation successful")
                return True
            else:
                print("[FAIL] Identity creation returned None")
                return False
        except Exception as e:
            print(f"[FAIL] Identity creation failed: {e}")
            return False
    
    @staticmethod
    def test_storage_functionality():
        """Test storage functionality."""
        try:
            sys.path.insert(0, str(Path.cwd() / "src"))
            from kimera.storage import LatticeStorage
            
            # Create temporary storage
            with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
                storage = LatticeStorage(tmp.name)
                
                # Test basic storage operations
                if hasattr(storage, 'store_echoform'):
                    print("[OK] Storage functionality available")
                    return True
                else:
                    print("[FAIL] Storage missing expected methods")
                    return False
        except Exception as e:
            print(f"[FAIL] Storage test failed: {e}")
            return False
    
    @staticmethod
    def test_vault_functionality():
        """Test vault functionality."""
        try:
            from vault.core.vault import Vault
            
            # Create a test vault
            vault = Vault()
            
            if vault is not None:
                print("[OK] Vault creation successful")
                return True
            else:
                print("[FAIL] Vault creation returned None")
                return False
        except Exception as e:
            print(f"[FAIL] Vault test failed: {e}")
            return False


class SystemTests:
    """Test system-level functionality."""
    
    @staticmethod
    def test_file_structure():
        """Test that required files exist."""
        required_files = [
            "src/kimera/__init__.py",
            "src/kimera/identity.py",
            "src/kimera/storage.py",
            "src/kimera/reactor_mp.py",
            "vault/__init__.py",
            "vault/core/__init__.py",
            "vault/core/vault.py",
            ".github/workflows/ci.yml"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)
        
        if missing_files:
            print(f"✗ Missing files: {missing_files}")
            return False
        else:
            print("[OK] All required files present")
            return True
    
    @staticmethod
    def test_python_syntax():
        """Test Python syntax of core files."""
        python_files = [
            "src/kimera/identity.py",
            "src/kimera/storage.py",
            "src/kimera/reactor_mp.py",
            "vault/core/vault.py"
        ]
        
        syntax_errors = []
        for file_path in python_files:
            if Path(file_path).exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        compile(f.read(), file_path, 'exec')
                except SyntaxError as e:
                    syntax_errors.append(f"{file_path}: {e}")
        
        if syntax_errors:
            print(f"[FAIL] Syntax errors: {syntax_errors}")
            return False
        else:
            print("[OK] All Python files have valid syntax")
            return True
    
    @staticmethod
    def test_ci_configuration():
        """Test CI configuration is valid."""
        ci_file = Path(".github/workflows/ci.yml")
        
        if not ci_file.exists():
            print("[FAIL] CI file missing")
            return False
        
        try:
            import yaml
            with open(ci_file, 'r') as f:
                yaml.safe_load(f.read())
            print("[OK] CI configuration is valid YAML")
            return True
        except ImportError:
            print("⚠️  PyYAML not available, skipping YAML validation")
            # Check basic structure instead
            with open(ci_file, 'r') as f:
                content = f.read()
                if 'name:' in content and 'jobs:' in content:
                    print("[OK] CI file has basic structure")
                    return True
                else:
                    print("[FAIL] CI file missing basic structure")
                    return False
        except Exception as e:
            print(f"[FAIL] CI configuration invalid: {e}")
            return False


class IntegrationTests:
    """Test integration between components."""
    
    @staticmethod
    def test_end_to_end_workflow():
        """Test a basic end-to-end workflow."""
        try:
            sys.path.insert(0, str(Path.cwd() / "src"))
            
            # Import required modules
            from kimera.identity import create_geoid_identity
            from kimera.storage import LatticeStorage
            from vault.core.vault import Vault
            
            # Create components
            identity = create_geoid_identity()
            vault = Vault()
            
            # Create temporary storage
            with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
                storage = LatticeStorage(tmp.name)
                
                print("[OK] End-to-end workflow components created successfully")
                return True
                
        except Exception as e:
            print(f"[FAIL] End-to-end workflow failed: {e}")
            return False
    
    @staticmethod
    def test_module_compatibility():
        """Test that modules work together."""
        try:
            sys.path.insert(0, str(Path.cwd() / "src"))
            
            # Test that modules can be imported together
            from kimera import identity, storage, reactor_mp
            from vault.core import vault
            
            print("[OK] Module compatibility test passed")
            return True
        except Exception as e:
            print(f"[FAIL] Module compatibility failed: {e}")
            return False


def main():
    """Run the complete test suite."""
    print("🚀 KIMERA COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Working directory: {Path.cwd()}")
    
    suite = TestSuite()
    
    # Import Tests
    print("\n📦 IMPORT TESTS")
    print("-" * 40)
    suite.run_test("Basic Python Imports", ImportTests.test_basic_imports)
    suite.run_test("Kimera Core Imports", ImportTests.test_kimera_core_imports)
    suite.run_test("Vault Imports", ImportTests.test_vault_imports)
    
    # Functionality Tests
    print("\n⚙️  FUNCTIONALITY TESTS")
    print("-" * 40)
    suite.run_test("Identity Creation", FunctionalityTests.test_identity_creation)
    suite.run_test("Storage Functionality", FunctionalityTests.test_storage_functionality)
    suite.run_test("Vault Functionality", FunctionalityTests.test_vault_functionality)
    
    # System Tests
    print("\n🏗️  SYSTEM TESTS")
    print("-" * 40)
    suite.run_test("File Structure", SystemTests.test_file_structure)
    suite.run_test("Python Syntax", SystemTests.test_python_syntax)
    suite.run_test("CI Configuration", SystemTests.test_ci_configuration)
    
    # Integration Tests
    print("\n🔗 INTEGRATION TESTS")
    print("-" * 40)
    suite.run_test("End-to-End Workflow", IntegrationTests.test_end_to_end_workflow)
    suite.run_test("Module Compatibility", IntegrationTests.test_module_compatibility)
    
    # Print summary
    suite.print_summary()
    
    # Return appropriate exit code
    return 0 if suite.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())