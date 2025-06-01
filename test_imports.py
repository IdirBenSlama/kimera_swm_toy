#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

print("Testing imports...")

try:
    print("1. Importing entropy...")
    from kimera.entropy import calculate_term_entropy, calculate_relationship_entropy, adaptive_tau
    print("✅ entropy imports OK")
except Exception as e:
    print(f"❌ entropy import error: {e}")

try:
    print("2. Importing identity...")
    from kimera.identity import Identity
    print("✅ identity import OK")
except Exception as e:
    print(f"❌ identity import error: {e}")

try:
    print("3. Importing echoform...")
    from kimera.echoform import EchoForm
    print("✅ echoform import OK")
except Exception as e:
    print(f"❌ echoform import error: {e}")

try:
    print("4. Importing storage...")
    from kimera.storage import LatticeStorage
    print("✅ storage import OK")
except Exception as e:
    print(f"❌ storage import error: {e}")

print("Import test complete.")