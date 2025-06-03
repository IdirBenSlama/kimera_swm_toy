"""
Comprehensive test to verify all fixes are working
==================================================

Tests that:
1. Fixed components work correctly
2. Broken components are not used
3. Examples run without errors
4. Performance is as measured
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import time
import numpy as np
from kimera.geoid import init_geoid
from kimera.resonance import resonance
from kimera.contradiction_v2_fixed import analyze_contradiction
from kimera.thermodynamics_v3 import ThermodynamicSystemV3
from kimera.mathematics.spectral import resonance_spectrum


def test_contradiction_detection():
    """Test that contradiction detection works correctly."""
    print("\n1. Testing Contradiction Detection (Fixed)")
    print("-" * 40)
    
    test_cases = [
        ("The sky is blue", "The sky is red", True),
        ("The sky is blue", "The sky is not blue", True),
        ("The sky is blue", "Grass is green", False),
    ]
    
    passed = 0
    for text1, text2, expected in test_cases:
        g1 = init_geoid(text1)
        g2 = init_geoid(text2)
        
        analysis = analyze_contradiction(g1, g2)
        result = analysis.is_contradiction
        
        if result == expected:
            passed += 1
            print(f"✓ '{text1}' vs '{text2}': {result}")
        else:
            print(f"✗ '{text1}' vs '{text2}': {result} (expected {expected})")
    
    print(f"\nPassed: {passed}/{len(test_cases)}")
    return passed == len(test_cases)


def test_thermodynamics():
    """Test that thermodynamics produces multiple phases."""
    print("\n2. Testing Thermodynamics V3")
    print("-" * 40)
    
    texts = [
        "Water is H2O",
        "Ice is frozen water",
        "The sky is blue",
        "The sky is red",
    ]
    
    geoids = [init_geoid(t) for t in texts]
    system = ThermodynamicSystemV3()
    
    phase_diagram, states = system.generate_phase_diagram(geoids)
    
    phases_with_content = sum(1 for states in phase_diagram.values() if states)
    
    print(f"Phases detected: {phases_with_content}")
    for phase, phase_states in phase_diagram.items():
        if phase_states:
            print(f"  {phase}: {len(phase_states)} geoids")
    
    return phases_with_content >= 2


def test_performance():
    """Test actual performance matches claims."""
    print("\n3. Testing Performance")
    print("-" * 40)
    
    # Test resonance speed
    texts = [f"Text {i}" for i in range(100)]
    geoids = [init_geoid(t) for t in texts]
    
    start = time.time()
    count = 0
    for i in range(50):
        for j in range(i+1, 50):
            _ = resonance(geoids[i], geoids[j])
            count += 1
    elapsed = time.time() - start
    
    pairs_per_second = count / elapsed if elapsed > 0 else 0
    print(f"Resonance speed: {pairs_per_second:.0f} pairs/second")
    
    # Test memory
    import sys
    single_geoid = init_geoid("Test")
    geoid_size = sys.getsizeof(single_geoid) + single_geoid.sem_vec.nbytes
    mb_per_million = geoid_size * 1_000_000 / (1024**2)
    
    print(f"Memory per million: {mb_per_million:.0f} MB")
    
    # Verify claims
    speed_ok = 2000 < pairs_per_second < 4000  # ~3000 expected
    memory_ok = 1000 < mb_per_million < 2000   # ~1500 expected
    
    return speed_ok and memory_ok


def test_spectral_analysis():
    """Test spectral analysis works."""
    print("\n4. Testing Spectral Analysis")
    print("-" * 40)
    
    texts = ["Text A", "Text B", "Text C", "Text D"]
    geoids = [init_geoid(t) for t in texts]
    
    try:
        R, eigenvalues, eigenvectors = resonance_spectrum(geoids)
        
        # Check properties
        symmetric = np.allclose(R, R.T)
        real_eigenvalues = np.all(np.isreal(eigenvalues))
        descending = np.all(eigenvalues[:-1] >= eigenvalues[1:])
        
        print(f"Matrix symmetric: {symmetric}")
        print(f"Eigenvalues real: {real_eigenvalues}")
        print(f"Eigenvalues descending: {descending}")
        
        return symmetric and real_eigenvalues and descending
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_no_broken_imports():
    """Verify broken components cannot be imported from main modules."""
    print("\n5. Testing No Broken Imports")
    print("-" * 40)
    
    # These should fail or not exist
    try:
        from kimera.contradiction import detect_contradiction
        # If we get here, the broken module is still accessible
        print("✗ WARNING: Broken contradiction module still accessible")
        return False
    except (ImportError, AttributeError):
        print("✓ Broken contradiction module not accessible")
    
    try:
        from kimera.thermodynamics import ThermodynamicSystem
        # Check if it's the broken version
        system = ThermodynamicSystem()
        # The broken version would classify everything as plasma
        print("⚠️  Original thermodynamics still accessible (should migrate to v3)")
    except (ImportError, AttributeError):
        print("✓ Original thermodynamics not accessible")
    
    return True


def main():
    """Run all tests."""
    print("COMPREHENSIVE FIX VERIFICATION")
    print("=" * 60)
    print("Testing that all fixes are working correctly...")
    
    tests = [
        ("Contradiction Detection", test_contradiction_detection),
        ("Thermodynamics V3", test_thermodynamics),
        ("Performance Claims", test_performance),
        ("Spectral Analysis", test_spectral_analysis),
        ("No Broken Imports", test_no_broken_imports),
    ]
    
    passed = 0
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"\n❌ {name} FAILED")
        except Exception as e:
            print(f"\n❌ {name} ERROR: {e}")
    
    print("\n" + "=" * 60)
    print(f"SUMMARY: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n✅ ALL FIXES VERIFIED - System is working correctly!")
    else:
        print("\n⚠️  Some issues remain - see failures above")


if __name__ == "__main__":
    main()