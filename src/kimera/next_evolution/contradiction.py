"""
Contradiction Reactor - Cognition Engine

Detects, injects, amplifies, and metabolizes contradiction between geoids and in scar vaults.
Implements contradiction conservation law and mutation protocol.
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import uuid
import numpy as np


@dataclass
class ContradictionEvent:
    """A record of a contradiction event between geoids."""
    id: str
    timestamp: datetime
    geoid_a: str
    geoid_b: str
    intensity: float
    resolved: bool = False
    mutation_vector: Optional[np.ndarray] = None
    scar_id: Optional[str] = None
    notes: Optional[str] = None


class ContradictionReactor:
    """
    The cognition engine for contradiction detection, injection, amplification, and metabolism.
    """
    def __init__(self, substrate, scar_vault, min_contradiction_density: float = 0.05):
        self.substrate = substrate  # GeoidSubstrate
        self.scar_vault = scar_vault  # ScarVault
        self.min_contradiction_density = min_contradiction_density
        self.events: List[ContradictionEvent] = []
        self.active_contradictions: Dict[Tuple[str, str], ContradictionEvent] = {}

    def detect_contradictions(self, threshold: float = 0.3) -> List[ContradictionEvent]:
        """Scan substrate for contradictions above threshold."""
        events = []
        geoids = list(self.substrate.geoids.values())
        for i, g1 in enumerate(geoids):
            for g2 in geoids[i+1:]:
                intensity = g1.compute_contradiction(g2)
                if intensity >= threshold:
                    event = ContradictionEvent(
                        id=str(uuid.uuid4()),
                        timestamp=datetime.now(),
                        geoid_a=g1.id,
                        geoid_b=g2.id,
                        intensity=intensity
                    )
                    events.append(event)
        return events

    def inject_contradiction(self, geoid_a_id: str, geoid_b_id: str, intensity: float, notes: str = "manual") -> ContradictionEvent:
        """Manually inject a contradiction event."""
        event = ContradictionEvent(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            geoid_a=geoid_a_id,
            geoid_b=geoid_b_id,
            intensity=intensity,
            notes=notes
        )
        self.events.append(event)
        self.active_contradictions[(geoid_a_id, geoid_b_id)] = event
        return event

    def amplify_contradictions(self, factor: float = 1.1):
        """Amplify all active contradictions by a factor."""
        for event in self.active_contradictions.values():
            event.intensity = min(event.intensity * factor, 1.0)

    def metabolize_contradictions(self, booklaw_check: callable) -> List[str]:
        """
        Resolve contradictions by mutating geoids and logging scar events.
        Returns list of new scar IDs.
        """
        scars_created = []
        for key, event in list(self.active_contradictions.items()):
            if event.resolved:
                continue
            g1 = self.substrate.geoids.get(event.geoid_a)
            g2 = self.substrate.geoids.get(event.geoid_b)
            if not g1 or not g2:
                continue
            # Mutation protocol: create drift vectors
            drift_vec = (g2.core.essence - g1.core.essence) * event.intensity * 0.1
            # Mutate both geoids (in opposite directions)
            mutated1 = g1.mutate(drift_vec, booklaw_check)
            mutated2 = g2.mutate(-drift_vec, booklaw_check)
            # Log scar event if at least one mutation occurred
            if mutated1 or mutated2:
                scar_id = self.scar_vault.create_scar([g1.id, g2.id], event.id, event.intensity)
                g1.add_scar(scar_id)
                g2.add_scar(scar_id)
                event.scar_id = scar_id
                event.resolved = True
                scars_created.append(scar_id)
        # Remove resolved contradictions
        self.active_contradictions = {k: v for k, v in self.active_contradictions.items() if not v.resolved}
        return scars_created

    def enforce_contradiction_conservation(self):
        """
        Ensure the system maintains a minimal density of contradiction (CLS ≠ 1.0).
        If too few contradictions, inject new ones between most resonant geoids.
        """
        total_geoids = len(self.substrate.geoids)
        if total_geoids < 2:
            return
        current_density = len(self.active_contradictions) / (total_geoids * (total_geoids - 1) / 2)
        if current_density < self.min_contradiction_density:
            # Find most resonant pairs and inject contradiction
            geoids = list(self.substrate.geoids.values())
            for i, g1 in enumerate(geoids):
                for g2 in geoids[i+1:]:
                    if (g1.id, g2.id) not in self.active_contradictions:
                        resonance = g1.compute_resonance(g2)
                        if resonance > 0.7:
                            self.inject_contradiction(g1.id, g2.id, intensity=0.4, notes="conservation law")
                            return  # Only inject one per call
