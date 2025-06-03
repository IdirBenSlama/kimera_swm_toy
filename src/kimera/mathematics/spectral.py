"""kimera.mathematics.spectral
================================
Spectral analysis utilities for the **resonance operator** described in the
Mathematical Foundations (Section *2.2 Spectral Analysis*).

Phase-1 implementation focuses on providing a *numerically stable* and
*computationally efficient* reference implementation that other high-level
modules (e.g., experimental benchmarks, clustering utilities, interactive
notebooks) can rely on.

The module offers:

1. **build_resonance_matrix** – construct the NxN symmetric resonance matrix
   for a given list of `Geoid` objects.
2. **compute_spectrum** – eigendecomposition of the matrix with eigenvalues
   sorted in **descending** order.
3. **resonance_spectrum** – convenience wrapper combining steps-1 & 2.
4. **compute_spectral_gap** – calculate the *spectral gap* Δ = λ₁ − λ₂ which
   is used as a semantic coherence indicator (see Theorem 2.2).
5. **spectral_coherence_score** – normalised coherence metric in \[0,1\].

The implementation purposefully targets *small/medium* collections (up to a few
thousand geoids) typical of Phase-1 experiments.  For larger datasets use the
upcoming distributed implementation (Phase-3).
"""
from __future__ import annotations

from typing import Callable, List, Tuple
import numpy as np

try:
    # Local import to avoid heavy dependency if not available
    from numpy.linalg import eigh  # type: ignore
except ImportError:  # pragma: no cover
    # Fallback using scipy if numpy lacks LAPACK (rare)
    from scipy.linalg import eigh  # type: ignore  # noqa: F401

from ..geoid import Geoid  # Relative import to avoid circular deps
from ..resonance import resonance as _default_resonance

__all__ = [
    "build_resonance_matrix",
    "compute_spectrum",
    "resonance_spectrum",
    "compute_spectral_gap",
    "spectral_coherence_score",
]

###############################################################################
# Core utilities
###############################################################################

def build_resonance_matrix(
    geoids: List[Geoid],
    *,
    resonance_fn: Callable[[Geoid, Geoid], float] = _default_resonance,
) -> np.ndarray:
    """Construct the symmetric resonance matrix *R*.

    Args:
        geoids: List of geoids G₀…Gₙ₋₁.
        resonance_fn: Callable implementing *R(Gᵢ, Gⱼ)*.  If omitted the default
            implementation from ``kimera.resonance`` is used.
    Returns:
        ``(n, n)`` **float64** NumPy array where ``R[i, j] = resonance_fn(Gᵢ, Gⱼ)``.
    """
    n = len(geoids)
    if n == 0:
        raise ValueError("geoid list cannot be empty")

    R = np.zeros((n, n), dtype=np.float64)

    # Exploit symmetry – fill upper triangle and reflect.
    for i in range(n):
        R[i, i] = 1.0  # self-resonance is maximal by definition (Thm 2.1)
        for j in range(i + 1, n):
            score = resonance_fn(geoids[i], geoids[j])
            R[i, j] = score
            R[j, i] = score  # symmetric
    return R


def compute_spectrum(R: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Compute eigendecomposition of the resonance matrix.

    The matrix is symmetric so we can safely use ``numpy.linalg.eigh`` which is
    optimised for Hermitian matrices and guarantees real eigenvalues.

    Args:
        R: Square, symmetric resonance matrix.
    Returns:
        (eigenvalues, eigenvectors) where eigenvalues are sorted in **descending**
        order.  Eigenvectors are the corresponding columns of *V*.
    """
    if R.shape[0] != R.shape[1]:
        raise ValueError("Resonance matrix must be square")

    # eigh returns eigenvalues in **ascending** order – flip at the end.
    eigenvalues, eigenvectors = eigh(R)
    eigenvalues = eigenvalues[::-1]
    eigenvectors = eigenvectors[:, ::-1]
    return eigenvalues, eigenvectors


def resonance_spectrum(
    geoids: List[Geoid],
    *,
    resonance_fn: Callable[[Geoid, Geoid], float] = _default_resonance,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Convenience wrapper: builds *R* and returns (R, λ, Ψ).

    Returns:
        ``R`` – resonance matrix,
        ``λ`` – eigenvalues (descending),
        ``Ψ`` – eigenvectors (columns aligned with λ).
    """
    R = build_resonance_matrix(geoids, resonance_fn=resonance_fn)
    eigenvalues, eigenvectors = compute_spectrum(R)
    return R, eigenvalues, eigenvectors


def compute_spectral_gap(eigenvalues: np.ndarray) -> float:
    """Compute spectral gap Δ = λ₁ − λ₂.

    Args:
        eigenvalues: 1-D array of eigenvalues sorted descending.
    Returns:
        Spectral gap (``float``).  Returns ``0.0`` when fewer than two values.
    """
    if eigenvalues.size < 2:
        return 0.0
    return float(eigenvalues[0] - eigenvalues[1])


def spectral_coherence_score(eigenvalues: np.ndarray) -> float:
    """Return a normalised coherence score in the range ``[0, 1]``.

    Follows the heuristic:
        score = Δ / (Δ + λ₂)
    so that clearly separated clusters (large Δ) approach 1, while
    near-transitional states (Δ≈0) approach 0.
    """
    if eigenvalues.size < 2:
        return 0.0
    delta = eigenvalues[0] - eigenvalues[1]
    denom = delta + eigenvalues[1]
    if denom <= 0:
        return 0.0
    return float(np.clip(delta / denom, 0.0, 1.0))


###############################################################################
# Simple CLI / debug helper (optional import)
###############################################################################

if __name__ == "__main__":  # pragma: no cover
    import argparse, json, sys
    from pathlib import Path

    parser = argparse.ArgumentParser(description="Compute resonance spectrum for sample texts")
    parser.add_argument("texts", nargs="*", help="Raw texts to embed as geoids.")
    args = parser.parse_args()

    if not args.texts:
        print("Provide sample texts as positional arguments.", file=sys.stderr)
        sys.exit(1)

    # Lazy import to avoid heavy deps when module used only as library
    from ..geoid import init_geoid  # noqa: E402

    geoids = [init_geoid(t) for t in args.texts]
    R, lambdas, _ = resonance_spectrum(geoids)

    print("Resonance matrix R:\n", np.array2string(R, precision=3))
    print("Eigenvalues λ:", np.round(lambdas, 3))
    print("Spectral gap Δ:", round(compute_spectral_gap(lambdas), 3))
    print("Coherence score:", round(spectral_coherence_score(lambdas), 3))
