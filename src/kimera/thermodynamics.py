"""
Thermodynamic concepts for Kimera-SWM
=====================================

This module implements thermodynamic-inspired concepts for knowledge representation:
- Semantic pressure from contradictions
- Constructive collapse and void formation
- Energy-based transformations
- Phase transitions in conceptual space
"""

import math
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from datetime import datetime
import numpy as np

from .geoid import Geoid
from .contradiction import detect_contradiction
from .entropy import calculate_shannon_entropy


@dataclass
class SemanticPressure:
    """Represents accumulated semantic pressure in a Geoid."""
    value: float = 0.0
    sources: List[str] = field(default_factory=list)  # GIDs of contradicting geoids
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def add_pressure(self, amount: float, source_gid: str):
        """Add pressure from a contradiction source."""
        self.value += amount
        if source_gid not in self.sources:
            self.sources.append(source_gid)
        self.timestamp = datetime.utcnow()


@dataclass
class ConceptualVoid:
    """Represents a void created by constructive collapse."""
    origin_gid: str  # The geoid that collapsed
    collapse_pressure: float  # Pressure at collapse
    timestamp: datetime = field(default_factory=datetime.utcnow)
    dimensions: Dict[str, float] = field(default_factory=dict)  # Void characteristics
    potential_energy: float = 0.0  # Energy available for new structures


