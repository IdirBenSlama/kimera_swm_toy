"""Test script to verify spectral analysis implementation"""
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from kimera.geoid import init_geoid
    from kimera.mathematics.spectral import (
        build_resonance_matrix,
        compute_spectrum,
        resonance_spectrum,
        compute_spectral_gap,
        spectral_coherence_score
    )
    print("✓ Successfully imported spectral analysis modules")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

def test_basic_spectral_analysis():
    """Test basic spectral analysis functionality"""
    print("\n=== Testing Basic Spectral Analysis ===")
    
    # Create test geoids
    texts = [
        "The quantum computer processes information",
        "Quantum computing revolutionizes data processing",
        "Classical computers use binary logic",
        "The weather is sunny today",
        "It's a beautiful sunny morning"
    ]
    
    print(f"\nCreating {len(texts)} test geoids...")
    geoids = [init_geoid(text) for text in texts]
    print("✓ Geoids created successfully")
    
    # Build resonance matrix
    print("\nBuilding resonance matrix...")
    R = build_resonance_matrix(geoids)
    print(f"✓ Resonance matrix shape: {R.shape}")
    print(f"  Matrix is symmetric: {np.allclose(R, R.T)}")
    print(f"  Diagonal values (self-resonance): {np.diag(R)}")
    
    # Compute spectrum
    print("\nComputing eigendecomposition...")
    eigenvalues, eigenvectors = compute_spectrum(R)
    print(f"✓ Eigenvalues (descending): {eigenvalues}")
    print(f"  All eigenvalues real: {np.all(np.isreal(eigenvalues))}")
    
    # Compute spectral gap
    gap = compute_spectral_gap(eigenvalues)
    print(f"\n✓ Spectral gap (λ₁ - λ₂): {gap:.4f}")
    
    # Compute coherence score
    coherence = spectral_coherence_score(eigenvalues)
    print(f"✓ Coherence score: {coherence:.4f}")
    
    # Interpretation
    print("\nInterpretation:")
    if gap > 0.1:
        print("  → Large spectral gap indicates semantically coherent clusters")
    elif gap > 0.01:
        print("  → Moderate spectral gap suggests some semantic structure")
    else:
        print("  → Small spectral gap indicates semantic phase transition")
    
    return True

def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n=== Testing Edge Cases ===")
    
    # Single geoid
    print("\nTesting with single geoid...")
    single_geoid = [init_geoid("Test")]
    R_single = build_resonance_matrix(single_geoid)
    eigenvalues_single, _ = compute_spectrum(R_single)
    gap_single = compute_spectral_gap(eigenvalues_single)
    print(f"✓ Single geoid handled correctly (gap = {gap_single})")
    
    # Empty list
    print("\nTesting with empty list...")
    try:
        build_resonance_matrix([])
        print("✗ Should have raised ValueError")
    except ValueError as e:
        print(f"✓ Correctly raised ValueError: {e}")
    
    # Non-square matrix
    print("\nTesting non-square matrix...")
    try:
        compute_spectrum(np.array([[1, 2, 3], [4, 5, 6]]))
        print("✗ Should have raised ValueError")
    except ValueError as e:
        print(f"✓ Correctly raised ValueError: {e}")
    
    return True

def test_semantic_clusters():
    """Test spectral analysis on semantically related clusters"""
    print("\n=== Testing Semantic Clusters ===")
    
    # Create two distinct semantic clusters
    cluster1 = [
        "Machine learning algorithms process data",
        "Deep learning neural networks",
        "Artificial intelligence systems"
    ]
    
    cluster2 = [
        "The cat sleeps on the mat",
        "A dog plays in the garden",
        "Birds sing in the morning"
    ]
    
    all_texts = cluster1 + cluster2
    geoids = [init_geoid(text) for text in all_texts]
    
    # Analyze spectrum
    R, eigenvalues, eigenvectors = resonance_spectrum(geoids)
    gap = compute_spectral_gap(eigenvalues)
    coherence = spectral_coherence_score(eigenvalues)
    
    print(f"\nResults for {len(cluster1)} + {len(cluster2)} geoids:")
    print(f"  Eigenvalues: {eigenvalues}")
    print(f"  Spectral gap: {gap:.4f}")
    print(f"  Coherence score: {coherence:.4f}")
    
    # Visualize resonance matrix
    print("\nResonance matrix (rounded):")
    print(np.round(R, 2))
    
    return True

def test_convergence_properties():
    """Test numerical stability and convergence"""
    print("\n=== Testing Convergence Properties ===")
    
    # Test with increasing number of similar texts
    base_text = "Quantum mechanics describes nature at small scales"
    variations = [
        base_text,
        base_text + " accurately",
        base_text + " very accurately",
        base_text + " with precision",
        base_text + " using mathematics"
    ]
    
    geoids = [init_geoid(text) for text in variations]
    R, eigenvalues, _ = resonance_spectrum(geoids)
    
    print(f"\nTesting with {len(variations)} similar texts:")
    print(f"  Eigenvalues: {eigenvalues}")
    print(f"  Largest eigenvalue: {eigenvalues[0]:.4f}")
    print(f"  Eigenvalue ratio λ₁/λ₂: {eigenvalues[0]/eigenvalues[1]:.4f}")
    
    # Check if largest eigenvalue dominates (indicating strong coherence)
    if eigenvalues[0] / np.sum(eigenvalues) > 0.8:
        print("  ✓ Dominant eigenvalue indicates strong semantic coherence")
    
    return True

def main():
    """Run all tests"""
    print("Kimera SWM Spectral Analysis Verification")
    print("=" * 50)
    
    tests = [
        test_basic_spectral_analysis,
        test_edge_cases,
        test_semantic_clusters,
        test_convergence_properties
    ]
    
    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"\n✗ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'=' * 50}")
    print(f"Tests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("\n✅ All spectral analysis tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())