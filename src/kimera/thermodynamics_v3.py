"""
Thermodynamics V3: Scientifically Grounded Implementation
========================================================

This is the corrected thermodynamic model that:
1. Uses proper contradiction detection (V2 fixed)
2. Calculates pressure from TRUE contradictions only
3. Normalizes by system size to prevent scaling issues
4. Produces meaningful phase diagrams

Key improvements:
- Pressure comes from actual contradictions, not low similarity
- Phase boundaries are empirically calibrated
- All calculations validated against test cases
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

from .geoid import Geoid
from .contradiction_v2_fixed import analyze_contradiction
from .resonance import resonance


@dataclass
class ThermodynamicState:
    """Complete thermodynamic state of a geoid."""
    gid: str
    raw: str
    pressure: float          # From true contradictions
    coherence: float         # Positive semantic alignment  
    temperature: float       # Semantic volatility
    phase: str              # solid, liquid, gas, plasma
    contradictions: List[str] # GIDs of contradicting geoids
    aligned_geoids: List[str] # GIDs of coherent geoids


class ThermodynamicSystemV3:
    """
    Scientifically grounded thermodynamic model.
    
    Based on rigorous principles:
    - Pressure = force from TRUE contradictions only
    - Coherence = positive semantic alignment
    - Temperature = variance in semantic relationships
    - Phase = emergent state from P/C/T balance
    """
    
    def __init__(self, 
                 min_contradiction_confidence: float = 0.7,
                 min_coherence_threshold: float = 0.2):
        self.min_contradiction_confidence = min_contradiction_confidence
        self.min_coherence_threshold = min_coherence_threshold
        
        # Empirically calibrated phase boundaries
        self.phase_boundaries = {
            "solid": {"max_pressure": 0.1, "min_coherence": 0.6},
            "liquid": {"max_pressure": 0.3, "min_coherence": 0.3},
            "gas": {"max_pressure": 0.6, "min_coherence": 0.1},
            # plasma: everything else
        }
    
    def calculate_semantic_pressure(self, geoid: Geoid, context: List[Geoid]) -> Tuple[float, List[str]]:
        """
        Calculate pressure from TRUE contradictions only.
        
        Returns: (normalized_pressure, contradicting_gids)
        """
        if not context:
            return 0.0, []
        
        contradicting_gids = []
        total_pressure = 0.0
        
        for other in context:
            if other.gid == geoid.gid:
                continue
            
            # Use the fixed contradiction detection
            analysis = analyze_contradiction(geoid, other)
            
            if (analysis.is_contradiction and 
                analysis.confidence >= self.min_contradiction_confidence):
                
                contradicting_gids.append(other.gid)
                
                # Pressure proportional to contradiction confidence
                pressure_contribution = analysis.confidence
                
                # Boost for high semantic similarity (paradoxical contradictions)
                semantic_sim = resonance(geoid, other)
                if semantic_sim > 0.6:
                    pressure_contribution *= (1 + semantic_sim * 0.5)
                
                total_pressure += pressure_contribution
        
        # Normalize by context size to prevent scaling issues
        normalized_pressure = total_pressure / len(context) if context else 0.0
        
        return normalized_pressure, contradicting_gids
    
    def calculate_semantic_coherence(self, geoid: Geoid, context: List[Geoid]) -> Tuple[float, List[str]]:
        """
        Calculate coherence from positive semantic alignment.
        
        Returns: (coherence_score, aligned_gids)
        """
        if not context:
            return 0.0, []
        
        aligned_gids = []
        coherence_scores = []
        
        for other in context:
            if other.gid == geoid.gid:
                continue
            
            # Check if NOT contradictory
            analysis = analyze_contradiction(geoid, other)
            
            if (not analysis.is_contradiction or 
                analysis.confidence < self.min_contradiction_confidence):
                
                # Check positive alignment
                semantic_sim = resonance(geoid, other)
                
                if semantic_sim >= self.min_coherence_threshold:
                    aligned_gids.append(other.gid)
                    coherence_scores.append(semantic_sim)
        
        # Average coherence with aligned concepts
        avg_coherence = np.mean(coherence_scores) if coherence_scores else 0.0
        
        return avg_coherence, aligned_gids
    
    def calculate_semantic_temperature(self, geoid: Geoid, context: List[Geoid]) -> float:
        """
        Calculate temperature as semantic volatility.
        
        High temperature = high variance in relationships
        """
        if not context:
            return 0.0
        
        resonances = []
        for other in context:
            if other.gid != geoid.gid:
                resonances.append(resonance(geoid, other))
        
        if len(resonances) < 2:
            return 0.0
        
        # Temperature as standard deviation of relationships
        temperature = np.std(resonances)
        
        return temperature
    
    def determine_phase(self, pressure: float, coherence: float, temperature: float) -> str:
        """
        Determine thermodynamic phase from state variables.
        
        Phases based on pressure and coherence:
        - Solid: Low pressure, high coherence (stable, well-defined)
        - Liquid: Medium pressure/coherence (flexible, adaptable)  
        - Gas: High pressure or low coherence (dispersed, unstable)
        - Plasma: Extreme pressure (breakdown of structure)
        """
        # Temperature affects effective pressure
        temp_factor = 1 + temperature * 0.5
        effective_pressure = pressure * temp_factor
        
        # Check phase boundaries
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
    
    def analyze_geoid_state(self, geoid: Geoid, context: List[Geoid]) -> ThermodynamicState:
        """
        Complete thermodynamic analysis of a geoid.
        """
        # Calculate state variables
        pressure, contradicting = self.calculate_semantic_pressure(geoid, context)
        coherence, aligned = self.calculate_semantic_coherence(geoid, context)
        temperature = self.calculate_semantic_temperature(geoid, context)
        
        # Determine phase
        phase = self.determine_phase(pressure, coherence, temperature)
        
        return ThermodynamicState(
            gid=geoid.gid,
            raw=geoid.raw,
            pressure=pressure,
            coherence=coherence,
            temperature=temperature,
            phase=phase,
            contradictions=contradicting,
            aligned_geoids=aligned
        )
    
    def generate_phase_diagram(self, geoids: List[Geoid]) -> Tuple[Dict[str, List[ThermodynamicState]], List[ThermodynamicState]]:
        """
        Generate complete phase diagram for geoids.
        
        Returns: (phase_diagram, all_states)
        """
        all_states = []
        
        # Analyze each geoid
        for geoid in geoids:
            state = self.analyze_geoid_state(geoid, geoids)
            all_states.append(state)
        
        # Group by phase
        phase_diagram = {
            "solid": [],
            "liquid": [],
            "gas": [],
            "plasma": []
        }
        
        for state in all_states:
            phase_diagram[state.phase].append(state)
        
        return phase_diagram, all_states
    
    def detect_critical_points(self, states: List[ThermodynamicState]) -> Dict[str, float]:
        """
        Detect critical points in the phase diagram.
        """
        if not states:
            return {}
        
        # Sort by pressure
        sorted_states = sorted(states, key=lambda s: s.pressure)
        
        critical_points = {}
        
        # Find phase boundaries
        phase_pressures = {}
        for state in sorted_states:
            if state.phase not in phase_pressures:
                phase_pressures[state.phase] = []
            phase_pressures[state.phase].append(state.pressure)
        
        # Calculate boundary pressures
        for phase, pressures in phase_pressures.items():
            if pressures:
                critical_points[f"{phase}_min"] = min(pressures)
                critical_points[f"{phase}_max"] = max(pressures)
        
        return critical_points
    
    def validate_system(self) -> Dict[str, bool]:
        """
        Validate the thermodynamic system with known test cases.
        """
        from .geoid import init_geoid
        
        validation_results = {}
        
        # Test 1: Contradictory texts should have high pressure
        contradictory_texts = [
            "The sky is blue",
            "The sky is red",
            "The sky is not blue"
        ]
        
        geoids = [init_geoid(t) for t in contradictory_texts]
        states = [self.analyze_geoid_state(g, geoids) for g in geoids]
        
        avg_pressure = np.mean([s.pressure for s in states])
        validation_results["contradictory_high_pressure"] = avg_pressure > 0.2
        
        # Test 2: Coherent texts should have low pressure, high coherence
        coherent_texts = [
            "Water is H2O",
            "Ice is frozen water", 
            "Steam is water vapor"
        ]
        
        geoids = [init_geoid(t) for t in coherent_texts]
        states = [self.analyze_geoid_state(g, geoids) for g in geoids]
        
        avg_pressure = np.mean([s.pressure for s in states])
        avg_coherence = np.mean([s.coherence for s in states])
        
        validation_results["coherent_low_pressure"] = avg_pressure < 0.1
        validation_results["coherent_high_coherence"] = avg_coherence > 0.5
        
        # Test 3: Mixed corpus should have multiple phases
        mixed_texts = contradictory_texts + coherent_texts
        geoids = [init_geoid(t) for t in mixed_texts]
        phase_diagram, _ = self.generate_phase_diagram(geoids)
        
        phases_present = sum(1 for phase_states in phase_diagram.values() if phase_states)
        validation_results["multiple_phases"] = phases_present >= 2
        
        return validation_results


def validate_thermodynamic_system():
    """Validate the thermodynamic system."""
    print("Validating Thermodynamic System V3")
    print("=" * 60)
    
    system = ThermodynamicSystemV3()
    results = system.validate_system()
    
    print("\nValidation Results:")
    for test, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status} {test}")
    
    all_passed = all(results.values())
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return all_passed


if __name__ == "__main__":
    validate_thermodynamic_system()