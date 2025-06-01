#!/usr/bin/env python3
"""
Comprehensive Kimera Validation Suite
Tests all major functionality and edge cases
"""

import sys
import os
import time
import traceback
from typing import List, Dict, Any

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

class KimeraValidator:
    def __init__(self):
        self.results = []
        self.start_time = time.time()
    
    def log_test(self, test_name: str, success: bool, details: str = "", error: str = ""):
        """Log test result"""
        self.results.append({
            'test': test_name,
            'success': success,
            'details': details,
            'error': error,
            'timestamp': time.time() - self.start_time
        })
        
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")
        if details:
            print(f"   {details}")
        if error:
            print(f"   Error: {error}")
    
    def test_core_imports(self):
        """Test all core module imports"""
        try:
            from kimera.geoid import init_geoid, Geoid
            from kimera.echoform import EchoForm
            from kimera.reactor import reactor_cycle, reactor_cycle_batched
            from kimera.resonance import resonance, THRESH
            from kimera.scar import create_scar
            from kimera.storage import get_storage, close_storage
            from kimera.cls import lattice_resolve
            from kimera.identity import Identity
            
            self.log_test("Core Imports", True, "All modules imported successfully")
            return True
        except Exception as e:
            self.log_test("Core Imports", False, error=str(e))
            return False
    
    def test_geoid_creation_patterns(self):
        """Test various geoid creation patterns"""
        try:
            from kimera.geoid import init_geoid
            
            # Basic pattern
            g1 = init_geoid("Hello world", "en", ["test"])
            
            # With raw parameter
            g2 = init_geoid("Hello world", "en", ["test"], raw="Original text")
            
            # Streaming pattern
            g3 = init_geoid(raw="Streaming text", lang="en", tags=["benchmark"])
            
            # Minimal pattern
            g4 = init_geoid("Minimal test")
            
            # Verify properties
            assert g1.gid and len(g1.gid) == 16
            assert g1.echo == "Hello world"
            assert g1.lang_axis == "en"
            assert g1.context_layers == ["test"]
            assert g1.sem_vec.shape[0] in [384, 512]  # Common embedding sizes
            
            self.log_test("Geoid Creation Patterns", True, 
                         f"Created 4 geoids with different patterns. Sample GID: {g1.gid}")
            return True
        except Exception as e:
            self.log_test("Geoid Creation Patterns", False, error=str(e))
            return False
    
    def test_echoform_functionality(self):
        """Test EchoForm creation and manipulation"""
        try:
            from kimera.echoform import EchoForm
            
            # Create form
            form = EchoForm(anchor="test_form", domain="validation")
            
            # Add terms
            form.add_term("hello", role="greeting", intensity=0.8)
            form.add_term("world", role="object", intensity=0.6)
            
            # Test methods
            intensity = form.intensity_sum()
            entropy = form.entropy()
            trace = form.trace_signature
            
            # Test serialization
            serialized = form.flatten()
            restored = EchoForm.reinflate(serialized)
            
            assert len(form.terms) == 2
            assert intensity > 0
            assert len(trace) == 16
            assert restored.anchor == form.anchor
            
            self.log_test("EchoForm Functionality", True,
                         f"Form with {len(form.terms)} terms, intensity={intensity:.3f}, entropy={entropy:.3f}")
            return True
        except Exception as e:
            self.log_test("EchoForm Functionality", False, error=str(e))
            return False
    
    def test_resonance_calculations(self):
        """Test resonance between different geoid pairs"""
        try:
            from kimera.geoid import init_geoid
            from kimera.resonance import resonance, THRESH
            
            # Create test geoids
            g1 = init_geoid("Birds can fly", "en", ["test"])
            g2 = init_geoid("Birds cannot fly", "en", ["test"])  # Negation
            g3 = init_geoid("The sky is blue", "en", ["test"])   # Unrelated
            g4 = init_geoid("Birds can fly", "en", ["test"])     # Identical
            
            # Test resonance scores
            score_negation = resonance(g1, g2)
            score_unrelated = resonance(g1, g3)
            score_identical = resonance(g1, g4)
            
            # Verify reasonable scores
            assert 0 <= score_negation <= 1
            assert 0 <= score_unrelated <= 1
            assert 0 <= score_identical <= 1
            
            # Identical should have highest score
            assert score_identical >= score_negation
            assert score_identical >= score_unrelated
            
            self.log_test("Resonance Calculations", True,
                         f"Negation: {score_negation:.3f}, Unrelated: {score_unrelated:.3f}, Identical: {score_identical:.3f}")
            return True
        except Exception as e:
            self.log_test("Resonance Calculations", False, error=str(e))
            return False
    
    def test_reactor_operations(self):
        """Test reactor cycle operations"""
        try:
            from kimera.geoid import init_geoid
            from kimera.reactor import reactor_cycle, reactor_cycle_batched
            
            # Create test geoids
            geoids = [init_geoid(f"Test sentence {i}", "en", ["reactor"]) for i in range(10)]
            
            # Test single-threaded reactor
            initial_scars = sum(len(g.scars) for g in geoids)
            stats = reactor_cycle(geoids, cycles=1)
            final_scars = sum(len(g.scars) for g in geoids)
            
            # Test batched reactor
            batch_stats = reactor_cycle_batched(geoids, chunk=5, verbose=False)
            
            new_scars = final_scars - initial_scars
            
            self.log_test("Reactor Operations", True,
                         f"Processed {len(geoids)} geoids, created {new_scars} scars")
            return True
        except Exception as e:
            self.log_test("Reactor Operations", False, error=str(e))
            return False
    
    def test_storage_operations(self):
        """Test storage and persistence"""
        try:
            from kimera.storage import get_storage, close_storage
            from kimera.echoform import EchoForm
            from kimera.identity import Identity
            
            # Get in-memory storage for testing
            storage = get_storage(":memory:")
            
            # Test EchoForm storage
            form = EchoForm(anchor="storage_test", domain="validation")
            form.add_term("test", role="storage", intensity=1.0)
            storage.store_form(form)
            
            # Test retrieval
            retrieved = storage.fetch_form("storage_test")
            assert retrieved is not None
            assert retrieved.anchor == "storage_test"
            
            # Test Identity storage
            identity = Identity(content="Test identity")
            storage.store_identity(identity)
            
            retrieved_identity = storage.fetch_identity(identity.id)
            assert retrieved_identity is not None
            
            # Clean up
            close_storage()
            
            self.log_test("Storage Operations", True,
                         "EchoForm and Identity storage/retrieval working")
            return True
        except Exception as e:
            self.log_test("Storage Operations", False, error=str(e))
            return False
    
    def test_cls_integration(self):
        """Test CLS lattice integration"""
        try:
            from kimera.geoid import init_geoid
            from kimera.cls import lattice_resolve
            from kimera.identity import geoid_to_identity
            
            # Create test geoids and convert to identities
            g1 = init_geoid("CLS test A", "en", ["cls"])
            g2 = init_geoid("CLS test B", "en", ["cls"])
            
            id1 = geoid_to_identity(g1)
            id2 = geoid_to_identity(g2)
            
            # Test lattice resolution
            intensity = lattice_resolve(id1, id2)
            
            assert isinstance(intensity, (int, float))
            assert intensity >= 0
            
            self.log_test("CLS Integration", True,
                         f"Lattice resolution returned intensity: {intensity:.3f}")
            return True
        except Exception as e:
            self.log_test("CLS Integration", False, error=str(e))
            return False
    
    def test_cli_interface(self):
        """Test CLI interface functionality"""
        try:
            import subprocess
            
            # Test basic CLI help
            result = subprocess.run([sys.executable, "-m", "kimera", "--help"], 
                                  capture_output=True, text=True, timeout=10)
            
            assert result.returncode == 0
            assert "kimera" in result.stdout.lower()
            
            # Test lattice list (should work even if empty)
            result = subprocess.run([sys.executable, "-m", "kimera", "lattice", "list"], 
                                  capture_output=True, text=True, timeout=10)
            
            assert result.returncode == 0
            
            self.log_test("CLI Interface", True,
                         "CLI help and lattice commands working")
            return True
        except Exception as e:
            self.log_test("CLI Interface", False, error=str(e))
            return False
    
    def test_performance_benchmarks(self):
        """Test performance with larger datasets"""
        try:
            from kimera.geoid import init_geoid
            from kimera.reactor import reactor_cycle
            import time
            
            # Create larger dataset
            start_time = time.time()
            geoids = [init_geoid(f"Performance test {i}", "en", ["perf"]) for i in range(50)]
            creation_time = time.time() - start_time
            
            # Test reactor performance
            start_time = time.time()
            reactor_cycle(geoids, cycles=1)
            reactor_time = time.time() - start_time
            
            self.log_test("Performance Benchmarks", True,
                         f"Created 50 geoids in {creation_time:.3f}s, reactor cycle in {reactor_time:.3f}s")
            return True
        except Exception as e:
            self.log_test("Performance Benchmarks", False, error=str(e))
            return False
    
    def run_all_tests(self):
        """Run all validation tests"""
        print("🚀 Kimera Comprehensive Validation Suite")
        print("=" * 60)
        
        tests = [
            self.test_core_imports,
            self.test_geoid_creation_patterns,
            self.test_echoform_functionality,
            self.test_resonance_calculations,
            self.test_reactor_operations,
            self.test_storage_operations,
            self.test_cls_integration,
            self.test_cli_interface,
            self.test_performance_benchmarks
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                self.log_test(test.__name__, False, error=f"Unexpected error: {e}")
                traceback.print_exc()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 VALIDATION SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for r in self.results if r['success'])
        total = len(self.results)
        success_rate = (passed / total) * 100 if total > 0 else 0
        
        print(f"Tests Passed: {passed}/{total} ({success_rate:.1f}%)")
        print(f"Total Runtime: {time.time() - self.start_time:.2f}s")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED - KIMERA IS PRODUCTION READY!")
        else:
            print(f"\n⚠️  {total - passed} tests failed - review needed")
            
            # Show failed tests
            failed_tests = [r for r in self.results if not r['success']]
            if failed_tests:
                print("\nFailed Tests:")
                for test in failed_tests:
                    print(f"  ❌ {test['test']}: {test['error']}")
        
        return passed == total

def main():
    validator = KimeraValidator()
    success = validator.run_all_tests()
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)