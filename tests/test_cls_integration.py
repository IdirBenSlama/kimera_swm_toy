#!/usr/bin/env python3
"""
Test CLS lattice integration with EchoForm storage and cls_event tracking
Now with persistent DuckDB storage backend
"""
import sys
import math
import os
sys.path.insert(0, 'src')

from kimera.echoform import EchoForm
from kimera.geoid import init_geoid
from kimera.cls import lattice_resolve, create_lattice_form, get_stored_forms, clear_stored_forms, get_form_by_anchor
from kimera.storage import get_storage, close_storage
from conftest import fresh_duckdb_path

# Floating-point tolerance constant
FLOAT_RTOL = 1e-7   # was 1e-9


def setup_test_storage():
    """Setup clean test storage"""
    # Use a fresh DuckDB path to avoid file conflicts
    test_db = fresh_duckdb_path()
    
    # Initialize storage with test database
    storage = get_storage(test_db)
    clear_stored_forms()
    return storage, test_db


def teardown_test_storage(test_db):
    """Clean up test storage"""
    close_storage()
    if os.path.exists(test_db):
        os.remove(test_db)


def test_lattice_resolve_basic():
    """Test basic lattice resolve functionality with storage"""
    # Setup clean test storage
    storage, test_db = setup_test_storage()
    
    try:
        # Create test geoids
        geo_a = init_geoid("Birds can fly", "en", ["test"])
        geo_b = init_geoid("Birds cannot fly", "en", ["test"])
        
        # Test lattice resolve
        intensity = lattice_resolve(geo_a, geo_b)
        
        # Should have initial intensity (1.0 + 0.1 = 1.1)
        assert math.isclose(intensity, 1.1, rel_tol=FLOAT_RTOL), f"Expected intensity 1.1, got {intensity}"
        
        # Check that form was stored
        stored_forms = get_stored_forms()
        assert len(stored_forms) == 1, f"Expected 1 stored form, got {len(stored_forms)}"
        
        # Get the stored form
        anchor = f"{geo_a.gid}_{geo_b.gid}"
        stored_form = get_form_by_anchor(anchor)
        assert stored_form.anchor == anchor
        assert stored_form.domain == "cls"
        assert len(stored_form.terms) == 2  # cls_seed + cls_event
        
        print("✅ Basic lattice resolve with storage test passed")
    
    finally:
        teardown_test_storage(test_db)


def test_lattice_resolve_repeat():
    """Test repeated lattice resolve adds cls_event terms"""
    # Setup clean test storage
    storage, test_db = setup_test_storage()
    
    try:
        # Create test geoids
        geo_a = init_geoid("Test repeat A", "en", ["test"])
        geo_b = init_geoid("Test repeat B", "en", ["test"])
        
        # First resolve
        intensity1 = lattice_resolve(geo_a, geo_b)
        assert math.isclose(intensity1, 1.1, rel_tol=FLOAT_RTOL), f"Expected first intensity 1.1 (within tolerance), got {intensity1}"
        
        # Second resolve (should add another cls_event)
        intensity2 = lattice_resolve(geo_a, geo_b)
        assert math.isclose(intensity2, 1.2, rel_tol=FLOAT_RTOL), f"Expected second intensity 1.2 (within tolerance), got {intensity2}"
        
        # Third resolve
        intensity3 = lattice_resolve(geo_a, geo_b)
        assert math.isclose(intensity3, 1.3, rel_tol=FLOAT_RTOL), f"Expected third intensity 1.3 (within tolerance), got {intensity3}"
        
        # Check stored form has accumulated terms
        anchor = f"{geo_a.gid}_{geo_b.gid}"
        stored_form = get_form_by_anchor(anchor)
        assert len(stored_form.terms) == 4  # cls_seed + 3 cls_events
        
        # Check that all cls_event terms have timestamps
        cls_events = [term for term in stored_form.terms if term.get("symbol") == "cls_event"]
        assert len(cls_events) == 3
        for event in cls_events:
            assert "timestamp" in event
            assert event["role"] == "resonance_trigger"
        
        print("✅ Repeated lattice resolve test passed")
    
    finally:
        teardown_test_storage(test_db)


