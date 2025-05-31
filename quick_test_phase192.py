#!/usr/bin/env python3
"""
Quick test of Phase 19.2 implementation
"""
import sys
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

def test_time_decay():
    """Test time-decay functionality"""
    safe_print("Testing time-decay functionality...")
    
    from kimera.echoform import EchoForm, TIME_DECAY_TAU
    import time
    
    # Test constants
    safe_print(f"  TIME_DECAY_TAU = {TIME_DECAY_TAU} seconds ({TIME_DECAY_TAU/(24*3600):.1f} days)")
    
    # Create form with time-stamped terms
    current_time = time.time()
    echo = EchoForm(anchor="decay_test")
    echo.terms = [
        {"intensity": 1.0, "timestamp": current_time},  # Recent
        {"intensity": 1.0, "timestamp": current_time - TIME_DECAY_TAU},  # 1 τ ago
        {"intensity": 1.0}  # No timestamp
    ]
    
    # Test without decay
    no_decay = echo.intensity_sum(apply_time_decay=False)
    safe_print(f"  Intensity without decay: {no_decay}")
    
    # Test with decay
    with_decay = echo.intensity_sum(apply_time_decay=True)
    safe_print(f"  Intensity with decay: {with_decay:.3f}")
    
    assert no_decay == 3.0
    assert with_decay < no_decay
    assert with_decay > 1.0  # At least the recent term
    
    safe_print("  ✅ Time-decay working correctly")

def test_cls_storage():
    """Test CLS storage functionality"""
    safe_print("\nTesting CLS storage functionality...")
    
    from kimera.geoid import init_geoid
    from kimera.cls import lattice_resolve, clear_stored_forms, get_stored_forms
    
    # Clear storage
    clear_stored_forms()
    
    # Create test geoids
    geo_a = init_geoid("Test A", "en", ["test"])
    geo_b = init_geoid("Test B", "en", ["test"])
    
    # First resolve
    intensity1 = lattice_resolve(geo_a, geo_b)
    safe_print(f"  First resolve intensity: {intensity1}")
    
    # Check storage
    stored = get_stored_forms()
    safe_print(f"  Stored forms: {len(stored)}")
    
    # Second resolve
    intensity2 = lattice_resolve(geo_a, geo_b)
    safe_print(f"  Second resolve intensity: {intensity2}")
    
    assert intensity1 == 1.1  # 1.0 + 0.1
    assert math.isclose(intensity2, 1.2, rel_tol=1e-9)  # 1.0 + 0.1 + 0.1
    assert len(stored) == 1
    
    safe_print("  ✅ CLS storage working correctly")

def test_cls_events():
    """Test cls_event tracking"""
    safe_print("\nTesting cls_event tracking...")
    
    from kimera.geoid import init_geoid
    from kimera.cls import lattice_resolve, clear_stored_forms, get_form_by_anchor
    
    # Clear storage
    clear_stored_forms()
    
    # Create test geoids
    geo_a = init_geoid("Event test A", "en", ["test"])
    geo_b = init_geoid("Event test B", "en", ["test"])
    
    # Multiple resolves
    lattice_resolve(geo_a, geo_b)
    lattice_resolve(geo_a, geo_b)
    lattice_resolve(geo_a, geo_b)
    
    # Check stored form
    anchor = f"{geo_a.gid}_{geo_b.gid}"
    form = get_form_by_anchor(anchor)
    
    # Count cls_event terms
    cls_events = [term for term in form.terms if term.get("symbol") == "cls_event"]
    safe_print(f"  Total cls_event terms: {len(cls_events)}")
    
    # Check timestamps
    for i, event in enumerate(cls_events):
        safe_print(f"    Event {i+1}: {event.get('event_type')} at {event.get('timestamp')}")
    
    assert len(cls_events) == 3
    assert all("timestamp" in event for event in cls_events)
    
    safe_print("  ✅ cls_event tracking working correctly")

def main():
    """Run quick tests"""
    safe_print("Quick Phase 19.2 Test")
    safe_print("=" * 25)
    
    try:
        test_time_decay()
        test_cls_storage()
        test_cls_events()
        
        safe_print("\nAll quick tests passed!")
        safe_print("Phase 19.2 implementation looks good!")
        return True
        
    except Exception as e:
        safe_print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)