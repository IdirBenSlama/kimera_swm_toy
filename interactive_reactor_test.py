#!/usr/bin/env python3
"""
Interactive test script for exploring reactor functionality
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Now you can import and use any kimera module
from kimera.reactor import reactor_cycle, reactor_cycle_batched, random_pairs
from kimera.geoid import init_geoid
from kimera.echoform import EchoForm
from kimera.resonance import resonance, THRESH
from kimera.scar import create_scar

print("🚀 Kimera modules imported successfully!")
print("Available functions:")
print("  - reactor_cycle(geoids, cycles=1)")
print("  - reactor_cycle_batched(geoids, chunk=200, verbose=True)")
print("  - random_pairs(sequence)")
print("  - resonance(geoid1, geoid2)")
print("  - create_scar(geoid1, geoid2, intensity)")
print("  - Geoid(text, lang, layers) - use init_geoid function")
print("  - EchoForm(anchor, domain)")

print(f"\nResonance threshold: {THRESH}")

# Example usage
print("\n📝 Example: Creating a simple geoid")
form = EchoForm(anchor="example", domain="test")
form.terms = [{"symbol": "hello", "role": "greeting", "intensity": 0.8}]
# Create geoid from text content using init_geoid
text_content = f"example: hello"
geoid = init_geoid(text_content, lang="en", layers=["test"])
print(f"Created geoid with gid: {geoid.gid}")
print(f"Geoid has {len(geoid.scars)} scars")

print("\n🎯 Ready for interactive exploration!")
print("Try creating more geoids and running reactor cycles...")