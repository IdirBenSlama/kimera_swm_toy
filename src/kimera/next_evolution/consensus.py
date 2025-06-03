 """
 Consensus Module (Next-Evolution)
 ---------------------------------

 This module introduces a *ConsensusEngine* that derives a shared, lawful representation
 from a set of geoids.  Whereas contradiction drives drift and mutation, consensus
 provides *confluence* – a reversible, auditable projection of common resonance that
 can be used for downstream reasoning, aggregation, or summarisation.  Consensus never
 erases contradiction; it simply produces a new geoid representing the locally-stable
 attractor in semantic space.

 Design Principles
 =================
 • Non-destructive – input geoids remain unchanged.
 • Lawful – every consensus proposal passes through Booklaw compliance checks.
 • Auditable – events are logged in an AuditLedger (if supplied).
 • Multi-strategy – weighted barycenter (default) or Kemeny-Snell-like rank fusion.
 • Minimal Entropy Loss – a Booklaw rule can forbid excessive information collapse.
 """

 from __future__ import annotations

 import uuid
 from datetime import datetime
 from typing import List, Dict, Optional, Tuple

 import numpy as np

 # Lazy-import to avoid circulars
 from .geoid import Geoid, GeoidSubstrate
 from .booklaw import ComplianceGrid, AuditLedger


 class ConsensusError(Exception):
     """Raised when consensus generation fails (e.g., law violation)."""


 class UnsupportedConsensusMethod(ConsensusError):
     pass


 # ---------------------------------------------------------------------------
 # Data-classes for provenance
 # ---------------------------------------------------------------------------

 from dataclasses import dataclass, field


 @dataclass
 class ConsensusEvent:
     """An audit entry for a consensus projection."""

     id: str
     timestamp: datetime
     participant_ids: List[str]
     method: str
     consensus_geoid_id: Optional[str] = None
     details: Dict[str, float] = field(default_factory=dict)


 # ---------------------------------------------------------------------------
 # Engine implementation
 # ---------------------------------------------------------------------------


 class ConsensusEngine:
     """Compute lawful consensus projections over a set of geoids."""

     def __init__(
         self,
         substrate: GeoidSubstrate,
         compliance: Optional[ComplianceGrid] = None,
         audit_ledger: Optional[AuditLedger] = None,
         default_method: str = "weighted_barycenter",
     ) -> None:
         self.substrate = substrate
         self.compliance = compliance
         self.audit_ledger = audit_ledger
         self.default_method = default_method

     # ------------------------------------------------------------------
     # Public API
     # ------------------------------------------------------------------

     def generate_consensus(
         self,
         geoid_ids: List[str],
         weights: Optional[List[float]] = None,
         method: Optional[str] = None,
         modality: Optional[str] = None,
     ) -> Geoid:
         """Return a *new* geoid that encodes consensus across the supplied geoids.

         Args:
             geoid_ids:  identifiers within the substrate.
             weights:    non-negative weights (same length).  If *None*, equal.
             method:     consensus strategy – "weighted_barycenter" (default) or
                          "rank_fusion".
             modality:   optional target modality.  If *None*, majority vote of
                          input modalities is used.

         Returns:
             Newly-created lawful Geoid representing the consensus.
         """
         method = method or self.default_method

         # Retrieve geoids and validate
         participants = [self._require_geoid(gid) for gid in geoid_ids]
         if not participants:
             raise ConsensusError("No valid participant geoids supplied")

         if weights is not None and len(weights) != len(participants):
             raise ConsensusError("Weights length does not match participants")

         if weights is None:
             weights = [1.0] * len(participants)

         weights_arr = np.array(weights, dtype=float)
         if np.any(weights_arr < 0):
             raise ConsensusError("Weights must be non-negative")

         # Normalise weights
         if np.sum(weights_arr) == 0:
             raise ConsensusError("At least one weight must be > 0")
         weights_arr = weights_arr / np.sum(weights_arr)

         # Choose modality by simple majority if not provided
         if modality is None:
             modality = self._majority_modality(participants)

         # Compute consensus representation
         if method == "weighted_barycenter":
             consensus_vector = self._weighted_barycenter(participants, weights_arr)
         elif method == "rank_fusion":
             consensus_vector = self._rank_fusion(participants)
         else:
             raise UnsupportedConsensusMethod(method)

         # Build event first (without geoid id)
         event = ConsensusEvent(
             id=str(uuid.uuid4()),
             timestamp=datetime.now(),
             participant_ids=[g.id for g in participants],
             method=method,
         )

         # Create candidate geoid
         candidate = Geoid(essence=consensus_vector, modality=modality, symbols={"consensus"})

         # Booklaw compliance check, if grid supplied
         if self.compliance is not None:
             if not self.compliance.is_compliant({"type": "consensus", "geoid": candidate.to_dict()}):
                 raise ConsensusError("Consensus geoid violates Booklaw")

         # Register into substrate
         self.substrate.add_geoid(candidate)

         # Update event with resulting id and simple stats
         event.consensus_geoid_id = candidate.id
         event.details = {
             "avg_resonance": float(
                 np.mean([g.compute_resonance(candidate) for g in participants])
             ),
             "vector_norm": float(np.linalg.norm(consensus_vector)),
         }

         # Audit
         if self.audit_ledger is not None:
             self.audit_ledger.log_event("consensus", event.id, {
                 "participants": event.participant_ids,
                 "consensus_geoid_id": candidate.id,
                 "method": method,
                 "details": event.details,
             })

         return candidate

     # ------------------------------------------------------------------
     # Internal helpers
     # ------------------------------------------------------------------

     def _require_geoid(self, gid: str) -> Geoid:
         g = self.substrate.geoids.get(gid)
         if g is None:
             raise ConsensusError(f"Geoid '{gid}' not found in substrate")
         return g

     @staticmethod
     def _majority_modality(geoids: List[Geoid]) -> str:
         from collections import Counter

         modality_counts = Counter(g.core.modality for g in geoids)
         return modality_counts.most_common(1)[0][0]

     @staticmethod
     def _weighted_barycenter(participants: List[Geoid], weights: np.ndarray) -> np.ndarray:
         vectors = np.array([g.core.essence for g in participants])
         barycenter = np.average(vectors, axis=0, weights=weights)
         norm = np.linalg.norm(barycenter)
         return barycenter / norm if norm > 0 else barycenter

     @staticmethod
     def _rank_fusion(participants: List[Geoid]) -> np.ndarray:
         """Simple rank fusion based on pairwise resonance ordering.

         It produces an approximate consensus vector by iteratively moving an
         initial vector toward the highest aggregate resonance direction.
         """
         # Start from arithmetic mean
         vector = np.mean([g.core.essence for g in participants], axis=0)
         vector = vector / (np.linalg.norm(vector) or 1.0)

         # Gradient-like refinement
         for _ in range(3):  # few iterations – keep cheap
             direction = np.zeros_like(vector)
             for g in participants:
                 sign = np.sign(np.dot(vector, g.core.essence))
                 direction += sign * g.core.essence
             direction = direction / (np.linalg.norm(direction) or 1.0)
             vector = (vector + direction) / 2.0
             vector = vector / (np.linalg.norm(vector) or 1.0)
         return vector