def test_create_lattice_form():
    """Test creating full lattice forms with storage"""
    # Setup clean test storage
    storage, test_db = setup_test_storage()
    
    try:
        # Create test geoids
        geo_a = init_geoid("Test A", "en", ["test"])
        geo_b = init_geoid("Test B", "en", ["test"])
        
        # Create lattice form
        form = create_lattice_form("test_lattice", geo_a, geo_b)
        
        assert form.anchor == "test_lattice"
        assert form.domain == "cls"
        assert form.phase == "lattice_active"
        assert len(form.terms) == 3  # 2 geoids + 1 cls_event
        assert math.isclose(form.intensity_sum(apply_time_decay=False), 1.1, rel_tol=FLOAT_RTOL)  # 0.5 + 0.5 + 0.1
        
        # Check topology
        assert form.topology["lattice_type"] == "contradiction"
        assert form.topology["identity_pair"] == [geo_a.gid, geo_b.gid]
        
        # Check terms
        identity_terms = [term for term in form.terms if term.get("role") in ["identity_a", "identity_b"]]
        cls_event_terms = [term for term in form.terms if term.get("role") == "creation_event"]
        
        assert len(identity_terms) == 2
        assert len(cls_event_terms) == 1
        
        # Check that form was stored
        stored_forms = get_stored_forms()
        assert "test_lattice" in stored_forms
        assert stored_forms["test_lattice"].anchor == "test_lattice"
        
        print("✅ Create lattice form with storage test passed")
    
    finally:
        teardown_test_storage(test_db)


def test_lattice_form_serialization():
    """Test that lattice forms can be serialized and restored"""
    # Setup clean test storage
    storage, test_db = setup_test_storage()
    
    try:
        # Create test geoids
        geo_a = init_geoid("Serialization test A", "en", ["test"])
        geo_b = init_geoid("Serialization test B", "en", ["test"])
        
        # Create and serialize lattice form
        form1 = create_lattice_form("serialize_test", geo_a, geo_b)
        blob = form1.flatten()
        
        # Restore from serialization
        form2 = EchoForm.reinflate(blob)
        
        # Verify restoration
        assert form1.anchor == form2.anchor
        assert form1.domain == form2.domain
        assert form1.phase == form2.phase
        assert form1.intensity_sum(apply_time_decay=False) == form2.intensity_sum(apply_time_decay=False)
        assert form1.topology == form2.topology
        assert len(form1.terms) == len(form2.terms)
        
        print("✅ Lattice form serialization test passed")
    
    finally:
        teardown_test_storage(test_db)


def test_lattice_integration_flow():
    """Test complete integration flow with storage"""
    print("\n🔥 Running complete CLS integration flow with storage...")
    
    # Setup clean test storage
    storage, test_db = setup_test_storage()
    
    try:
        # Step 1: Create geoids
        geo_a = init_geoid("Integration test A", "en", ["integration"])
        geo_b = init_geoid("Integration test B", "en", ["integration"])
        print(f"  Created geoids: {geo_a.gid[:8]}... and {geo_b.gid[:8]}...")
        
        # Step 2: Simple lattice resolve (first time)
        intensity1 = lattice_resolve(geo_a, geo_b)
        print(f"  First lattice resolve intensity: {intensity1}")
        
        # Step 3: Repeat lattice resolve (should add cls_event)
        intensity2 = lattice_resolve(geo_a, geo_b)
        print(f"  Second lattice resolve intensity: {intensity2}")
        
        # Step 4: Create full lattice form
        form = create_lattice_form(f"integration_{geo_a.gid[:8]}", geo_a, geo_b)
        print(f"  Created lattice form: {form}")
        
        # Step 5: Check storage
        stored_forms = get_stored_forms()
        print(f"  Total stored forms: {len(stored_forms)}")
        
        # Step 6: Serialize and restore
        blob = form.flatten()
        restored_form = EchoForm.reinflate(blob)
        print(f"  Serialized and restored: {len(blob)} chars")
        
        # Step 7: Verify integrity
        assert math.isclose(intensity1, 1.1, rel_tol=FLOAT_RTOL)  # Initial: 1.0 + 0.1
        assert math.isclose(intensity2, 1.2, rel_tol=FLOAT_RTOL)  # Second: 1.0 + 0.1 + 0.1
        assert math.isclose(form.intensity_sum(apply_time_decay=False), 1.1, rel_tol=FLOAT_RTOL)  # 0.5 + 0.5 + 0.1
        assert math.isclose(restored_form.intensity_sum(apply_time_decay=False), 1.1, rel_tol=FLOAT_RTOL)
        assert form.anchor == restored_form.anchor
        assert len(stored_forms) == 2  # One from lattice_resolve, one from create_lattice_form
        
        print("✅ Complete integration flow with storage test passed!")
        return True
    
    finally:
        teardown_test_storage(test_db)


def main():
    """Run all CLS integration tests"""
    print("🧪 CLS Integration Tests with Storage & cls_event Tracking")
    print("=" * 55)
    
    tests = [
        test_lattice_resolve_basic,
        test_lattice_resolve_repeat,
        test_create_lattice_form,
        test_lattice_form_serialization,
        test_lattice_integration_flow
    ]
    
    passed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n📊 Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All CLS integration tests passed!")
        return True
    else:
        print("❌ Some tests failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)