class ThermodynamicSystem:
    """Manages thermodynamic properties of a Geoid network."""
    
    def __init__(self, pressure_threshold: float = 10.0, energy_constant: float = 1.0):
        self.pressure_threshold = pressure_threshold
        self.energy_constant = energy_constant
        self.pressures: Dict[str, SemanticPressure] = {}
        self.voids: List[ConceptualVoid] = []
        self.phase_transitions: List[Dict] = []
        
    def calculate_pressure(self, geoid: Geoid, contradicting_geoids: List[Geoid]) -> float:
        """
        Calculate semantic pressure from contradictions.
        
        Pressure increases with:
        - Number of contradictions
        - Strength of contradictions
        - Resonance with contradicting concepts (paradoxically)
        """
        if geoid.gid not in self.pressures:
            self.pressures[geoid.gid] = SemanticPressure()
        
        pressure = self.pressures[geoid.gid]
        
        for other in contradicting_geoids:
            # First check for semantic opposition
            from .resonance import resonance
            res_score = resonance(geoid, other)
            
            # Low resonance can indicate opposition
            if res_score < 0.3:
                # Treat very low resonance as potential contradiction
                base_pressure = (1.0 - res_score) * 1.5
                pressure.add_pressure(base_pressure, other.gid)
                continue
            
            # Check explicit contradiction
            is_contradiction, confidence, reasoning = detect_contradiction(geoid, other)
            
            if is_contradiction:
                # Base pressure from contradiction
                base_pressure = confidence * 2.0
                
                # Additional pressure if there's also resonance (paradox)
                paradox_multiplier = 1.0 + res_score  # Higher resonance = more pressure
                
                pressure_amount = base_pressure * paradox_multiplier
                pressure.add_pressure(pressure_amount, other.gid)
            elif res_score > 0.7:
                # High resonance with something in the "contradicting" list
                # suggests internal tension or paradox
                pressure.add_pressure(res_score * 0.5, other.gid)
        
        return pressure.value
    
    def check_collapse_conditions(self, geoid: Geoid) -> Tuple[bool, Optional[str]]:
        """
        Check if a geoid should undergo constructive collapse.
        
        Returns:
            (should_collapse, collapse_type)
        """
        if geoid.gid not in self.pressures:
            return False, None
        
        pressure = self.pressures[geoid.gid].value
        
        if pressure >= self.pressure_threshold:
            # Determine collapse type based on pressure characteristics
            n_sources = len(self.pressures[geoid.gid].sources)
            
            if n_sources > 5:
                return True, "fragmentation"  # Too many contradictions
            elif pressure > self.pressure_threshold * 2:
                return True, "implosion"  # Extreme pressure
            else:
                return True, "transformation"  # Standard collapse
        
        return False, None
    
    def constructive_collapse(self, geoid: Geoid, collapse_type: str = "transformation") -> ConceptualVoid:
        """
        Perform constructive collapse of a geoid, creating a void.
        
        The void represents a space where new understanding can emerge.
        """
        pressure = self.pressures.get(geoid.gid, SemanticPressure()).value
        
        # Calculate void characteristics based on collapse type
        void_dimensions = {}
        
        if collapse_type == "fragmentation":
            # Multiple smaller voids with specific characteristics
            void_dimensions["fragments"] = len(self.pressures[geoid.gid].sources)
            void_dimensions["coherence"] = 0.2
            potential_energy = pressure * 0.5  # Energy dispersed
            
        elif collapse_type == "implosion":
            # Single deep void with high potential
            void_dimensions["depth"] = pressure / self.pressure_threshold
            void_dimensions["coherence"] = 0.8
            potential_energy = pressure * 1.5  # Energy concentrated
            
        else:  # transformation
            # Balanced void ready for restructuring
            void_dimensions["openness"] = 0.6
            void_dimensions["coherence"] = 0.5
            potential_energy = pressure * 1.0
        
        # Create the void
        void = ConceptualVoid(
            origin_gid=geoid.gid,
            collapse_pressure=pressure,
            dimensions=void_dimensions,
            potential_energy=potential_energy
        )
        
        self.voids.append(void)
        
        # Record phase transition
        self.phase_transitions.append({
            "timestamp": datetime.utcnow(),
            "geoid_gid": geoid.gid,
            "transition_type": f"collapse_{collapse_type}",
            "pressure": pressure,
            "void_id": len(self.voids) - 1
        })
        
        # Reset pressure after collapse
        if geoid.gid in self.pressures:
            del self.pressures[geoid.gid]
        
        return void
    
    def calculate_system_entropy(self, geoids: List[Geoid]) -> float:
        """
        Calculate total entropy of the geoid system.
        
        Higher entropy indicates more diverse/distributed information.
        """
        if not geoids:
            return 0.0
        
        # Collect all semantic vectors
        all_vectors = []
        for geoid in geoids:
            if hasattr(geoid, 'sem_vec') and geoid.sem_vec is not None:
                all_vectors.append(geoid.sem_vec)
        
        if not all_vectors:
            return 0.0
        
        # Calculate diversity based on vector distances
        vectors = np.array(all_vectors)
        mean_vec = np.mean(vectors, axis=0)
        
        # Distances from mean represent diversity
        distances = [np.linalg.norm(v - mean_vec) for v in vectors]
        
        # Convert to entropy
        return calculate_shannon_entropy(distances)
    
    def find_equilibrium_point(self, geoid: Geoid, context_geoids: List[Geoid]) -> Dict[str, float]:
        """
        Find the equilibrium point for a geoid in its context.
        
        Returns metrics indicating stability/instability.
        """
        # Calculate various forces
        pressure = self.calculate_pressure(geoid, context_geoids)
        
        # Coherence force (how well it fits with non-contradicting geoids)
        from .resonance import resonance
        coherence_scores = []
        for other in context_geoids:
            is_contradiction, _, _ = detect_contradiction(geoid, other)
            if not is_contradiction:
                coherence_scores.append(resonance(geoid, other))
        
        avg_coherence = np.mean(coherence_scores) if coherence_scores else 0.0
        
        # Calculate equilibrium metrics
        stability = avg_coherence / (1.0 + pressure)  # Higher coherence, lower pressure = stable
        tension = pressure / (1.0 + avg_coherence)  # Higher pressure, lower coherence = tense
        
        return {
            "pressure": pressure,
            "coherence": avg_coherence,
            "stability": stability,
            "tension": tension,
            "equilibrium": stability > 0.5  # Simple threshold
        }
    
    def energy_transfer(self, source_geoid: Geoid, target_geoid: Geoid, amount: float = 1.0) -> Dict[str, float]:
        """
        Model energy transfer between geoids during interaction.
        
        Energy can represent attention, influence, or information flow.
        """
        # Calculate transfer efficiency based on resonance
        from .resonance import resonance
        transfer_efficiency = resonance(source_geoid, target_geoid)
        
        # Actual energy transferred
        transferred = amount * transfer_efficiency
        
        # Energy can create pressure if there's contradiction
        is_contradiction, confidence, _ = detect_contradiction(source_geoid, target_geoid)
        if is_contradiction:
            pressure_increase = transferred * confidence
            if target_geoid.gid not in self.pressures:
                self.pressures[target_geoid.gid] = SemanticPressure()
            self.pressures[target_geoid.gid].add_pressure(pressure_increase, source_geoid.gid)
        
        return {
            "requested": amount,
            "efficiency": transfer_efficiency,
            "transferred": transferred,
            "pressure_created": pressure_increase if is_contradiction else 0.0
        }
    
    def phase_diagram(self, geoids: List[Geoid]) -> Dict[str, List[Geoid]]:
        """
        Categorize geoids by their thermodynamic phase.
        
        Phases:
        - solid: stable, low pressure, high coherence
        - liquid: moderate pressure, moderate coherence
        - gas: high pressure, low coherence
        - plasma: extreme pressure, near collapse
        """
        phases = {
            "solid": [],
            "liquid": [],
            "gas": [],
            "plasma": []
        }
        
        for geoid in geoids:
            equilibrium = self.find_equilibrium_point(geoid, geoids)
            pressure = equilibrium["pressure"]
            coherence = equilibrium["coherence"]
            
            # Classify based on pressure and coherence
            if pressure < 2.0 and coherence > 0.7:
                phases["solid"].append(geoid)
            elif pressure < 5.0 and coherence > 0.4:
                phases["liquid"].append(geoid)
            elif pressure < self.pressure_threshold:
                phases["gas"].append(geoid)
            else:
                phases["plasma"].append(geoid)
        
        return phases


def create_thermodynamic_system(pressure_threshold: float = 10.0) -> ThermodynamicSystem:
    """Factory function to create a thermodynamic system."""
    return ThermodynamicSystem(pressure_threshold=pressure_threshold)