#!/usr/bin/env python3
"""
Demo script to test the reactor module functionality
"""

import sys
import os

# Add the src directory to Python path so we can import kimera
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from kimera.reactor import reactor_cycle, reactor_cycle_batched
from kimera.geoid import init_geoid
from kimera.echoform import EchoForm

def main():
    print("🧪 Testing Kimera Reactor Module")
    print("=" * 50)
    
    # Create some test geoids
    print("Creating test geoids...")
    geoids = []
    
    # Create a few test EchoForms and convert to Geoids
    test_terms = [
        [{"symbol": "test1", "role": "subject", "intensity": 0.8}],
        [{"symbol": "test2", "role": "predicate", "intensity": 0.6}],
        [{"symbol": "test3", "role": "object", "intensity": 0.7}],
        [{"symbol": "test4", "role": "subject", "intensity": 0.9}],
    ]
    
    for i, terms in enumerate(test_terms):
        form = EchoForm(anchor=f"test_form_{i}", domain="test")
        form.terms = terms
        # Convert EchoForm to text and create Geoid using init_geoid
        text_content = f"test_form_{i}: {terms[0]['symbol']}"
        geoid = init_geoid(text_content, lang="en", layers=["test"])
        geoids.append(geoid)
    
    print(f"Created {len(geoids)} test geoids")
    
    # Test single-threaded reactor cycle
    print("\n🔄 Testing single-threaded reactor cycle...")
    initial_scars = sum(len(g.scars) for g in geoids)
    print(f"Initial scars: {initial_scars}")
    
    reactor_cycle(geoids, cycles=1)
    
    final_scars = sum(len(g.scars) for g in geoids)
    print(f"Final scars: {final_scars}")
    print(f"New scars created: {final_scars - initial_scars}")
    
    # Test batched reactor cycle
    print("\n⚡ Testing batched reactor cycle...")
    stats = reactor_cycle_batched(geoids, chunk=2, verbose=True)
    
    print(f"\nBatched cycle stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n✅ Reactor module test completed successfully!")

if __name__ == "__main__":
    main()