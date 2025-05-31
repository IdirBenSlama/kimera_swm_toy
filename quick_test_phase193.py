#!/usr/bin/env python3
"""
Quick test of Phase 19.3 persistent storage functionality
"""
import sys
import os
sys.path.insert(0, 'src')

from kimera.storage import get_storage, close_storage
from kimera.geoid import init_geoid
from kimera.cls import lattice_resolve, create_lattice_form, get_stored_forms


def main():
    print("🧪 Quick Phase 19.3 Storage Test")
    print("=" * 35)
    
    try:
        # Clean up any existing test database
        if os.path.exists("test_quick.db"):
            os.remove("test_quick.db")
        
        # Initialize storage with test database
        storage = get_storage("test_quick.db")
        
        print("1. Creating test geoids...")
        geo_a = init_geoid("Quick test A", "en", ["test"])
        geo_b = init_geoid("Quick test B", "en", ["test"])
        print(f"   Created: {geo_a.gid[:8]}... and {geo_b.gid[:8]}...")
        
        print("2. Testing lattice resolve...")
        intensity1 = lattice_resolve(geo_a, geo_b)
        print(f"   First resolve: {intensity1}")
        
        intensity2 = lattice_resolve(geo_a, geo_b)
        print(f"   Second resolve: {intensity2}")
        
        print("3. Testing custom lattice form...")
        custom_form = create_lattice_form("quick_test", geo_a, geo_b)
        print(f"   Custom form intensity: {custom_form.intensity_sum():.3f}")
        
        print("4. Checking storage...")
        stored_forms = get_stored_forms()
        print(f"   Total stored forms: {len(stored_forms)}")
        
        # List forms using storage directly
        forms_list = storage.list_forms(limit=5)
        print("   Recent forms:")
        for form_meta in forms_list:
            print(f"     {form_meta['anchor']} (intensity: {form_meta['intensity_sum']:.3f})")
        
        print("5. Testing time-decay...")
        storage.apply_time_decay(tau_days=0.1)  # Very short for demo
        print("   Time-decay applied")
        
        # Check forms after decay
        forms_after = storage.list_forms(limit=5)
        print("   Forms after decay:")
        for form_meta in forms_after:
            print(f"     {form_meta['anchor']} (intensity: {form_meta['intensity_sum']:.3f})")
        
        print("\n✅ All Phase 19.3 storage tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        close_storage()
        # Clean up test database
        if os.path.exists("test_quick.db"):
            os.remove("test_quick.db")


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)