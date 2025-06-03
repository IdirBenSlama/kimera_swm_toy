"""
Unit tests for kimera.mathematics.spectral module

Tests the spectral analysis implementation against the mathematical
foundations defined in Section 2.2 of the research documentation.
"""
import sys
from pathlib import Path
# Ensure we use the local kimera module
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
import numpy as np
from unittest.mock import Mock, patch

from kimera.geoid import Geoid, init_geoid
from kimera.mathematics.spectral import (
    build_resonance_matrix,
    compute_spectrum,
    resonance_spectrum,
    compute_spectral_gap,
    spectral_coherence_score,
)


class TestBuildResonanceMatrix:
    """Test resonance matrix construction"""
    
    def test_empty_list_raises_error(self):
        """Empty geoid list should raise ValueError"""
        with pytest.raises(ValueError, match="geoid list cannot be empty"):
            build_resonance_matrix([])
    
    def test_single_geoid(self):
        """Single geoid should produce 1x1 matrix with value 1.0"""
        geoid = init_geoid("test")
        R = build_resonance_matrix([geoid])
        assert R.shape == (1, 1)
        assert R[0, 0] == 1.0
    
    def test_matrix_symmetry(self):
        """Resonance matrix must be symmetric"""
        geoids = [init_geoid(f"text {i}") for i in range(5)]
        R = build_resonance_matrix(geoids)
        assert np.allclose(R, R.T), "Matrix is not symmetric"
    
    def test_diagonal_values(self):
        """Diagonal values (self-resonance) should be 1.0"""
        geoids = [init_geoid(f"text {i}") for i in range(4)]
        R = build_resonance_matrix(geoids)
        assert np.allclose(np.diag(R), 1.0), "Diagonal values are not 1.0"
    
    def test_custom_resonance_function(self):
        """Should use custom resonance function if provided"""
        def mock_resonance(g1, g2):
            return 0.5 if g1.gid != g2.gid else 1.0
        
        geoids = [init_geoid(f"text {i}") for i in range(3)]
        R = build_resonance_matrix(geoids, resonance_fn=mock_resonance)
        
        # Check off-diagonal values
        for i in range(3):
            for j in range(3):
                if i == j:
                    assert R[i, j] == 1.0
                else:
                    assert R[i, j] == 0.5


class TestComputeSpectrum:
    """Test eigendecomposition computation"""
    
    def test_non_square_matrix_raises_error(self):
        """Non-square matrix should raise ValueError"""
        R = np.array([[1, 2, 3], [4, 5, 6]])
        with pytest.raises(ValueError, match="must be square"):
            compute_spectrum(R)
    
    def test_eigenvalues_descending_order(self):
        """Eigenvalues should be in descending order"""
        # Create a simple symmetric matrix
        R = np.array([[2, 1, 0], [1, 2, 1], [0, 1, 2]])
        eigenvalues, _ = compute_spectrum(R)
        assert np.all(np.diff(eigenvalues) <= 0), "Eigenvalues not in descending order"
    
    def test_eigenvalues_real(self):
        """All eigenvalues should be real for symmetric matrix"""
        R = np.random.rand(5, 5)
        R = (R + R.T) / 2  # Make symmetric
        eigenvalues, _ = compute_spectrum(R)
        assert np.all(np.isreal(eigenvalues)), "Eigenvalues contain imaginary parts"
    
    def test_eigenvector_orthogonality(self):
        """Eigenvectors should be orthonormal"""
        R = np.random.rand(4, 4)
        R = (R + R.T) / 2  # Make symmetric
        _, eigenvectors = compute_spectrum(R)
        
        # Check orthonormality
        I = eigenvectors.T @ eigenvectors
        assert np.allclose(I, np.eye(4), atol=1e-10), "Eigenvectors not orthonormal"


class TestSpectralGap:
    """Test spectral gap computation"""
    
    def test_empty_eigenvalues(self):
        """Empty eigenvalue array should return 0.0"""
        assert compute_spectral_gap(np.array([])) == 0.0
    
    def test_single_eigenvalue(self):
        """Single eigenvalue should return 0.0"""
        assert compute_spectral_gap(np.array([5.0])) == 0.0
    
    def test_spectral_gap_calculation(self):
        """Spectral gap should be λ₁ - λ₂"""
        eigenvalues = np.array([5.0, 3.0, 1.0, 0.5])
        gap = compute_spectral_gap(eigenvalues)
        assert gap == 2.0
    
    def test_negative_eigenvalues(self):
        """Should handle negative eigenvalues correctly"""
        eigenvalues = np.array([1.0, -2.0, -3.0])
        gap = compute_spectral_gap(eigenvalues)
        assert gap == 3.0  # 1.0 - (-2.0) = 3.0


