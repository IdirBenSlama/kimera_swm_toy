#!/usr/bin/env python3
"""
Minimal test to check if basic imports work
"""
import sys
sys.path.insert(0, 'src')

print("Testing basic imports...")

try:
    from kimera.echoform import EchoForm
    print("✓ EchoForm import successful")
except Exception as e:
    print(f"✗ EchoForm import failed: {e}")
    sys.exit(1)

try:
    from kimera.identity import Identity
    print("✓ Identity import successful")
except Exception as e:
    print(f"✗ Identity import failed: {e}")
    sys.exit(1)

try:
    from kimera.entropy import calculate_shannon_entropy
    print("✓ Entropy import successful")
except Exception as e:
    print(f"✗ Entropy import failed: {e}")
    sys.exit(1)

print("\nTesting basic functionality...")

try:
    # Test EchoForm
    echo = EchoForm()
    echo.add_term("test", intensity=2.0)
    intensity = echo.intensity_sum()
    print(f"✓ EchoForm basic test - intensity: {intensity}")
except Exception as e:
    print(f"✗ EchoForm test failed: {e}")
    sys.exit(1)

try:
    # Test Identity
    identity = Identity(content="test content")
    print(f"✓ Identity basic test - ID: {identity.id}")
except Exception as e:
    print(f"✗ Identity test failed: {e}")
    sys.exit(1)

try:
    # Test entropy
    entropy = calculate_shannon_entropy([1.0, 2.0, 3.0])
    print(f"✓ Entropy basic test - value: {entropy:.3f}")
except Exception as e:
    print(f"✗ Entropy test failed: {e}")
    sys.exit(1)

print("\n✓ All basic tests passed! Core functionality is working.")
print("Status: READY FOR ROADMAP IMPLEMENTATION")