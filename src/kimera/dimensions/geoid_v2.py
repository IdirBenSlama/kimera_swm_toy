"""
Enhanced Geoid Model with Full SWM Dimensions

This module implements the GeoidV2 model, which extends the original Geoid
with comprehensive dimensional analysis capabilities for the Spherical Wavelet Model (SWM).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from enum import Enum
import hashlib
import json


class DimensionType(Enum):
    """Types of dimensions in the SWM model"""
    LINGUISTIC = "linguistic"
    CULTURAL = "cultural"
    METAPHORICAL = "metaphorical"
    STRUCTURAL = "structural"
    HISTORICAL = "historical"
    CONTEXTUAL = "contextual"
    SENSORY = "sensory"
    EMOTIONAL = "emotional"
    SEMANTIC = "semantic"
    SYMBOLIC = "symbolic"
    TEMPORAL = "temporal"
    SPATIAL = "spatial"
    COGNITIVE = "cognitive"
    SOCIAL = "social"
    PRAGMATIC = "pragmatic"


@dataclass
class GeoidDimension:
    """Represents a single dimension of a Geoid"""
    type: DimensionType
    value: Any
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    extracted_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_vector(self) -> np.ndarray:
        """Convert dimension to vector representation"""
        if isinstance(self.value, np.ndarray):
            return self.value
        elif isinstance(self.value, (list, tuple)):
            return np.array(self.value)
        elif isinstance(self.value, dict):
            # For dict values, create a hash-based vector
            hash_str = json.dumps(self.value, sort_keys=True)
            hash_bytes = hashlib.sha256(hash_str.encode()).digest()
            # Convert to normalized vector
            vec = np.frombuffer(hash_bytes[:32], dtype=np.float32)
            return vec / np.linalg.norm(vec)
        else:
            # For scalar values, create a one-hot style vector
            vec = np.zeros(16)
            vec[hash(str(self.value)) % 16] = float(self.value) if isinstance(self.value, (int, float)) else 1.0
            return vec


@dataclass
class GeoidV2:
    """
    Enhanced Geoid with full SWM dimensional analysis
    
    This extends the original Geoid model with:
    - Multi-dimensional analysis across 15 dimension types
    - Spherical wavelet decomposition
    - Enhanced vector representations
    - Dimensional interaction modeling
    - Temporal evolution tracking
    """
    # Core fields from original Geoid
    raw: str
    echo: str
    gid: str
    lang_axis: str
    context_layers: List[str]
    sem_vec: np.ndarray
    sym_vec: np.ndarray
    vdr: float
    scars: List[str] = field(default_factory=list)
    
    # Enhanced dimensional fields
    dimensions: Dict[DimensionType, GeoidDimension] = field(default_factory=dict)
    wavelet_coeffs: Dict[str, np.ndarray] = field(default_factory=dict)
    interaction_matrix: Optional[np.ndarray] = None
    evolution_history: List[Dict[str, Any]] = field(default_factory=list)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    version: str = "2.0"
    
    def add_dimension(self, dim_type: DimensionType, value: Any, 
                     confidence: float = 1.0, metadata: Dict[str, Any] = None) -> None:
        """Add or update a dimension"""
        self.dimensions[dim_type] = GeoidDimension(
            type=dim_type,
            value=value,
            confidence=confidence,
            metadata=metadata or {}
        )
        self.updated_at = datetime.utcnow()
        self._update_interaction_matrix()
    
    def get_dimension_vector(self, dim_type: DimensionType) -> Optional[np.ndarray]:
        """Get vector representation of a specific dimension"""
        if dim_type in self.dimensions:
            return self.dimensions[dim_type].to_vector()
        return None
    
    def get_composite_vector(self, dim_types: List[DimensionType] = None) -> np.ndarray:
        """Get composite vector from multiple dimensions"""
        if dim_types is None:
            dim_types = list(self.dimensions.keys())
        
        vectors = []
        weights = []
        
        for dim_type in dim_types:
            if dim_type in self.dimensions:
                dim = self.dimensions[dim_type]
                vectors.append(dim.to_vector())
                weights.append(dim.confidence)
        
        if not vectors:
            # Return semantic vector as fallback
            return self.sem_vec
        
        # Weighted average of dimension vectors
        vectors = np.array(vectors)
        weights = np.array(weights)
        weights = weights / weights.sum()
        
        composite = np.sum(vectors * weights[:, np.newaxis], axis=0)
        return composite / np.linalg.norm(composite)
    
    def _update_interaction_matrix(self) -> None:
        """Update the interaction matrix between dimensions"""
        dim_types = list(self.dimensions.keys())
        n = len(dim_types)
        
        if n < 2:
            self.interaction_matrix = None
            return
        
        # Create interaction matrix based on vector similarities
        matrix = np.zeros((n, n))
        
        for i, dim1 in enumerate(dim_types):
            vec1 = self.dimensions[dim1].to_vector()
            for j, dim2 in enumerate(dim_types):
                if i != j:
                    vec2 = self.dimensions[dim2].to_vector()
                    # Ensure vectors have same shape
                    min_len = min(len(vec1), len(vec2))
                    similarity = np.dot(vec1[:min_len], vec2[:min_len])
                    matrix[i, j] = similarity
        
        self.interaction_matrix = matrix
    
    def compute_wavelet_decomposition(self, levels: int = 4) -> Dict[str, np.ndarray]:
        """
        Compute spherical wavelet decomposition of the Geoid
        
        This creates a multi-resolution representation of the Geoid's
        semantic space using wavelet transforms.
        """
        # Combine all dimension vectors
        all_vectors = [self.sem_vec, self.sym_vec]
        
        for dim in self.dimensions.values():
            vec = dim.to_vector()
            # Pad or truncate to match sem_vec size
            if len(vec) < len(self.sem_vec):
                vec = np.pad(vec, (0, len(self.sem_vec) - len(vec)))
            else:
                vec = vec[:len(self.sem_vec)]
            all_vectors.append(vec)
        
        # Stack vectors into matrix
        signal_matrix = np.vstack(all_vectors)
        
        # Simple wavelet-like decomposition using FFT
        coeffs = {}
        for level in range(levels):
            # Apply frequency-based decomposition
            fft_result = np.fft.fft(signal_matrix, axis=1)
            
            # Extract different frequency bands
            n = signal_matrix.shape[1]
            band_size = n // (2 ** (level + 1))
            
            if band_size > 0:
                low_freq = fft_result[:, :band_size]
                high_freq = fft_result[:, band_size:2*band_size]
                
                coeffs[f'level_{level}_low'] = np.real(np.fft.ifft(low_freq, n=n, axis=1))
                coeffs[f'level_{level}_high'] = np.real(np.fft.ifft(high_freq, n=n, axis=1))
        
        self.wavelet_coeffs = coeffs
        return coeffs
    
    def measure_dimensional_coherence(self) -> float:
        """
        Measure the coherence between different dimensions
        
        Returns a value between 0 and 1 indicating how well
        the different dimensions align with each other.
        """
        if len(self.dimensions) < 2:
            return 1.0
        
        if self.interaction_matrix is None:
            self._update_interaction_matrix()
        
        if self.interaction_matrix is None:
            return 1.0
        
        # Calculate average off-diagonal similarity
        n = self.interaction_matrix.shape[0]
        mask = ~np.eye(n, dtype=bool)
        coherence = np.mean(np.abs(self.interaction_matrix[mask]))
        
        return float(coherence)
    
    def evolve(self, changes: Dict[DimensionType, Any]) -> None:
        """
        Evolve the Geoid by updating dimensions and tracking history
        """
        # Record current state
        current_state = {
            'timestamp': datetime.utcnow(),
            'dimensions': {
                dim_type: {
                    'value': dim.value,
                    'confidence': dim.confidence
                }
                for dim_type, dim in self.dimensions.items()
            },
            'coherence': self.measure_dimensional_coherence()
        }
        self.evolution_history.append(current_state)
        
        # Apply changes
        for dim_type, new_value in changes.items():
            if isinstance(new_value, tuple):
                value, confidence = new_value
                self.add_dimension(dim_type, value, confidence)
            else:
                self.add_dimension(dim_type, new_value)
    
    def get_evolution_trajectory(self) -> List[np.ndarray]:
        """Get the trajectory of the Geoid through dimensional space over time"""
        trajectory = []
        
        for state in self.evolution_history:
            # Reconstruct composite vector for each historical state
            vectors = []
            for dim_type_str, dim_data in state['dimensions'].items():
                # Simple vector reconstruction from historical data
                if isinstance(dim_data['value'], list):
                    vectors.append(np.array(dim_data['value']))
            
            if vectors:
                composite = np.mean(vectors, axis=0)
                trajectory.append(composite)
        
        # Add current state
        trajectory.append(self.get_composite_vector())
        
        return trajectory
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert GeoidV2 to dictionary representation"""
        return {
            'gid': self.gid,
            'raw': self.raw,
            'echo': self.echo,
            'lang_axis': self.lang_axis,
            'context_layers': self.context_layers,
            'vdr': self.vdr,
            'scars': self.scars,
            'dimensions': {
                dim_type.value: {
                    'value': dim.value,
                    'confidence': dim.confidence,
                    'metadata': dim.metadata
                }
                for dim_type, dim in self.dimensions.items()
            },
            'coherence': self.measure_dimensional_coherence(),
            'version': self.version,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_geoid(cls, geoid: Any) -> GeoidV2:
        """Create GeoidV2 from original Geoid"""
        return cls(
            raw=geoid.raw,
            echo=geoid.echo,
            gid=geoid.gid,
            lang_axis=geoid.lang_axis,
            context_layers=geoid.context_layers,
            sem_vec=geoid.sem_vec,
            sym_vec=geoid.sym_vec,
            vdr=geoid.vdr,
            scars=geoid.scars if hasattr(geoid, 'scars') else [],
            created_at=geoid.created_at if hasattr(geoid, 'created_at') else datetime.utcnow(),
            updated_at=geoid.updated_at if hasattr(geoid, 'updated_at') else datetime.utcnow()
        )


def init_geoid_v2(text: str = None, lang: str = "en", layers: List[str] = None, 
                  *, raw: str | None = None, tags=None, **kwargs) -> GeoidV2:
    """
    Initialize an enhanced GeoidV2 with full dimensional analysis
    
    This maintains compatibility with the original init_geoid function
    while adding enhanced dimensional capabilities.
    """
    # Import the original init_geoid function
    from ..geoid import init_geoid
    
    # Create base geoid using original function
    base_geoid = init_geoid(text=text, lang=lang, layers=layers, 
                           raw=raw, tags=tags, **kwargs)
    
    # Convert to GeoidV2
    geoid_v2 = GeoidV2.from_geoid(base_geoid)
    
    # Add initial semantic and symbolic dimensions
    geoid_v2.add_dimension(
        DimensionType.SEMANTIC,
        base_geoid.sem_vec,
        confidence=1.0,
        metadata={'source': 'sentence_transformer'}
    )
    
    geoid_v2.add_dimension(
        DimensionType.SYMBOLIC,
        base_geoid.sym_vec,
        confidence=1.0,
        metadata={'source': 'sentence_transformer'}
    )
    
    return geoid_v2