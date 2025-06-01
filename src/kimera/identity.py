"""
Unified Identity Model for Kimera
Replaces separate Geoid and Scar models with a single, extensible identity system.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import hashlib
import math
from uuid import uuid4

from .entropy import calculate_term_entropy, calculate_relationship_entropy, adaptive_tau


@dataclass
class Identity:
    """
    Unified identity model that replaces both Geoid and Scar.
    
    Supports both content-based identities (former Geoids) and 
    relationship-based identities (former Scars).
    """
    
    # Core identification
    id: str = field(default_factory=lambda: str(uuid4()))
    identity_type: str = "geoid"  # "geoid" or "scar"
    
    # Content & semantics (primarily for geoid-type)
    raw: str = ""
    echo: str = ""
    lang_axis: str = "en"
    tags: List[str] = field(default_factory=list)
    
    # Vectors & scoring
    vector: Optional[np.ndarray] = None
    weight: float = 1.0
    
    # Relationships (primarily for scar-type)
    related_ids: List[str] = field(default_factory=list)
    
    # Metadata & extensibility
    meta: Dict[str, Any] = field(default_factory=dict)
    
    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Initialize computed fields and defaults"""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = self.created_at
        
        # Set echo to raw if not provided
        if not self.echo and self.raw:
            self.echo = self.raw
    
    def entropy(self) -> float:
        """
        Calculate Shannon entropy for this identity.
        
        For geoid-type: entropy of term intensities
        For scar-type: entropy of relationships
        """
        if self.identity_type == "scar":
            return calculate_relationship_entropy(self.related_ids, self.weight)
        
        # For geoid-type, use terms from meta if available
        if "terms" in self.meta and isinstance(self.meta["terms"], list):
            return calculate_term_entropy(self.meta["terms"])
        
        # Fallback: entropy based on tag diversity
        if self.tags:
            # Uniform distribution over tags
            n_tags = len(self.tags)
            return math.log2(n_tags) if n_tags > 1 else 0.0
        
        return 0.0
    
    def effective_tau(self, base_tau: float = 14 * 24 * 3600, k: float = 0.1) -> float:
        """
        Calculate effective time decay constant based on entropy.
        
        Args:
            base_tau: Base tau in seconds (default: 14 days)
            k: Entropy scaling factor
            
        Returns:
            Effective tau adjusted for entropy
        """
        entropy = self.entropy()
        return adaptive_tau(base_tau, entropy, k)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = {
            "id": self.id,
            "identity_type": self.identity_type,
            "raw": self.raw,
            "echo": self.echo,
            "lang_axis": self.lang_axis,
            "tags": self.tags,
            "weight": self.weight,
            "related_ids": self.related_ids,
            "meta": self.meta,
        }
        
        if self.created_at:
            data["created_at"] = self.created_at.isoformat()
        if self.updated_at:
            data["updated_at"] = self.updated_at.isoformat()
        
        # Handle numpy array
        if self.vector is not None:
            data["vector"] = self.vector.tolist()
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Identity:
        """Create Identity from dictionary"""
        # Handle timestamps
        created_at = None
        updated_at = None
        
        if "created_at" in data:
            created_at = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data:
            updated_at = datetime.fromisoformat(data["updated_at"])
        
        # Handle vector
        vector = None
        if "vector" in data and data["vector"] is not None:
            vector = np.array(data["vector"])
        
        return cls(
            id=data.get("id", str(uuid4())),
            identity_type=data.get("identity_type", "geoid"),
            raw=data.get("raw", ""),
            echo=data.get("echo", ""),
            lang_axis=data.get("lang_axis", "en"),
            tags=data.get("tags", []),
            weight=data.get("weight", 1.0),
            related_ids=data.get("related_ids", []),
            meta=data.get("meta", {}),
            vector=vector,
            created_at=created_at,
            updated_at=updated_at,
        )


# Migration utilities for backward compatibility

def geoid_to_identity(geoid) -> Identity:
    """Convert a Geoid to an Identity"""
    return Identity(
        id=getattr(geoid, "gid", getattr(geoid, "id", None)),
        identity_type="geoid",
        raw=geoid.raw,
        echo=getattr(geoid, 'echo', geoid.raw),
        lang_axis=getattr(geoid, 'lang_axis', 'en'),
        tags=getattr(geoid, 'tags', []),
        vector=getattr(geoid, 'vector', None),
        weight=getattr(geoid, 'weight', 1.0),
        meta=getattr(geoid, 'meta', {}),
        created_at=getattr(geoid, 'created_at', None),
        updated_at=getattr(geoid, 'updated_at', None),
    )


def scar_to_identity(scar) -> Identity:
    """Convert a Scar to an Identity"""
    return Identity(
        id=getattr(scar, 'id', str(uuid4())),
        identity_type="scar",
        raw=getattr(scar, 'raw', ""),
        echo=getattr(scar, 'echo', ""),
        lang_axis=getattr(scar, 'lang_axis', 'en'),
        tags=getattr(scar, 'tags', []),
        weight=getattr(scar, 'weight', 1.0),
        related_ids=getattr(scar, 'related_ids', []),
        meta=getattr(scar, 'meta', {}),
        created_at=getattr(scar, 'created_at', None),
        updated_at=getattr(scar, 'updated_at', None),
    )


def identity_to_geoid(identity: Identity):
    """Convert Identity back to Geoid-like object (for compatibility)"""
    from .geoid import Geoid
    
    return Geoid(
        raw=identity.raw,
        echo=identity.echo,
        lang_axis=identity.lang_axis,
        tags=identity.tags,
        vector=identity.vector,
        weight=identity.weight,
        meta=identity.meta,
    )


def identity_to_scar(identity: Identity):
    """Convert Identity back to Scar-like object (for compatibility)"""
    from .scar import Scar
    
    # Create a basic scar with available data
    scar = Scar()
    scar.id = identity.id
    scar.weight = identity.weight
    scar.related_ids = identity.related_ids
    scar.meta = identity.meta
    return scar


# Factory functions for creating specific identity types

def create_geoid_identity(text: str, lang: str = "en", tags: Optional[List[str]] = None, 
                         vector: Optional[np.ndarray] = None, **kwargs) -> Identity:
    """Create a geoid-type identity"""
    if tags is None:
        tags = []
    
    # Generate deterministic ID based on content
    content_hash = hashlib.sha256(f"{text}:{lang}".encode()).hexdigest()[:16]
    
    return Identity(
        id=f"geoid_{content_hash}",
        identity_type="geoid",
        raw=text,
        echo=text,
        lang_axis=lang,
        tags=tags,
        vector=vector,
        **kwargs
    )


def create_scar_identity(id1: str, id2: str, weight: float = 1.0, **kwargs) -> Identity:
    """Create a scar-type identity representing a relationship"""
    # Generate deterministic ID based on related IDs
    relation_hash = hashlib.sha256(f"{id1}:{id2}".encode()).hexdigest()[:16]
    
    return Identity(
        id=f"scar_{relation_hash}",
        identity_type="scar",
        related_ids=[id1, id2],
        weight=weight,
        **kwargs
    )