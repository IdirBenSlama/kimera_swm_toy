"""
Thermodynamic EchoForm Integration
==================================

This module bridges EchoForm with thermodynamic concepts:
- EchoForms accumulate semantic pressure from contradictory terms
- Phase transitions affect form topology
- Energy flows through term relationships
- Entropy influences time decay
"""

from typing import List, Dict, Optional, Tuple, Any
import time
import math
from dataclasses import dataclass

from .echoform import EchoForm
from .thermodynamics import ThermodynamicSystem, SemanticPressure, ConceptualVoid
from .geoid import init_geoid
from .resonance import resonance
from .contradiction import detect_contradiction


@dataclass
class ThermodynamicEchoForm(EchoForm):
    """
    EchoForm enhanced with thermodynamic properties.
    
    Adds:
    - Semantic pressure from contradictory terms
    - Phase state based on pressure and coherence
    - Energy capacity and transfer
    - Thermodynamic topology mutations
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thermo_system = ThermodynamicSystem()
        self.phase_state = "liquid"  # Default phase
        self.pressure_history = []
        self.energy_capacity = 10.0
        self.stored_energy = 0.0
        
    def calculate_internal_pressure(self) -> float:
        """
        Calculate semantic pressure from contradictory terms within the form.
        
        Returns:
            Total internal pressure
        """
        if len(self.terms) < 2:
            return 0.0
        
        total_pressure = 0.0
        
        # Check each pair of terms for contradictions
        for i, term1 in enumerate(self.terms):
            for j, term2 in enumerate(self.terms[i+1:], i+1):
                # Create temporary geoids for comparison
                g1 = init_geoid(term1["symbol"], lang="en")
                g2 = init_geoid(term2["symbol"], lang="en")
                
                # Check contradiction
                is_contra, confidence, _ = detect_contradiction(g1, g2)
                
                if is_contra:
                    # Pressure increases with intensity of contradicting terms
                    pressure = confidence * term1["intensity"] * term2["intensity"]
                    total_pressure += pressure
                    
                # Also check for low resonance (opposition)
                res = resonance(g1, g2)
                if res < 0.3:
                    pressure = (1.0 - res) * min(term1["intensity"], term2["intensity"])
                    total_pressure += pressure
        
        # Record pressure history
        self.pressure_history.append({
            "timestamp": time.time(),
            "pressure": total_pressure
        })
        
        return total_pressure
    
    def update_phase_state(self) -> str:
        """
        Update phase state based on current pressure and coherence.
        
        Phase states:
        - solid: Low pressure, high coherence
        - liquid: Moderate pressure/coherence
        - gas: High pressure, low coherence
        - plasma: Critical pressure, near collapse
        """
        pressure = self.calculate_internal_pressure()
        coherence = self.calculate_coherence()
        
        # Determine phase
        if pressure < 2.0 and coherence > 0.7:
            self.phase_state = "solid"
        elif pressure < 5.0 and coherence > 0.4:
            self.phase_state = "liquid"
        elif pressure < 10.0:
            self.phase_state = "gas"
        else:
            self.phase_state = "plasma"
        
        # Update EchoForm phase to match
        self.phase = f"thermo_{self.phase_state}"
        
        return self.phase_state
    
    def calculate_coherence(self) -> float:
        """
        Calculate internal coherence based on term resonances.
        
        Returns:
            Coherence score (0-1)
        """
        if len(self.terms) < 2:
            return 1.0
        
        total_resonance = 0.0
        pair_count = 0
        
        for i, term1 in enumerate(self.terms):
            for j, term2 in enumerate(self.terms[i+1:], i+1):
                g1 = init_geoid(term1["symbol"], lang="en")
                g2 = init_geoid(term2["symbol"], lang="en")
                
                res = resonance(g1, g2)
                total_resonance += res
                pair_count += 1
        
        return total_resonance / pair_count if pair_count > 0 else 1.0
    
    def add_term_with_pressure_check(self, symbol: str, role="generic", 
                                    intensity: float = 1.0, **kwargs) -> Dict[str, Any]:
        """
        Add term and check if it causes pressure buildup.
        
        Returns:
            Dict with pressure analysis
        """
        # Calculate pressure before adding
        pressure_before = self.calculate_internal_pressure()
        
        # Add the term
        self.add_term(symbol, role, intensity, **kwargs)
        
        # Calculate pressure after
        pressure_after = self.calculate_internal_pressure()
        pressure_increase = pressure_after - pressure_before
        
        # Update phase
        old_phase = self.phase_state
        new_phase = self.update_phase_state()
        
        return {
            "added": symbol,
            "pressure_before": pressure_before,
            "pressure_after": pressure_after,
            "pressure_increase": pressure_increase,
            "phase_before": old_phase,
            "phase_after": new_phase,
            "phase_changed": old_phase != new_phase
        }
    
    def check_collapse_conditions(self) -> Tuple[bool, Optional[str]]:
        """
        Check if the EchoForm should undergo constructive collapse.
        
        Returns:
            (should_collapse, collapse_type)
        """
        pressure = self.calculate_internal_pressure()
        
        # Different thresholds for different domains
        threshold = {
            "echo": 10.0,
            "scar": 15.0,  # Scars are more resilient
            "law": 20.0    # Laws are most stable
        }.get(self.domain, 10.0)
        
        if pressure >= threshold:
            if len(self.terms) > 20:
                return True, "fragmentation"
            elif pressure > threshold * 2:
                return True, "implosion"
            else:
                return True, "transformation"
        
        return False, None
    
    def constructive_collapse(self) -> ConceptualVoid:
        """
        Perform constructive collapse, creating a void.
        
        Returns:
            ConceptualVoid representing the collapsed form
        """
        pressure = self.calculate_internal_pressure()
        
        # Create void
        void = ConceptualVoid(
            origin_gid=self.trace_signature,
            collapse_pressure=pressure,
            dimensions={
                "term_count": len(self.terms),
                "coherence": self.calculate_coherence(),
                "entropy": self.entropy(),
                "domain": self.domain
            },
            potential_energy=pressure * self.intensity_sum()
        )
        
        # Reset the form to a void state
        self.terms = []
        self.phase = "void"
        self.topology = {"collapsed": True, "void_id": id(void)}
        
        return void
    
    def energy_transfer_to(self, other: 'ThermodynamicEchoForm', amount: float = 1.0) -> Dict[str, float]:
        """
        Transfer energy to another EchoForm.
        
        Energy transfer efficiency depends on domain compatibility and resonance.
        """
        # Check available energy
        available = min(amount, self.stored_energy)
        
        # Calculate transfer efficiency
        domain_compatibility = {
            ("echo", "echo"): 1.0,
            ("echo", "scar"): 0.8,
            ("echo", "law"): 0.6,
            ("scar", "scar"): 1.0,
            ("scar", "echo"): 0.8,
            ("scar", "law"): 0.7,
            ("law", "law"): 1.0,
            ("law", "scar"): 0.7,
            ("law", "echo"): 0.6,
        }.get((self.domain, other.domain), 0.5)
        
        # Calculate resonance between anchors
        g1 = init_geoid(self.anchor, lang="en")
        g2 = init_geoid(other.anchor, lang="en")
        anchor_resonance = resonance(g1, g2)
        
        # Total efficiency
        efficiency = domain_compatibility * anchor_resonance
        transferred = available * efficiency
        
        # Update energy levels
        self.stored_energy -= available
        other.stored_energy = min(other.stored_energy + transferred, other.energy_capacity)
        
        # Energy transfer can cause pressure in the receiver
        if anchor_resonance < 0.3:  # Low resonance = opposition
            pressure_created = transferred * (1.0 - anchor_resonance)
            other.pressure_history.append({
                "timestamp": time.time(),
                "pressure": pressure_created,
                "source": "energy_transfer"
            })
        else:
            pressure_created = 0.0
        
        return {
            "requested": amount,
            "available": available,
            "efficiency": efficiency,
            "transferred": transferred,
            "pressure_created": pressure_created
        }
    
    def thermodynamic_mutate(self, temperature: float = 1.0) -> 'ThermodynamicEchoForm':
        """
        Mutate the form based on thermodynamic principles.
        
        Higher temperature = more radical mutations.
        """
        # Update phase based on temperature
        pressure = self.calculate_internal_pressure()
        
        # Temperature affects phase transitions
        effective_pressure = pressure * temperature
        
        if effective_pressure < 2.0:
            new_phase = "solid"
        elif effective_pressure < 5.0:
            new_phase = "liquid"
        elif effective_pressure < 10.0:
            new_phase = "gas"
        else:
            new_phase = "plasma"
        
        # Create mutated form
        mutated = self.mutate_phase(f"thermo_{new_phase}")
        
        # Convert to ThermodynamicEchoForm
        thermo_mutated = ThermodynamicEchoForm(
            anchor=mutated.anchor,
            domain=mutated.domain,
            phase=mutated.phase
        )
        thermo_mutated.terms = mutated.terms
        thermo_mutated.topology = mutated.topology
        thermo_mutated.trace_signature = mutated.trace_signature
        
        # Inherit thermodynamic properties with mutations
        thermo_mutated.stored_energy = self.stored_energy * (1.0 - temperature * 0.1)
        thermo_mutated.phase_state = new_phase
        
        return thermo_mutated
    
    def effective_tau_thermodynamic(self) -> float:
        """
        Calculate effective tau considering both entropy and pressure.
        
        High pressure reduces tau (faster decay).
        High entropy increases tau (slower decay).
        """
        base_tau = self.effective_tau()  # Entropy-based tau from parent
        
        # Pressure reduces tau
        pressure = self.calculate_internal_pressure()
        pressure_factor = 1.0 / (1.0 + pressure * 0.1)
        
        # Phase affects tau
        phase_factors = {
            "solid": 1.5,    # Solid forms decay slowest
            "liquid": 1.0,   # Normal decay
            "gas": 0.7,      # Faster decay
            "plasma": 0.3    # Very fast decay
        }
        phase_factor = phase_factors.get(self.phase_state, 1.0)
        
        return base_tau * pressure_factor * phase_factor
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Enhanced dictionary representation with thermodynamic data.
        """
        base_dict = super().to_dict()
        
        # Add thermodynamic metadata
        base_dict["thermodynamics"] = {
            "phase_state": self.phase_state,
            "internal_pressure": self.calculate_internal_pressure(),
            "coherence": self.calculate_coherence(),
            "stored_energy": self.stored_energy,
            "energy_capacity": self.energy_capacity,
            "effective_tau": self.effective_tau_thermodynamic(),
            "pressure_history_length": len(self.pressure_history)
        }
        
        # Check collapse conditions
        should_collapse, collapse_type = self.check_collapse_conditions()
        base_dict["thermodynamics"]["near_collapse"] = should_collapse
        if should_collapse:
            base_dict["thermodynamics"]["collapse_type"] = collapse_type
        
        return base_dict


def create_thermodynamic_echoform(anchor: str = "", domain: str = "echo", 
                                 initial_energy: float = 0.0, **kwargs) -> ThermodynamicEchoForm:
    """
    Factory function to create a ThermodynamicEchoForm.
    
    Args:
        anchor: Form anchor
        domain: Form domain (echo, scar, law)
        initial_energy: Starting energy level
        **kwargs: Additional EchoForm parameters
        
    Returns:
        ThermodynamicEchoForm instance
    """
    form = ThermodynamicEchoForm(anchor=anchor, domain=domain, **kwargs)
    form.stored_energy = initial_energy
    return form