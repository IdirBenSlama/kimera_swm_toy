"""
Geoid Substrate - Non-tokenized Knowledge Layer

The Geoid is the atomic unit of knowledge in Kimera's next evolution.
It's a multidimensional, topological structure representing meaning, context, and history.
"""

import numpy as np
from typing import Dict, List, Set, Optional, Any, Tuple
from dataclasses import dataclass, field
import uuid
from datetime import datetime


@dataclass
class GeoidCore:
    """The semantic core of a Geoid - its essential meaning."""
    essence: np.ndarray  # High-dimensional semantic vector
    modality: str  # 'language', 'image', 'code', 'hybrid'
    polyglot_axes: Dict[str, np.ndarray] = field(default_factory=dict)  # Cross-lingual/modal projections
    
    def __post_init__(self):
        if self.essence.ndim != 1:
            raise ValueError("Essence must be a 1D vector")


@dataclass
class SymbolicShell:
    """The symbolic shell wrapping the semantic core."""
    symbols: Set[str]  # Symbolic identifiers
    relations: Dict[str, List[str]]  # Symbolic relationships
    constraints: List[str]  # Booklaw constraints
    
    def add_symbol(self, symbol: str):
        self.symbols.add(symbol)
    
    def add_relation(self, relation_type: str, target: str):
        if relation_type not in self.relations:
            self.relations[relation_type] = []
        self.relations[relation_type].append(target)


