#!/usr/bin/env python3
"""
Simple test to verify Geoid creation works correctly
"""

import sys
import os

# Add the src directory to Python path so we can import kimera
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_geoid_creation():
    print("🧪 Testing Geoid Creation")
    print("=" * 30)
    
    try:
        from kimera.geoid import init_geoid
        
        # Test basic geoid creation
        print("Creating geoid with init_geoid...")
        geoid = init_geoid("Hello world", "en", ["test"])
        
        print(f"✅ Geoid created successfully!")
        print(f"   GID: {geoid.gid}")
        print(f"   Raw: {geoid.raw}")
        print(f"   Echo: {geoid.echo}")
        print(f"   Language: {geoid.lang_axis}")
        print(f"   Layers: {geoid.context_layers}")
        print(f"   Vector shape: {geoid.sem_vec.shape}")
        print(f"   Scars: {len(geoid.scars)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating geoid: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_echoform_creation():
    print("\n🧪 Testing EchoForm Creation")
    print("=" * 30)
    
    try:
        from kimera.echoform import EchoForm
        
        # Test basic echoform creation
        print("Creating EchoForm...")
        form = EchoForm(anchor="test_form", domain="test")
        form.add_term("hello", role="greeting", intensity=0.8)
        
        print(f"✅ EchoForm created successfully!")
        print(f"   Anchor: {form.anchor}")
        print(f"   Domain: {form.domain}")
        print(f"   Terms: {len(form.terms)}")
        print(f"   Intensity sum: {form.intensity_sum()}")
        print(f"   Trace: {form.trace_signature}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating EchoForm: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 Simple Kimera Test")
    print("=" * 50)
    
    success = True
    success &= test_geoid_creation()
    success &= test_echoform_creation()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)