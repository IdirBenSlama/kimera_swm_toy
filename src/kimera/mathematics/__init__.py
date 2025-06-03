"""
Kimera Mathematics Module
========================

Mathematical foundations and algorithms for Kimera SWM.

This module provides rigorous mathematical implementations for:
- Spectral analysis of resonance operators
- Topological computations on semantic manifolds
- Algebraic operations on geoids
- Thermodynamic formalism

Phase 1 Implementation Status:
- ✅ Spectral analysis (spectral.py) - COMPLETE
- ⏳ Manifold operations - In Progress
- ⏳ Algebraic structures - Planned
- ⏳ Topological computations - Planned
"""

from .spectral import (
    build_resonance_matrix,
    compute_spectrum,
    resonance_spectrum,
    compute_spectral_gap,
    spectral_coherence_score,
)

__all__ = [
    "build_resonance_matrix",
    "compute_spectrum", 
    "resonance_spectrum",
    "compute_spectral_gap",
    "spectral_coherence_score",
]

__version__ = "0.1.0"