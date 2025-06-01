#!/usr/bin/env python3
"""
Check basic imports step by step
"""
import sys
import os
sys.path.insert(0, 'src')

print("=== Checking Basic Imports ===")
print(f"Current working directory: {os.getcwd()}")
print(f"Python path includes: {sys.path[0]}")

# Check if src/kimera exists
kimera_path = os.path.join('src', 'kimera')
print(f"Kimera path exists: {os.path.exists(kimera_path)}")
if os.path.exists(kimera_path):
    print(f"Kimera contents: {os.listdir(kimera_path)}")

# Try importing step by step
try:
    print("\n1. Importing kimera package...")
    import kimera
    print("✅ kimera package imported")
except Exception as e:
    print(f"❌ kimera package import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\n2. Importing entropy...")
    from kimera import entropy
    print("✅ entropy imported")
except Exception as e:
    print(f"❌ entropy import failed: {e}")

try:
    print("\n3. Importing identity...")
    from kimera import identity
    print("✅ identity module imported")
except Exception as e:
    print(f"❌ identity import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\n4. Importing Identity class...")
    from kimera.identity import Identity
    print("✅ Identity class imported")
except Exception as e:
    print(f"❌ Identity class import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\n5. Importing EchoForm...")
    from kimera.echoform import EchoForm
    print("✅ EchoForm imported")
except Exception as e:
    print(f"❌ EchoForm import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\n6. Importing LatticeStorage...")
    from kimera.storage import LatticeStorage
    print("✅ LatticeStorage imported")
except Exception as e:
    print(f"❌ LatticeStorage import failed: {e}")
    import traceback
    traceback.print_exc()