class Geoid:
    """
    A multidimensional, topological structure representing meaning, context, and history.
    Each geoid carries semantic core, symbolic shell, resonance links, contradiction links, and scar index.
    """
    
    def __init__(self, 
                 essence: np.ndarray,
                 modality: str = 'language',
                 symbols: Optional[Set[str]] = None,
                 metadata: Optional[Dict[str, Any]] = None):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.core = GeoidCore(essence=essence, modality=modality)
        self.shell = SymbolicShell(
            symbols=symbols or set(),
            relations={},
            constraints=[]
        )
        
        # Dynamic links
        self.resonance_links: Dict[str, float] = {}  # geoid_id -> resonance_strength
        self.contradiction_links: Dict[str, float] = {}  # geoid_id -> contradiction_intensity
        self.scar_index: List[str] = []  # List of scar IDs this geoid participated in
        
        # Drift tracking
        self.drift_history: List[Tuple[datetime, np.ndarray]] = [(self.created_at, essence.copy())]
        self.mutation_count: int = 0
        
        # Metadata
        self.metadata = metadata or {}
    
    def compute_resonance(self, other: 'Geoid') -> float:
        """Compute resonance strength with another geoid."""
        # Cosine similarity in semantic space
        dot_product = np.dot(self.core.essence, other.core.essence)
        norm_product = np.linalg.norm(self.core.essence) * np.linalg.norm(other.core.essence)
        
        if norm_product == 0:
            return 0.0
        
        base_resonance = dot_product / norm_product
        
        # Modality bonus/penalty
        modality_factor = 1.0 if self.core.modality == other.core.modality else 0.8
        
        # Symbolic overlap bonus
        symbol_overlap = len(self.shell.symbols & other.shell.symbols)
        symbol_bonus = min(0.2, symbol_overlap * 0.05)
        
        return np.clip(base_resonance * modality_factor + symbol_bonus, -1.0, 1.0)
    
    def compute_contradiction(self, other: 'Geoid') -> float:
        """Compute contradiction intensity with another geoid."""
        # Anti-correlation in semantic space
        resonance = self.compute_resonance(other)
        
        # Base contradiction from anti-resonance
        base_contradiction = max(0, -resonance)
        
        # Check for explicit contradictory relations
        contradiction_boost = 0.0
        for rel_type, targets in self.shell.relations.items():
            if rel_type.startswith('contradicts_') or rel_type == 'negates':
                if other.id in targets:
                    contradiction_boost = 0.5
                    break
        
        # Modality contradiction (e.g., text vs image of different concepts)
        if self.core.modality != other.core.modality:
            # Different modalities representing different concepts
            cross_modal_distance = 1.0 - abs(resonance)
            contradiction_boost += cross_modal_distance * 0.2
        
        return np.clip(base_contradiction + contradiction_boost, 0.0, 1.0)
    
    def mutate(self, drift_vector: np.ndarray, booklaw_check: callable) -> bool:
        """
        Mutate the geoid's essence according to drift vector.
        Returns True if mutation was lawful and applied.
        """
        new_essence = self.core.essence + drift_vector
        
        # Check with Booklaw
        if not booklaw_check(self, new_essence):
            return False
        
        # Apply mutation
        self.core.essence = new_essence
        self.drift_history.append((datetime.now(), new_essence.copy()))
        self.mutation_count += 1
        
        return True
    
    def add_scar(self, scar_id: str):
        """Record participation in a scar event."""
        self.scar_index.append(scar_id)
    
    def project_to_modality(self, target_modality: str) -> Optional[np.ndarray]:
        """Project this geoid to another modality if axis exists."""
        return self.core.polyglot_axes.get(target_modality)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize geoid to dictionary."""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'modality': self.core.modality,
            'essence_dim': len(self.core.essence),
            'symbols': list(self.shell.symbols),
            'relations': self.shell.relations,
            'constraints': self.shell.constraints,
            'resonance_links': self.resonance_links,
            'contradiction_links': self.contradiction_links,
            'scar_count': len(self.scar_index),
            'mutation_count': self.mutation_count,
            'metadata': self.metadata
        }


class GeoidSubstrate:
    """
    The substrate layer managing all geoids in the system.
    Provides spatial indexing, resonance fields, and cross-modal bridges.
    """
    
    def __init__(self, dimension: int = 512):
        self.dimension = dimension
        self.geoids: Dict[str, Geoid] = {}
        
        # Spatial indices for efficient resonance/contradiction search
        self.modality_index: Dict[str, Set[str]] = {}
        self.symbol_index: Dict[str, Set[str]] = {}
        
        # Global resonance field
        self.resonance_field: Optional[np.ndarray] = None
        self.field_update_count = 0
    
    def add_geoid(self, geoid: Geoid) -> str:
        """Add a geoid to the substrate."""
        self.geoids[geoid.id] = geoid
        
        # Update indices
        if geoid.core.modality not in self.modality_index:
            self.modality_index[geoid.core.modality] = set()
        self.modality_index[geoid.core.modality].add(geoid.id)
        
        for symbol in geoid.shell.symbols:
            if symbol not in self.symbol_index:
                self.symbol_index[symbol] = set()
            self.symbol_index[symbol].add(geoid.id)
        
        # Mark field for update
        self.resonance_field = None
        
        return geoid.id
    
    def find_resonant_geoids(self, geoid: Geoid, threshold: float = 0.5, 
                           limit: int = 10) -> List[Tuple[str, float]]:
        """Find geoids that resonate above threshold."""
        resonances = []
        
        for other_id, other in self.geoids.items():
            if other_id == geoid.id:
                continue
            
            resonance = geoid.compute_resonance(other)
            if resonance >= threshold:
                resonances.append((other_id, resonance))
        
        # Sort by resonance strength
        resonances.sort(key=lambda x: x[1], reverse=True)
        
        return resonances[:limit]
    
    def find_contradictory_geoids(self, geoid: Geoid, threshold: float = 0.3,
                                limit: int = 10) -> List[Tuple[str, float]]:
        """Find geoids that contradict above threshold."""
        contradictions = []
        
        for other_id, other in self.geoids.items():
            if other_id == geoid.id:
                continue
            
            contradiction = geoid.compute_contradiction(other)
            if contradiction >= threshold:
                contradictions.append((other_id, contradiction))
        
        # Sort by contradiction intensity
        contradictions.sort(key=lambda x: x[1], reverse=True)
        
        return contradictions[:limit]
    
    def compute_global_resonance_field(self) -> np.ndarray:
        """Compute the global resonance field across all geoids."""
        if self.resonance_field is not None and self.field_update_count < 100:
            self.field_update_count += 1
            return self.resonance_field
        
        # Initialize field
        field = np.zeros(self.dimension)
        
        # Sum weighted essences
        for geoid in self.geoids.values():
            # Weight by mutation count (more mutations = more influence)
            weight = 1.0 + np.log1p(geoid.mutation_count)
            field += geoid.core.essence * weight
        
        # Normalize
        norm = np.linalg.norm(field)
        if norm > 0:
            field = field / norm
        
        self.resonance_field = field
        self.field_update_count = 0
        
        return field
    
    def cross_modal_bridge(self, source_geoid_id: str, 
                         target_modality: str) -> Optional[Geoid]:
        """Create a cross-modal projection of a geoid."""
        source = self.geoids.get(source_geoid_id)
        if not source:
            return None
        
        # Check if projection exists
        projection = source.project_to_modality(target_modality)
        if projection is None:
            # Generate projection using resonance field
            field = self.compute_global_resonance_field()
            
            # Simple projection: blend essence with field
            projection = 0.7 * source.core.essence + 0.3 * field
            projection = projection / np.linalg.norm(projection)
        
        # Create new geoid in target modality
        bridge_geoid = Geoid(
            essence=projection,
            modality=target_modality,
            symbols={f"bridge_from_{source.id}"},
            metadata={
                'source_id': source.id,
                'source_modality': source.core.modality,
                'bridge_type': 'cross_modal'
            }
        )
        
        # Link to source
        bridge_geoid.resonance_links[source.id] = 0.8
        
        return bridge_geoid
    
    def get_substrate_stats(self) -> Dict[str, Any]:
        """Get statistics about the substrate."""
        total_resonance_links = sum(len(g.resonance_links) for g in self.geoids.values())
        total_contradiction_links = sum(len(g.contradiction_links) for g in self.geoids.values())
        total_scars = sum(len(g.scar_index) for g in self.geoids.values())
        
        modality_counts = {m: len(ids) for m, ids in self.modality_index.items()}
        
        return {
            'total_geoids': len(self.geoids),
            'modality_distribution': modality_counts,
            'total_resonance_links': total_resonance_links,
            'total_contradiction_links': total_contradiction_links,
            'total_scars': total_scars,
            'avg_mutations_per_geoid': sum(g.mutation_count for g in self.geoids.values()) / max(1, len(self.geoids))
        }