class TestSpectralCoherenceScore:
    """Test coherence score computation"""
    
    def test_empty_eigenvalues(self):
        """Empty eigenvalue array should return 0.0"""
        assert spectral_coherence_score(np.array([])) == 0.0
    
    def test_single_eigenvalue(self):
        """Single eigenvalue should return 0.0"""
        assert spectral_coherence_score(np.array([5.0])) == 0.0
    
    def test_coherence_bounds(self):
        """Coherence score should be in [0, 1]"""
        # Test various eigenvalue configurations
        test_cases = [
            np.array([10.0, 1.0, 0.1]),  # Large gap
            np.array([2.0, 1.9, 0.1]),    # Small gap
            np.array([1.0, 1.0, 0.5]),    # No gap
            np.array([5.0, 0.0, -1.0]),   # Zero second eigenvalue
        ]
        
        for eigenvalues in test_cases:
            score = spectral_coherence_score(eigenvalues)
            assert 0.0 <= score <= 1.0, f"Score {score} out of bounds"
    
    def test_coherence_formula(self):
        """Test the coherence formula: Δ / (Δ + λ₂)"""
        eigenvalues = np.array([5.0, 2.0, 1.0])
        gap = 5.0 - 2.0  # 3.0
        expected = gap / (gap + 2.0)  # 3.0 / 5.0 = 0.6
        assert np.isclose(spectral_coherence_score(eigenvalues), expected)


class TestResonanceSpectrum:
    """Test the convenience wrapper function"""
    
    def test_returns_correct_tuple(self):
        """Should return (R, eigenvalues, eigenvectors)"""
        geoids = [init_geoid(f"text {i}") for i in range(3)]
        R, eigenvalues, eigenvectors = resonance_spectrum(geoids)
        
        assert R.shape == (3, 3)
        assert eigenvalues.shape == (3,)
        assert eigenvectors.shape == (3, 3)
    
    def test_consistency_with_individual_functions(self):
        """Results should match calling functions individually"""
        geoids = [init_geoid(f"text {i}") for i in range(4)]
        
        # Using wrapper
        R1, ev1, evec1 = resonance_spectrum(geoids)
        
        # Using individual functions
        R2 = build_resonance_matrix(geoids)
        ev2, evec2 = compute_spectrum(R2)
        
        assert np.allclose(R1, R2)
        assert np.allclose(ev1, ev2)
        assert np.allclose(np.abs(evec1), np.abs(evec2))  # Eigenvectors can differ by sign


class TestMathematicalProperties:
    """Test mathematical properties from the foundations document"""
    
    def test_theorem_2_1_symmetry(self):
        """Theorem 2.1: R(G₁, G₂) = R(G₂, G₁)"""
        geoids = [init_geoid("quantum"), init_geoid("classical")]
        R = build_resonance_matrix(geoids)
        assert R[0, 1] == R[1, 0], "Resonance operator not symmetric"
    
    def test_theorem_2_1_self_resonance(self):
        """Theorem 2.1: R(G, G) = 1 (assuming no self-scars)"""
        geoid = init_geoid("test")
        R = build_resonance_matrix([geoid])
        assert R[0, 0] == 1.0, "Self-resonance not equal to 1"
    
    def test_theorem_2_2_spectral_gap_interpretation(self):
        """Theorem 2.2: Spectral gap indicates semantic coherence"""
        # Create coherent cluster
        coherent = [init_geoid(f"quantum physics {i}") for i in range(3)]
        R_coherent, ev_coherent, _ = resonance_spectrum(coherent)
        gap_coherent = compute_spectral_gap(ev_coherent)
        
        # Create mixed cluster
        mixed = [
            init_geoid("quantum physics"),
            init_geoid("cooking recipe"),
            init_geoid("weather forecast")
        ]
        R_mixed, ev_mixed, _ = resonance_spectrum(mixed)
        gap_mixed = compute_spectral_gap(ev_mixed)
        
        # Coherent cluster should have larger spectral gap
        assert gap_coherent > gap_mixed, "Coherent cluster should have larger spectral gap"


@pytest.mark.parametrize("n_geoids", [10, 50, 100])
def test_performance_scaling(n_geoids):
    """Test that operations scale reasonably with input size"""
    import time
    
    geoids = [init_geoid(f"text {i}") for i in range(n_geoids)]
    
    start = time.time()
    R, eigenvalues, eigenvectors = resonance_spectrum(geoids)
    elapsed = time.time() - start
    
    # Basic sanity checks
    assert R.shape == (n_geoids, n_geoids)
    assert eigenvalues.shape == (n_geoids,)
    assert eigenvectors.shape == (n_geoids, n_geoids)
    
    # Performance should be reasonable (< 1 second for 100 geoids)
    if n_geoids <= 100:
        assert elapsed < 1.0, f"Too slow for {n_geoids} geoids: {elapsed:.2f}s"