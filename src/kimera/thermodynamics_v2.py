"""
Thermodynamics V2: Rigorous Semantic Pressure Model
==================================================

This module implements a scientifically grounded thermodynamic model where:
- Pressure comes from TRUE contradictions, not just low similarity
- Phase transitions are based on meaningful semantic properties
- All calculations are validated against known examples

Key improvements:
1. Contradiction must be explicit (A and not-A), not just low similarity
2. Pressure is normalized by system size
3. Coherence measures positive alignment, not just non-contradiction
4. Phase boundaries are empirically calibrated
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

from .geoid import Geoid
from .contradiction import detect_contradiction
from .resonance import resonance


@dataclass
class SemanticState:
    """Complete thermodynamic state of a geoid."""
    gid: str
    pressure: float  # From true contradictions
    coherence: float  # Positive semantic alignment
    tension: float  # Internal inconsistency
    temperature: float  # Semantic volatility
    phase: str  # solid, liquid, gas, plasma


class ThermodynamicSystemV2:
    """
    Rigorous thermodynamic model based on semantic principles.
    
    Key concepts:
    - Pressure: Force from direct contradictions only
    - Coherence: Degree of semantic alignment with context
    - Temperature: Rate of semantic change/volatility
    - Phase: Emergent state from pressure/coherence balance
    """
    
    def __init__(self, 
                 contradiction_threshold: float = 0.8,  # Min confidence for true contradiction
                 coherence_threshold: float = 0.5,      # Min resonance for coherence
                 pressure_scale: float = 1.0):          # Pressure scaling factor
        self.contradiction_threshold = contradiction_threshold
        self.coherence_threshold = coherence_threshold
        self.pressure_scale = pressure_scale
        
        # Empirically calibrated phase boundaries
        self.phase_boundaries = {
            "solid": {"max_pressure": 0.2, "min_coherence": 0.7},
            "liquid": {"max_pressure": 0.5, "min_coherence": 0.4},
            "gas": {"max_pressure": 0.8, "min_coherence": 0.2},
            # plasma: everything else
        }
    
    def calculate_semantic_pressure(self, geoid: Geoid, context: List[Geoid]) -> Tuple[float, List[str]]:
        """
        Calculate pressure from TRUE contradictions only.
        
        Returns:
            (normalized_pressure, list_of_contradicting_gids)
        """
        if not context:
            return 0.0, []
        
        contradicting_gids = []
        total_pressure = 0.0
        
        for other in context:
            if other.gid == geoid.gid:
                continue
            
            # Check for true contradiction
            is_contradiction, confidence, reasoning = detect_contradiction(geoid, other)
            
            if is_contradiction and confidence >= self.contradiction_threshold:
                # This is a true semantic contradiction
                contradicting_gids.append(other.gid)
                
                # Pressure proportional to contradiction strength
                pressure_contribution = confidence * self.pressure_scale
                
                # Additional pressure if there's also high resonance (paradox)
                res = resonance(geoid, other)
                if res > 0.5:  # Paradoxical: similar yet contradictory
                    pressure_contribution *= (1 + res)
                
                total_pressure += pressure_contribution
        
        # Normalize by context size to prevent scaling issues
        normalized_pressure = total_pressure / len(context) if context else 0.0
        
        return normalized_pressure, contradicting_gids
    
    def calculate_semantic_coherence(self, geoid: Geoid, context: List[Geoid]) -> Tuple[float, List[str]]:
        """
        Calculate coherence from positive semantic alignment.
        
        Returns:
            (coherence_score, list_of_aligned_gids)
        """
        if not context:
            return 0.0, []
        
        aligned_gids = []
        coherence_scores = []
        
        for other in context:
            if other.gid == geoid.gid:
                continue
            
            # Check if NOT contradictory
            is_contradiction, confidence, _ = detect_contradiction(geoid, other)
            
            if not is_contradiction or confidence < self.contradiction_threshold:
                # Check positive alignment
                res = resonance(geoid, other)
                
                if res >= self.coherence_threshold:
                    aligned_gids.append(other.gid)
                    coherence_scores.append(res)
        
        # Average coherence with aligned concepts
        avg_coherence = np.mean(coherence_scores) if coherence_scores else 0.0
        
        return avg_coherence, aligned_gids
    
    def calculate_semantic_temperature(self, geoid: Geoid, context: List[Geoid]) -> float:
        """
        Calculate temperature as semantic volatility/ambiguity.
        
        High temperature = high variance in relationships
        """
        if not context:
            return 0.0
        
        resonances = []
        for other in context:
            if other.gid != geoid.gid:
                resonances.append(resonance(geoid, other))
        
        if not resonances:
            return 0.0
        
        # Temperature as variance in semantic relationships
        temperature = np.std(resonances)
        
        return temperature
    
    def determine_phase(self, pressure: float, coherence: float, temperature: float) -> str:
        """
        Determine thermodynamic phase from state variables.
        
        Phases:
        - Solid: Low pressure, high coherence, low temperature (stable, well-defined)
        - Liquid: Medium pressure/coherence/temperature (flexible, adaptable)
        - Gas: High pressure or low coherence (dispersed, unstable)
        - Plasma: Extreme conditions (breakdown of semantic structure)
        """
        # Temperature modifier
        temp_factor = 1 + temperature
        
        # Effective pressure increases with temperature
        effective_pressure = pressure * temp_factor
        
        # Check phase boundaries in order
        if (effective_pressure <= self.phase_boundaries["solid"]["max_pressure"] and
            coherence >= self.phase_boundaries["solid"]["min_coherence"]):
            return "solid"
        
        elif (effective_pressure <= self.phase_boundaries["liquid"]["max_pressure"] and
              coherence >= self.phase_boundaries["liquid"]["min_coherence"]):
            return "liquid"
        
        elif (effective_pressure <= self.phase_boundaries["gas"]["max_pressure"] and
              coherence >= self.phase_boundaries["gas"]["min_coherence"]):
            return "gas"
        
        else:
            return "plasma"
    
    def analyze_semantic_state(self, geoid: Geoid, context: List[Geoid]) -> SemanticState:
        """
        Complete thermodynamic analysis of a geoid in context.
        """
        # Calculate state variables
        pressure, contradicting = self.calculate_semantic_pressure(geoid, context)
        coherence, aligned = self.calculate_semantic_coherence(geoid, context)
        temperature = self.calculate_semantic_temperature(geoid, context)
        
        # Calculate derived quantities
        tension = pressure / (coherence + 0.1)  # Avoid division by zero
        
        # Determine phase
        phase = self.determine_phase(pressure, coherence, temperature)
        
        return SemanticState(
            gid=geoid.gid,
            pressure=pressure,
            coherence=coherence,
            tension=tension,
            temperature=temperature,
            phase=phase
        )
    
    def generate_phase_diagram(self, geoids: List[Geoid]) -> Dict[str, List[SemanticState]]:
        """
        Generate complete phase diagram for a set of geoids.
        """
        states = []
        for geoid in geoids:
            state = self.analyze_semantic_state(geoid, geoids)
            states.append(state)
        
        # Group by phase
        phase_diagram = {
            "solid": [],
            "liquid": [],
            "gas": [],
            "plasma": []
        }
        
        for state in states:
            phase_diagram[state.phase].append(state)
        
        return phase_diagram, states
    
    def detect_critical_points(self, states: List[SemanticState]) -> Dict[str, float]:
        """
        Detect critical points in the phase diagram.
        """
        if not states:
            return {}
        
        # Sort by pressure
        sorted_states = sorted(states, key=lambda s: s.pressure)
        
        critical_points = {}
        
        # Find phase transition points
        current_phase = sorted_states[0].phase
        for state in sorted_states:
            if state.phase != current_phase:
                # Phase transition detected
                transition_name = f"{current_phase}_to_{state.phase}"
                critical_points[transition_name] = state.pressure
                current_phase = state.phase
        
        return critical_points


def validate_thermodynamic_model():
    """
    Validate the model with known examples.
    """
    from .geoid import init_geoid
    
    print("Validating Thermodynamic Model V2")
    print("=" * 60)
    
    # Test cases with expected phases
    test_cases = [
        # Solid: Coherent, non-contradictory
        (["Water is H2O", "Ice is frozen water", "Steam is water vapor"], "solid"),
        
        # Liquid: Some tension but coherent
        (["Democracy is good", "Democracy has flaws", "Democracy needs improvement"], "liquid"),
        
        # Gas: Contradictory but related
        (["Light is a wave", "Light is a particle", "Light has dual nature"], "gas"),
        
        # Plasma: Extreme contradictions
        (["This statement is true", "This statement is false", "All statements are lies"], "plasma"),
    ]
    
    system = ThermodynamicSystemV2()
    
    for texts, expected_phase in test_cases:
        geoids = [init_geoid(t) for t in texts]
        states = [system.analyze_semantic_state(g, geoids) for g in geoids]
        
        phases = [s.phase for s in states]
        most_common = max(set(phases), key=phases.count)
        
        print(f"\nTest: {texts[0][:30]}...")
        print(f"Expected: {expected_phase}, Got: {most_common}")
        print(f"Distribution: {dict((p, phases.count(p)) for p in set(phases))}")
        
        if most_common == expected_phase:
            print("✓ PASS")
        else:
            print("✗ FAIL")
            for s in states:
                print(f"  {s.gid[:8]}: P={s.pressure:.3f}, C={s.coherence:.3f}, T={s.temperature:.3f}")


if __name__ == "__main__":
    from .geoid import init_geoid
    validate_thermodynamic_model()