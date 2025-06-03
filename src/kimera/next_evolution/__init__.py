"""
Kimera SWM Next Evolution - Post-token, Contradiction-native Architecture

This module implements the core components of the next evolution of Kimera:
- Geoid Substrate (non-tokenized knowledge layer)
- Contradiction Reactor (cognition engine)
- Scar Vault (topological memory)
- SWM Semantic Physics Engine
- Booklaw & Compliance Layer
- Observability & Manipulation Layer
"""

from .geoid import Geoid, GeoidSubstrate
from .contradiction import ContradictionReactor, ContradictionEvent
from .scar_vault import ScarVault, Scar, ScarTopology
from .semantic_physics import SWMPhysicsEngine, EchoformGrammar
from .booklaw import Booklaw, ComplianceGrid, AuditLedger
from .observability import Watchtower, VaultForensics
# Newly added modules
from .consensus import ConsensusEngine, ConsensusEvent
from .verbose_diffusion import VerboseDiffusionNarrator

__all__ = [
    "Geoid",
    "GeoidSubstrate",
    "ContradictionReactor",
    "ContradictionEvent",
    "ScarVault",
    "Scar",
    "ScarTopology",
    "SWMPhysicsEngine",
    "EchoformGrammar",
    "Booklaw",
    "ComplianceGrid",
    "AuditLedger",
    "Watchtower",
    "VaultForensics",
    # Consensus & Diffusion
    "ConsensusEngine",
    "ConsensusEvent",
    "VerboseDiffusionNarrator"
]