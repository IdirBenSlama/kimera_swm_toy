#!/usr/bin/env python3
"""
Comprehensive validation for Kimera v0.7.3
Tests CLS lattice storage, cls_event tracking, and time-decay weighting
"""
import sys
import os
import math
sys.path.insert(0, 'src')

def safe_print(message):
    """Safe print function that handles Unicode issues on Windows"""
    try:
        print(message)
    except UnicodeEncodeError:
        # Fallback: replace problematic characters
        safe_message = message.encode('ascii', 'replace').decode('ascii')
        print(safe_message)

def test_echoform_time_decay():
    """Test EchoForm time-decay functionality"""
    safe_print("Testing EchoForm Time-Decay...")
    
    try:
        from kimera.echoform import EchoForm, TIME_DECAY_TAU
        import time
        
        # Test constants
        expected_tau = 14 * 24 * 3600  # 14 days
        assert TIME_DECAY_TAU == expected_tau, f"Expected τ = {expected_tau}, got {TIME_DECAY_TAU}"
        safe_print(f"  ✅ TIME_DECAY_TAU = {TIME_DECAY_TAU} seconds ({TIME_DECAY_TAU/(24*3600):.1f} days)")
        
        # Test time-decay calculation
        current_time = time.time()
        echo = EchoForm(anchor="decay_test")
        echo.terms = [
            {"intensity": 1.0, "timestamp": current_time},  # Recent
            {"intensity": 1.0, "timestamp": current_time - TIME_DECAY_TAU},  # 1 τ ago
            {"intensity": 1.0}  # No timestamp
        ]
        
        # Test without decay
        no_decay = echo.intensity_sum(apply_time_decay=False)
        assert math.isclose(no_decay, 3.0, rel_tol=1e-9), f"Expected 3.0 (within tolerance) without decay, got {no_decay}"
        
        # Test with decay
        with_decay = echo.intensity_sum(apply_time_decay=True)
        assert with_decay < no_decay, "Decay should reduce total intensity"
        assert with_decay > 1.0, "Should have at least recent term intensity"
        
        safe_print(f"  ✅ Intensity without decay: {no_decay}")
        safe_print(f"  ✅ Intensity with decay: {with_decay:.3f}")
        safe_print(f"  ✅ Decay factor: {with_decay/no_decay:.3f}")
        
        return True
        
    except Exception as e:
        safe_print(f"  ❌ Time-decay test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cls_lattice_storage():
    """Test CLS lattice storage functionality"""
    safe_print("\nTesting CLS Lattice Storage...")
    
    try:
        from kimera.geoid import init_geoid
        from kimera.cls import lattice_resolve, clear_stored_forms, get_stored_forms, get_form_by_anchor
        
        # Clear storage
        clear_stored_forms()
        
        # Create test geoids
        geo_a = init_geoid("Storage test A", "en", ["test"])
        geo_b = init_geoid("Storage test B", "en", ["test"])
        
        # First resolve
        intensity1 = lattice_resolve(geo_a, geo_b)
        assert math.isclose(intensity1, 1.1, rel_tol=1e-9), f"Expected 1.1 (within tolerance), got {intensity1}"
        
        # Check storage
        stored = get_stored_forms()
        assert len(stored) == 1, f"Expected 1 stored form, got {len(stored)}"
        
        # Second resolve (should add cls_event)
        intensity2 = lattice_resolve(geo_a, geo_b)
        assert math.isclose(intensity2, 1.2, rel_tol=1e-9), f"Expected 1.2 (within tolerance), got {intensity2}"
        
        # Third resolve
        intensity3 = lattice_resolve(geo_a, geo_b)
        assert math.isclose(intensity3, 1.3, rel_tol=1e-9), f"Expected 1.3 (within tolerance), got {intensity3}"
        
        # Check stored form details
        anchor = f"{geo_a.gid}_{geo_b.gid}"
        form = get_form_by_anchor(anchor)
        assert form.domain == "cls", "Form should be in cls domain"
        assert len(form.terms) == 4, f"Expected 4 terms, got {len(form.terms)}"  # 1 cls_seed + 3 cls_events
        
        safe_print(f"  ✅ Storage working: {len(stored)} forms stored")
        safe_print(f"  ✅ Intensity progression: {intensity1} → {intensity2} → {intensity3}")
        safe_print(f"  ✅ Form has {len(form.terms)} terms")
        
        return True
        
    except Exception as e:
        safe_print(f"  ❌ CLS storage test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cls_event_tracking():
    """Test cls_event tracking functionality"""
    safe_print("\nTesting cls_event Tracking...")
    
    try:
        from kimera.geoid import init_geoid
        from kimera.cls import lattice_resolve, clear_stored_forms, get_form_by_anchor, create_lattice_form
        
        # Clear storage
        clear_stored_forms()
        
        # Test lattice_resolve events
        geo_a = init_geoid("Event test A", "en", ["test"])
        geo_b = init_geoid("Event test B", "en", ["test"])
        
        # Multiple resolves
        lattice_resolve(geo_a, geo_b)
        lattice_resolve(geo_a, geo_b)
        
        # Check cls_events
        anchor = f"{geo_a.gid}_{geo_b.gid}"
        form = get_form_by_anchor(anchor)
        cls_events = [term for term in form.terms if term.get("symbol") == "cls_event"]
        
        assert len(cls_events) == 2, f"Expected 2 cls_events, got {len(cls_events)}"
        
        # Check event properties
        for event in cls_events:
            assert "timestamp" in event, "cls_event should have timestamp"
            assert event["role"] == "resonance_trigger", "cls_event should have correct role"
            assert math.isclose(event["intensity"], 0.1, rel_tol=1e-9), "cls_event should have 0.1 intensity"
            assert "event_type" in event, "cls_event should have event_type"
        
        # Test create_lattice_form events
        form2 = create_lattice_form("test_creation", geo_a, geo_b)
        creation_events = [term for term in form2.terms if term.get("role") == "creation_event"]
        assert len(creation_events) == 1, "Should have 1 creation event"
        assert creation_events[0]["event_type"] == "lattice_form_created"
        
        safe_print(f"  ✅ cls_event tracking: {len(cls_events)} events found")
        safe_print(f"  ✅ Creation event tracking: {len(creation_events)} events found")
        
        return True
        
    except Exception as e:
        safe_print(f"  ❌ cls_event tracking test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_backward_compatibility():
    """Test that existing functionality still works"""
    safe_print("\nTesting Backward Compatibility...")
    
    try:
        # Test basic geoid creation
        from kimera.geoid import init_geoid
        g = init_geoid(text="Compatibility test", lang="en", tags=["test"])
        assert hasattr(g, 'echo'), "Geoid should have echo field"
        assert g.echo == "Compatibility test", "Echo should match input"
        safe_print("  ✅ Geoid creation works")
        
        # Test EchoForm basic functionality
        from kimera.echoform import EchoForm
        echo = EchoForm(anchor="compat_test")
        echo.add_term("test", "role", 1.0)
        assert math.isclose(echo.intensity_sum(apply_time_decay=False), 1.0, rel_tol=1e-9), "Basic intensity sum should work"
        safe_print("  ✅ EchoForm basic functionality works")
        
        # Test serialization
        blob = echo.flatten()
        restored = EchoForm.reinflate(blob)
        assert restored.anchor == echo.anchor, "Serialization should preserve anchor"
        safe_print("  ✅ Serialization works")
        
        return True
        
    except Exception as e:
        safe_print(f"  ❌ Backward compatibility test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_parameter_documentation():
    """Test that parameter documentation exists"""
    safe_print("\nTesting Parameter Documentation...")
    
    try:
        # Check that docs/echoform_params.md exists
        assert os.path.exists("docs/echoform_params.md"), "Parameter documentation should exist"
        
        # Check content
        with open("docs/echoform_params.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        assert "TIME_DECAY_TAU" in content, "Should document TIME_DECAY_TAU"
        assert "extra_domains" in content, "Should document extra_domains"
        assert "topology_backend" in content, "Should document topology_backend"
        assert "trace_signature" in content, "Should document trace_signature"
        
        safe_print("  ✅ Parameter documentation exists and contains key parameters")
        
        return True
        
    except Exception as e:
        safe_print(f"  ❌ Parameter documentation test failed: {e}")
        return False

def main():
    """Run comprehensive v0.7.3 validation"""
    safe_print("Kimera v0.7.3 Comprehensive Validation")
    safe_print("CLS Lattice Storage + Time-Decay Weighting")
    safe_print("=" * 50)
    
    tests = [
        ("EchoForm Time-Decay", test_echoform_time_decay),
        ("CLS Lattice Storage", test_cls_lattice_storage),
        ("cls_event Tracking", test_cls_event_tracking),
        ("Backward Compatibility", test_backward_compatibility),
        ("Parameter Documentation", test_parameter_documentation),
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            safe_print(f"\n❌ {name} test crashed: {e}")
    
    safe_print(f"\nValidation Results: {passed}/{total} tests passed")
    
    if passed == total:
        safe_print("\nAll v0.7.3 features working perfectly!")
        safe_print("\nPhase 19.2 Complete:")
        safe_print("  • CLS lattice forms stored and tracked")
        safe_print("  • cls_event terms append on every resonance")
        safe_print("  • Time-decay weighting with τ = 14 days")
        safe_print("  • Enhanced parameter documentation")
        safe_print("  • All backward compatibility preserved")
        safe_print("\nReady for v0.7.3 tag and next phase!")
        return True
    else:
        safe_print(f"\n{total - passed} test(s) failed")
        safe_print("Fix issues before tagging v0.7.3")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)