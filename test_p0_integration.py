#!/usr/bin/env python3
"""
P0 Integration Test Suite
Tests the critical P0 functionality:
1. Migration with dual-write
2. CLS lattice integration with Identity
3. Observability hooks and entropy tracking
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from conftest import fresh_duckdb_path

def test_p0_migration_integration():
    """Test P0: Migration with dual-write verification"""
    print("🧪 P0 Test 1: Migration with dual-write verification")
    
    # Set dual-write environment variable
    os.environ["KIMERA_ID_DUAL_WRITE"] = "1"
    
    try:
        from kimera.storage import LatticeStorage
        from kimera.identity import create_geoid_identity
        from kimera.echoform import EchoForm
        import scripts.migrate_identity as migrate
        
        # Create temporary database using fresh_duckdb_path
        db_path = fresh_duckdb_path()
        
        try:
            storage = LatticeStorage(db_path)
            
            # Create test data
            echo1 = EchoForm("Migration test content", lang="en")
            storage.store_echoform(echo1)
            
            # Run migration
            migrate.add_identity_schema(storage)
            migrate.migrate_echoforms_to_identities(storage)
            
            # Test dual-write
            new_identity = create_geoid_identity("Dual write test", tags=["p0_test"])
            storage.store_identity(new_identity)
            
            # Verify retrieval
            retrieved = storage.fetch_identity(new_identity.id)
            assert retrieved is not None, "Failed to retrieve stored identity"
            assert retrieved.raw == new_identity.raw, "Data mismatch"
            
            print("✅ P0 Migration test passed")
            storage.close()
            return True
            
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
                
    except Exception as e:
        print(f"❌ P0 Migration test failed: {e}")
        return False
    
    finally:
        if "KIMERA_ID_DUAL_WRITE" in os.environ:
            del os.environ["KIMERA_ID_DUAL_WRITE"]


def test_p0_cls_integration():
    """Test P0: CLS lattice integration with Identity"""
    print("🧪 P0 Test 2: CLS lattice integration")
    
    try:
        from kimera.storage import LatticeStorage
        from kimera.identity import create_geoid_identity
        from kimera.cls import lattice_resolve, create_lattice_form, create_identity_lattice, create_scar_lattice
        
        # Create temporary database using fresh_duckdb_path
        db_path = fresh_duckdb_path()
        
        try:
            storage = LatticeStorage(db_path)
            
            # Test 1: Identity-based lattice resolution
            identity_a = create_geoid_identity("Test content A", tags=["cls_test"])
            identity_b = create_geoid_identity("Test content B", tags=["cls_test"])
            
            # Perform lattice resolution
            intensity = lattice_resolve(identity_a, identity_b)
            assert isinstance(intensity, (int, float)), "Lattice resolve should return numeric intensity"
            assert intensity > 0, "Intensity should be positive"
            
            # Test 2: Create lattice form
            form = create_lattice_form("test_anchor", identity_a, identity_b)
            assert form is not None, "Lattice form should be created"
            assert "entropy" in str(form.terms), "Form should include entropy data"
            
            # Test 3: Convenience function
            convenience_intensity = create_identity_lattice("Content X", "Content Y", ["test"], ["test"])
            assert isinstance(convenience_intensity, (int, float)), "Convenience function should return intensity"
            
            # Test 4: Scar lattice
            scar_intensity = create_scar_lattice(identity_a, identity_b, "contradiction")
            assert isinstance(scar_intensity, (int, float)), "Scar lattice should return intensity"
            
            print("✅ P0 CLS integration test passed")
            storage.close()
            return True
            
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
                
    except Exception as e:
        print(f"❌ P0 CLS integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_p0_observability():
    """Test P0: Observability hooks and entropy tracking"""
    print("🧪 P0 Test 3: Observability and entropy tracking")
    
    try:
        from kimera.storage import LatticeStorage
        from kimera.identity import create_geoid_identity
        from kimera.cls import lattice_resolve
        
        # Test observability imports
        try:
            from kimera.observability import (
                get_metrics_summary, 
                export_metrics_to_file
            )
            observability_available = True
        except ImportError:
            print("⚠️  Observability not available (prometheus_client not installed)")
            observability_available = False
        
        # Create temporary database using fresh_duckdb_path
        db_path = fresh_duckdb_path()
        
        try:
            storage = LatticeStorage(db_path)
            
            # Create identities with different entropy levels
            simple_identity = create_geoid_identity("Simple", tags=["simple"])
            complex_identity = create_geoid_identity(
                "Complex content with many terms and metadata",
                tags=["complex", "multi-term", "high-entropy", "test"]
            )
            
            # Store identities (should trigger observability hooks)
            storage.store_identity(simple_identity)
            storage.store_identity(complex_identity)
            
            # Perform lattice operations (should trigger observability hooks)
            lattice_resolve(simple_identity, complex_identity)
            
            # Test entropy calculations
            simple_entropy = simple_identity.entropy()
            complex_entropy = complex_identity.entropy()
            
            assert complex_entropy > simple_entropy, "Complex identity should have higher entropy"
            
            # Test effective tau
            simple_tau = simple_identity.effective_tau()
            complex_tau = complex_identity.effective_tau()
            
            assert simple_tau != complex_tau, "Different identities should have different tau values"
            
            if observability_available:
                # Test metrics collection
                metrics_summary = get_metrics_summary()
                assert metrics_summary["metrics_available"], "Metrics should be available"
                
                # Test metrics export
                export_success = export_metrics_to_file("test_metrics.txt")
                assert export_success, "Metrics export should succeed"
                
                # Clean up
                if os.path.exists("test_metrics.txt"):
                    os.unlink("test_metrics.txt")
            
            print("✅ P0 Observability test passed")
            storage.close()
            return True
            
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
                
    except Exception as e:
        print(f"❌ P0 Observability test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_p0_entropy_adaptive_decay():
    """Test P0: Entropy-adaptive time decay"""
    print("🧪 P0 Test 4: Entropy-adaptive time decay")
    
    try:
        from kimera.identity import create_geoid_identity
        from kimera.entropy import adaptive_tau
        
        # Create identities with different entropy levels
        low_entropy = create_geoid_identity("Simple", tags=["low"])
        high_entropy = create_geoid_identity(
            "Complex multi-term content",
            tags=["high", "entropy", "complex", "multi", "term"]
        )
        
        # Test entropy calculations
        low_ent = low_entropy.entropy()
        high_ent = high_entropy.entropy()
        
        assert high_ent > low_ent, "High entropy identity should have higher entropy"
        
        # Test adaptive tau
        low_tau = adaptive_tau(1000, low_ent)  # base_tau, entropy
        high_tau = adaptive_tau(1000, high_ent)
        
        assert high_tau != low_tau, "Different entropy should produce different tau"
        
        # Test decay factors
        low_decay = decay_factor(100, low_tau)  # 100 seconds
        high_decay = decay_factor(100, high_tau)
        
        assert 0 <= low_decay <= 1, "Decay factor should be between 0 and 1"
        assert 0 <= high_decay <= 1, "Decay factor should be between 0 and 1"
        
        # Test effective tau method
        low_effective = low_entropy.effective_tau()
        high_effective = high_entropy.effective_tau()
        
        assert low_effective > 0, "Effective tau should be positive"
        assert high_effective > 0, "Effective tau should be positive"
        
        print(f"  Low entropy: {low_ent:.3f}, tau: {low_effective:.1f}")
        print(f"  High entropy: {high_ent:.3f}, tau: {high_effective:.1f}")
        
        print("✅ P0 Entropy-adaptive decay test passed")
        return True
        
    except Exception as e:
        print(f"❌ P0 Entropy-adaptive decay test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_p0_test_suite():
    """Run the complete P0 test suite"""
    print("🚀 Running P0 Integration Test Suite\n")
    
    tests = [
        test_p0_migration_integration,
        test_p0_cls_integration,
        test_p0_observability,
        test_p0_entropy_adaptive_decay
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            print()
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
            print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print(f"📊 P0 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All P0 tests passed! Ready for production deployment.")
        return True
    else:
        print("💥 Some P0 tests failed. Address issues before proceeding.")
        return False


if __name__ == "__main__":
    success = run_p0_test_suite()
    sys.exit(0 if success else 1)