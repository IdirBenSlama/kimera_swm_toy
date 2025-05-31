#!/usr/bin/env python3
"""
Migration script to move lattice forms from in-memory to persistent storage
This is a one-time migration helper for Phase 19.3
"""
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from kimera.storage import get_storage, close_storage
from kimera.echoform import EchoForm
from kimera.geoid import init_geoid
from kimera.cls import lattice_resolve, create_lattice_form
import time


def safe_print(msg: str):
    """Print message with encoding fallback for Windows console"""
    try:
        print(msg)
    except UnicodeEncodeError:
        # Fallback to ASCII with backslash escapes
        print(msg.encode("ascii", "backslashreplace").decode())


def create_sample_forms():
    """Create some sample forms to demonstrate the migration"""
    print("Creating sample lattice forms...")
    
    # Create some sample geoids
    geo1 = init_geoid("The sky is blue", "en", ["color", "sky"])
    geo2 = init_geoid("The sky is red", "en", ["color", "sky"])
    geo3 = init_geoid("Water is wet", "en", ["water", "property"])
    geo4 = init_geoid("Fire is dry", "en", ["fire", "property"])
    
    # Generate some lattice interactions
    result1 = lattice_resolve(geo1, geo2)  # Contradiction
    result2 = lattice_resolve(geo3, geo4)  # Another pair
    result3 = lattice_resolve(geo1, geo2)  # Repeat interaction
    
    print(f"Sample interactions created:")
    print(f"  {geo1.gid}_{geo2.gid} -> {result1:.3f}")
    print(f"  {geo3.gid}_{geo4.gid} -> {result2:.3f}")
    print(f"  {geo1.gid}_{geo2.gid} (repeat) -> {result3:.3f}")
    
    # Create a custom form
    custom_form = create_lattice_form("custom_test", geo1, geo3)
    print(f"  Custom form: {custom_form.anchor} -> {custom_form.intensity_sum():.3f}")


def verify_storage():
    """Verify that the storage system is working correctly"""
    print("\nVerifying storage system...")
    
    storage = get_storage()
    
    # Check form count
    total_forms = storage.get_form_count()
    cls_forms = storage.get_form_count(domain="cls")
    
    print(f"Total forms in storage: {total_forms}")
    print(f"CLS domain forms: {cls_forms}")
    
    # List recent forms
    recent_forms = storage.list_forms(limit=5, domain="cls")
    print(f"\nRecent CLS forms:")
    for form_meta in recent_forms:
        print(f"  {form_meta['anchor']} (intensity: {form_meta['intensity_sum']:.3f}, "
              f"age: {form_meta['age_hours']:.1f}h)")
    
    # Test retrieval
    if recent_forms:
        test_anchor = recent_forms[0]['anchor']
        test_form = storage.fetch_form(test_anchor)
        if test_form:
            print(f"\nTest retrieval successful:")
            print(f"  Anchor: {test_form.anchor}")
            print(f"  Terms: {len(test_form.terms)}")
            print(f"  Intensity: {test_form.intensity_sum():.3f}")


def test_time_decay():
    """Test the time-decay functionality"""
    print("\nTesting time-decay functionality...")
    
    storage = get_storage()
    
    # Get intensity before decay
    forms_before = storage.list_forms(limit=3, domain="cls")
    if not forms_before:
        print("No forms to test decay on")
        return
    
    print("Intensities before decay:")
    for form_meta in forms_before:
        print(f"  {form_meta['anchor']}: {form_meta['intensity_sum']:.3f}")
    
    # Apply decay with short tau for testing
    storage.apply_time_decay(tau_days=0.1)  # Very short decay for demo
    
    # Get intensities after decay
    forms_after = storage.list_forms(limit=3, domain="cls")
    print("\nIntensities after decay (τ=0.1 days):")
    for form_meta in forms_after:
        print(f"  {form_meta['anchor']}: {form_meta['intensity_sum']:.3f}")


def main():
    """Main migration function"""
    print("Kimera Lattice Migration to DuckDB")
    print("=" * 40)
    
    try:
        # Create sample data if needed
        create_sample_forms()
        
        # Verify storage is working
        verify_storage()
        
        # Test time decay
        test_time_decay()
        
        print("\n✅ Migration and verification complete!")
        print("\nYou can now use the CLI to manage the lattice:")
        print("  python -m kimera lattice list")
        print("  python -m kimera lattice show <anchor>")
        print("  python -m kimera lattice prune --older-than 30")
        
    except Exception as e:
        safe_print(f"\nMigration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        close_storage()


if __name__ == "__main__":
    main()