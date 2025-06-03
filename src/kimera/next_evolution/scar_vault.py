"""
Scar Vault - Non-linear, Topological Memory

Scars are persistent, spatially indexed records of contradiction collisions, with echo/decay law.
Vault supports non-Euclidean retrieval by resonance, not recency.
"""

from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import uuid
import numpy as np


@dataclass
class Scar:
    """A persistent record of a contradiction collision (scar event)."""
    id: str
    timestamp: datetime
    geoid_ids: List[str]
    contradiction_event_id: str
    intensity: float
    echo_strength: float = 1.0
    decay_rate: float = 0.01  # Per time unit
    resonance_signature: Optional[np.ndarray] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    reactivation_count: int = 0
    last_reactivated: Optional[datetime] = None

    def decay(self, now: Optional[datetime] = None):
        """Apply echo decay law to the scar."""
        now = now or datetime.now()
        if self.last_reactivated:
            dt = (now - self.last_reactivated).total_seconds()
        else:
            dt = (now - self.timestamp).total_seconds()
        self.echo_strength *= np.exp(-self.decay_rate * dt)
        if self.echo_strength < 1e-6:
            self.echo_strength = 0.0

    def reactivate(self, resonance_boost: float = 0.2):
        """Reactivate the scar, boosting echo strength and updating timestamp."""
        self.echo_strength = min(self.echo_strength + resonance_boost, 1.0)
        self.reactivation_count += 1
        self.last_reactivated = datetime.now()


class ScarTopology:
    """Non-Euclidean spatial index for scars (hypergraph/holographic)."""
    def __init__(self):
        self.scar_map: Dict[str, Scar] = {}
        self.geoid_to_scars: Dict[str, Set[str]] = {}

    def add_scar(self, scar: Scar):
        self.scar_map[scar.id] = scar
        for gid in scar.geoid_ids:
            if gid not in self.geoid_to_scars:
                self.geoid_to_scars[gid] = set()
            self.geoid_to_scars[gid].add(scar.id)

    def scars_for_geoid(self, geoid_id: str) -> List[Scar]:
        return [self.scar_map[sid] for sid in self.geoid_to_scars.get(geoid_id, set())]

    def all_scars(self) -> List[Scar]:
        return list(self.scar_map.values())

    def scars_by_resonance(self, resonance_vec: np.ndarray, top_k: int = 10) -> List[Scar]:
        scored = []
        for scar in self.scar_map.values():
            if scar.resonance_signature is not None:
                sim = float(np.dot(resonance_vec, scar.resonance_signature) /
                            (np.linalg.norm(resonance_vec) * np.linalg.norm(scar.resonance_signature) + 1e-8))
                scored.append((sim, scar))
        scored.sort(reverse=True, key=lambda x: x[0])
        return [s for _, s in scored[:top_k]]


class ScarVault:
    """
    The scar vault stores, reactivates, and decays scars.
    Retrieval is by resonance, not recency.
    """
    def __init__(self, dimension: int = 512):
        self.topology = ScarTopology()
        self.dimension = dimension

    def create_scar(self, geoid_ids: List[str], contradiction_event_id: str, intensity: float,
                    resonance_signature: Optional[np.ndarray] = None, metadata: Optional[Dict[str, Any]] = None) -> str:
        scar = Scar(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            geoid_ids=geoid_ids,
            contradiction_event_id=contradiction_event_id,
            intensity=intensity,
            resonance_signature=resonance_signature,
            metadata=metadata or {}
        )
        self.topology.add_scar(scar)
        return scar.id

    def decay_all(self):
        now = datetime.now()
        for scar in self.topology.all_scars():
            scar.decay(now)

    def reactivate_scar(self, scar_id: str, resonance_boost: float = 0.2):
        scar = self.topology.scar_map.get(scar_id)
        if scar:
            scar.reactivate(resonance_boost)

    def retrieve_by_resonance(self, resonance_vec: np.ndarray, top_k: int = 10) -> List[Scar]:
        return self.topology.scars_by_resonance(resonance_vec, top_k=top_k)

    def scars_for_geoid(self, geoid_id: str) -> List[Scar]:
        return self.topology.scars_for_geoid(geoid_id)

    def get_stats(self) -> Dict[str, Any]:
        scars = self.topology.all_scars()
        return {
            'total_scars': len(scars),
            'avg_echo_strength': float(np.mean([s.echo_strength for s in scars]) if scars else 0.0),
            'avg_reactivations': float(np.mean([s.reactivation_count for s in scars]) if scars else 0.0)
        }
