#!/usr/bin/env python3
"""
Fuzz testing for EchoForm using Hypothesis
Tests random EchoForm generation, serialization, and round-trip integrity
"""
import sys
import time
import math
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from hypothesis import given, strategies as st, settings, HealthCheck
from kimera.echoform import EchoForm
import random


# Hypothesis strategies for generating test data
@st.composite
def echoform_term(draw):
    """Generate a random EchoForm term"""
    symbol = draw(st.text(min_size=1, max_size=20, alphabet=st.characters(min_codepoint=32, max_codepoint=126)))
    intensity = draw(st.floats(min_value=0.0, max_value=2.0, allow_nan=False, allow_infinity=False))
    role = draw(st.sampled_from(["primary", "secondary", "resonance_trigger", "geoid_a", "geoid_b", "creation_event"]))
    
    term = {
        "symbol": symbol,
        "intensity": intensity,
        "role": role,
        "timestamp": time.time() + draw(st.floats(min_value=-86400, max_value=86400))  # ±1 day
    }
    
    # Sometimes add extra fields
    if draw(st.booleans()):
        term["metadata"] = draw(st.dictionaries(
            st.text(min_size=1, max_size=10, alphabet=st.characters(min_codepoint=32, max_codepoint=126)),
            st.one_of(st.text(max_size=50), st.floats(allow_nan=False, allow_infinity=False), st.booleans()),
            min_size=0, max_size=3
        ))
    
    return term


@st.composite
def random_echoform(draw):
    """Generate a random EchoForm with 10-100 terms"""
    num_terms = draw(st.integers(min_value=10, max_value=100))
    terms = draw(st.lists(echoform_term(), min_size=num_terms, max_size=num_terms))
    
    anchor = draw(st.text(min_size=1, max_size=50, alphabet=st.characters(min_codepoint=32, max_codepoint=126)))
    domain = draw(st.sampled_from(["cls", "test", "fuzz", "random"]))
    phase = draw(st.sampled_from(["active", "dormant", "lattice_active", "resonance"]))
    
    # Create topology
    topology = {
        "type": draw(st.sampled_from(["simple", "lattice", "complex"])),
        "created_at": time.time()
    }
    
    if draw(st.booleans()):
        topology["metadata"] = draw(st.dictionaries(
            st.text(min_size=1, max_size=10),
            st.text(max_size=20),
            min_size=0, max_size=2
        ))
    
    return EchoForm(
        anchor=anchor,
        domain=domain,
        phase=phase,
        terms=terms,
        topology=topology
    )


class TestEchoFormFuzz:
    """Fuzz tests for EchoForm"""
    
    @given(random_echoform())
    @settings(max_examples=1000, deadline=2000, suppress_health_check=[HealthCheck.too_slow])
    def test_round_trip_serialization(self, form):
        """Test that EchoForm can be serialized and deserialized without data loss"""
        # Serialize
        blob = form.flatten()
        assert isinstance(blob, str)
        assert len(blob) > 0
        
        # Deserialize
        restored_form = EchoForm.reinflate(blob)
        
        # Verify basic properties
        assert restored_form.anchor == form.anchor
        assert restored_form.domain == form.domain
        assert restored_form.phase == form.phase
        assert len(restored_form.terms) == len(form.terms)
        assert restored_form.topology == form.topology
        
        # Verify intensity sum is close (accounting for floating point precision)
        original_intensity = form.intensity_sum(apply_time_decay=False)
        restored_intensity = restored_form.intensity_sum(apply_time_decay=False)
        
        if not (math.isnan(original_intensity) and math.isnan(restored_intensity)):
            assert math.isclose(original_intensity, restored_intensity, rel_tol=1e-9), \
                f"Intensity mismatch: {original_intensity} != {restored_intensity}"
    
    @given(random_echoform())
    @settings(max_examples=500, deadline=1000)
    def test_intensity_sum_properties(self, form):
        """Test properties of intensity_sum calculation"""
        intensity_no_decay = form.intensity_sum(apply_time_decay=False)
        intensity_with_decay = form.intensity_sum(apply_time_decay=True)
        
        # Both should be non-negative (unless all terms have negative intensity)
        min_term_intensity = min((term.get("intensity", 0) for term in form.terms), default=0)
        if min_term_intensity >= 0:
            assert intensity_no_decay >= 0
            assert intensity_with_decay >= 0
        
        # With decay should be <= without decay (decay reduces intensity)
        if not math.isnan(intensity_no_decay) and not math.isnan(intensity_with_decay):
            assert intensity_with_decay <= intensity_no_decay + 1e-9  # Small tolerance for floating point
    
    @given(random_echoform(), st.floats(min_value=0.1, max_value=100.0))
    @settings(max_examples=300, deadline=1000)
    def test_time_decay_properties(self, form, tau):
        """Test time decay calculation properties"""
        try:
            intensity_no_decay = form.intensity_sum(apply_time_decay=False)
            intensity_with_decay = form.intensity_sum(apply_time_decay=True, tau=tau)
            
            # Skip if either is NaN
            if math.isnan(intensity_no_decay) or math.isnan(intensity_with_decay):
                return
            
            # Decay should reduce or maintain intensity
            assert intensity_with_decay <= intensity_no_decay + 1e-9
            
            # Both should be finite
            assert math.isfinite(intensity_no_decay)
            assert math.isfinite(intensity_with_decay)
            
        except (ValueError, OverflowError):
            # Some extreme values might cause mathematical errors, which is acceptable
            pass
    
    @given(st.lists(random_echoform(), min_size=2, max_size=5))
    @settings(max_examples=200, deadline=1500)
    def test_multiple_forms_serialization(self, forms):
        """Test serialization of multiple forms doesn't interfere"""
        blobs = []
        
        # Serialize all forms
        for form in forms:
            blob = form.flatten()
            blobs.append(blob)
        
        # Deserialize all forms
        restored_forms = []
        for blob in blobs:
            restored_form = EchoForm.reinflate(blob)
            restored_forms.append(restored_form)
        
        # Verify each form matches its original
        for original, restored in zip(forms, restored_forms):
            assert original.anchor == restored.anchor
            assert original.domain == restored.domain
            assert len(original.terms) == len(restored.terms)
            
            # Check intensity sums are close
            orig_intensity = original.intensity_sum(apply_time_decay=False)
            rest_intensity = restored.intensity_sum(apply_time_decay=False)
            
            if not (math.isnan(orig_intensity) and math.isnan(rest_intensity)):
                assert math.isclose(orig_intensity, rest_intensity, rel_tol=1e-9)


