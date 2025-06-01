#!/usr/bin/env python3
"""
Simple test to verify reactor functionality works correctly
"""

import sys
import os

# Add the src directory to Python path so we can import kimera
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_reactor_basic():
    print("🧪 Testing Basic Reactor Functionality")
    print("=" * 40)
    
    try:
        from kimera.geoid import init_geoid
        from kimera.reactor import reactor_cycle
        from kimera.resonance import resonance
        
        # Create test geoids
        print("Creating test geoids...")
        geoids = []
        test_texts = [
            "The sky is blue",
            "Birds can fly", 
            "Water is wet",
            "Fire is hot"
        ]
        
        for text in test_texts:
            geoid = init_geoid(text, "en", ["test"])
            geoids.append(geoid)
            print(f"   Created geoid for: '{text}' (GID: {geoid.gid[:8]}...)")
        
        print(f"\n✅ Created {len(geoids)} geoids successfully!")
        
        # Test resonance between two geoids
        print("\nTesting resonance...")
        score = resonance(geoids[0], geoids[1])
        print(f"   Resonance between '{test_texts[0]}' and '{test_texts[1]}': {score:.3f}")
        
        # Test reactor cycle
        print("\nTesting reactor cycle...")
        initial_scars = sum(len(g.scars) for g in geoids)
        print(f"   Initial scars: {initial_scars}")
        
        stats = reactor_cycle(geoids, cycles=1)
        
        final_scars = sum(len(g.scars) for g in geoids)
        print(f"   Final scars: {final_scars}")
        print(f"   New scars created: {final_scars - initial_scars}")
        print(f"   Reactor stats: {stats}")
        
        print("✅ Reactor functionality working!")
        return True
        
    except Exception as e:
        print(f"❌ Error in reactor test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 Simple Reactor Test")
    print("=" * 50)
    
    success = test_reactor_basic()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Reactor test passed!")
    else:
        print("❌ Reactor test failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)