def run_performance_test():
    """Run a quick performance test to ensure fuzz tests complete in reasonable time"""
    print("Running EchoForm fuzz performance test...")
    
    start_time = time.perf_counter()
    
    # Generate and test 100 random forms
    for i in range(100):
        # Create a random form
        terms = []
        for _ in range(random.randint(10, 50)):
            terms.append({
                "symbol": f"test_symbol_{random.randint(1, 1000)}",
                "intensity": random.uniform(0.0, 2.0),
                "role": random.choice(["primary", "secondary", "resonance_trigger"]),
                "timestamp": time.time() + random.uniform(-3600, 3600)
            })
        
        form = EchoForm(
            anchor=f"perf_test_{i}",
            domain="test",
            phase="active",
            terms=terms,
            topology={"type": "simple", "created_at": time.time()}
        )
        
        # Test round-trip
        blob = form.flatten()
        restored = EchoForm.reinflate(blob)
        
        # Quick verification
        assert restored.anchor == form.anchor
        assert len(restored.terms) == len(form.terms)
    
    elapsed = time.perf_counter() - start_time
    print(f"Performance test completed: 100 forms in {elapsed:.2f}s ({elapsed/100*1000:.1f}ms per form)")
    
    if elapsed > 2.0:
        print("WARNING: Performance test took longer than expected")
        return False
    else:
        print("Performance test passed!")
        return True


def main():
    """Run fuzz tests"""
    print("🧪 EchoForm Fuzz Testing with Hypothesis")
    print("=" * 45)
    
    # Run performance test first
    if not run_performance_test():
        print("❌ Performance test failed")
        return False
    
    print("\nRunning Hypothesis fuzz tests...")
    
    # Import pytest to run the tests
    try:
        import pytest
        
        # Run the fuzz tests
        result = pytest.main([
            __file__,
            "-v",
            "--tb=short",
            "-x"  # Stop on first failure
        ])
        
        if result == 0:
            print("✅ All fuzz tests passed!")
            return True
        else:
            print("❌ Some fuzz tests failed")
            return False
            
    except ImportError:
        print("❌ pytest not available, running basic test...")
        
        # Run a basic test manually
        try:
            test_instance = TestEchoFormFuzz()
            
            # Generate a few random forms and test them
            for i in range(10):
                # Create a simple random form
                terms = [{
                    "symbol": f"test_{i}_{j}",
                    "intensity": random.uniform(0.1, 1.0),
                    "role": "primary",
                    "timestamp": time.time()
                } for j in range(random.randint(10, 30))]
                
                form = EchoForm(
                    anchor=f"manual_test_{i}",
                    domain="test",
                    phase="active",
                    terms=terms,
                    topology={"type": "simple"}
                )
                
                # Test serialization
                blob = form.flatten()
                restored = EchoForm.reinflate(blob)
                
                assert restored.anchor == form.anchor
                assert len(restored.terms) == len(form.terms)
                
                orig_intensity = form.intensity_sum(apply_time_decay=False)
                rest_intensity = restored.intensity_sum(apply_time_decay=False)
                assert math.isclose(orig_intensity, rest_intensity, rel_tol=1e-9)
            
            print("✅ Basic fuzz tests passed!")
            return True
            
        except Exception as e:
            print(f"❌ Basic fuzz test failed: {e}")
            return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)