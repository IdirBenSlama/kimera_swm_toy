"""
Unified Identity Model for Kimera
Replaces separate Geoid and Scar models with a single, extensible identity system.
"""

from __future__ import annotations
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import hashlib
import math
from uuid import uuid4

from .entropy import calculate_term_entropy, calculate_relationship_entropy, adaptive_tau


class Identity:
    """
    Unified identity model that replaces both Geoid and Scar.
    
    Supports both content-based identities (former Geoids) and 
    relationship-based identities (former Scars).
    """

    def _validate_vector(self, vector):
        """Validate numpy array input for security."""
        if vector is None:
            return None
            
        # Type validation
        if not isinstance(vector, np.ndarray):
            raise TypeError("Vector must be numpy ndarray")
            
        # Size validation (max 100MB)
        if hasattr(vector, 'nbytes') and vector.nbytes > 100 * 1024 * 1024:
            raise ValueError(f"Vector too large: {vector.nbytes} bytes (max 100MB)")
            
        # Bounds validation
        if not np.all(np.isfinite(vector)):
            raise ValueError("Vector contains invalid values (NaN/Infinity)")
            
        return vector

    def __init__(self,
                 id: Optional[str] = None,
                 identity_type: Optional[str] = None,
                 raw: Optional[str] = None,
                 echo: Optional[str] = None,
                 lang_axis: Optional[str] = None,
                 tags: Optional[List[str]] = None,
                 vector: Optional[np.ndarray] = None,
                 weight: Optional[float] = None,
                 related_ids: Optional[List[str]] = None,
                 meta: Optional[Dict[str, Any]] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None,
                 # Backward-compatibility arguments:
                 content: Optional[str] = None,
                 metadata: Optional[Dict[str, Any]] = None):
        """
        Backward-compatible constructor:
        - If content=... is supplied, assume geoid-type identity
        - If metadata=... is supplied, fill the meta field
        Otherwise, require the full set of args.
        """
        now = datetime.now(timezone.utc)

        # If the caller used content=... syntax (legacy):
        if content is not None:
            # Treat as a "geoid" (content-based) identity
            self.identity_type = "geoid"
            self.id = f"geoid_{uuid4().hex}"
            self.raw = content
            self.echo = content
            self.lang_axis = "en"
            self.tags = []
            self.vector = self._validate_vector(vector)
            self.weight = 1.0
            self.related_ids = []
            self.meta = metadata or {}
            self.created_at = now
            self.updated_at = now
            # Add legacy properties for backward compatibility
            self.content = content
            self.metadata = metadata or {}
            return

        # If none of content/metadata were used, fall back to current behavior:
        self.id = id or str(uuid4())
        self.identity_type = identity_type or "geoid"
        self.raw = raw or ""
        self.echo = echo or self.raw
        self.lang_axis = lang_axis or "en"
        self.tags = tags or []
        self.vector = self._validate_vector(vector)
        self.weight = weight if weight is not None else 1.0
        self.related_ids = related_ids or []
        self.meta = meta or {}
        self.created_at = created_at or now
        self.updated_at = updated_at or now

    def __post_init__(self):
        """Initialize computed fields and defaults"""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = self.created_at
        
        # Set echo to raw if not provided
        if not self.echo and self.raw:
            self.echo = self.raw

    @classmethod
    def create_scar(cls,
                    content: Optional[str] = None,
                    related_ids: Optional[List[str]] = None,
                    weight: float = 1.0,
                    metadata: Optional[Dict[str, Any]] = None):
        """
        Factory method for a SCAR identity.
        Example usage:
            scar = Identity.create_scar(content="test scar", related_ids=["id1", "id2"], metadata={"rel_type": "test"})
        """
        now = datetime.now(timezone.utc)
        new_id = f"scar_{uuid4().hex}"
        
        # Prepare metadata with related_ids
        meta = metadata or {}
        if related_ids:
            meta["related_ids"] = related_ids
            
        scar = cls(
            id=new_id,
            identity_type="scar",
            raw=content or "",
            echo=content or "",
            lang_axis="en",
            tags=[],
            vector=None,
            weight=weight,
            related_ids=related_ids or [],
            meta=meta,
            created_at=now,
            updated_at=now,
        )
        
        # Add legacy attributes for backward compatibility
        scar.content = content or ""
        scar.metadata = meta
        
        return scar

    def __eq__(self, other):
        """Test equality based on content and type"""
        if not isinstance(other, Identity):
            return False
        
        # For backward compatibility, check legacy content attribute first
        if hasattr(self, 'content') and hasattr(other, 'content'):
            return (
                self.identity_type == other.identity_type and
                self.content == other.content
            )
        
        return (
            self.identity_type == other.identity_type and
            self.raw == other.raw and
            self.echo == other.echo and
            self.lang_axis == other.lang_axis and
            self.tags == other.tags and
            self.related_ids == other.related_ids and
            self.meta == other.meta
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert Identity to dictionary for serialization"""
        result = {
            "id": self.id,
            "identity_type": self.identity_type,
            "raw": self.raw,
            "echo": self.echo,
            "lang_axis": self.lang_axis,
            "tags": self.tags,
            "weight": self.weight,
            "related_ids": self.related_ids,
            "meta": self.meta,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        
        # Add legacy fields for backward compatibility
        if hasattr(self, 'content'):
            result["content"] = self.content
        if hasattr(self, 'metadata'):
            result["metadata"] = self.metadata
            
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Identity':
        """Create Identity from dictionary"""
        # Handle datetime parsing
        created_at = None
        updated_at = None
        if data.get("created_at"):
            created_at = datetime.fromisoformat(data["created_at"])
        if data.get("updated_at"):
            updated_at = datetime.fromisoformat(data["updated_at"])
        
        # Check if this is legacy format with content/metadata
        if "content" in data:
            return cls(
                content=data["content"],
                metadata=data.get("metadata", {})
            )
        
        # New format
        return cls(
            id=data.get("id"),
            identity_type=data.get("identity_type", "geoid"),
            raw=data.get("raw", ""),
            echo=data.get("echo", ""),
            lang_axis=data.get("lang_axis", "en"),
            tags=data.get("tags", []),
            weight=data.get("weight", 1.0),
            related_ids=data.get("related_ids", []),
            meta=data.get("meta", {}),
            created_at=created_at,
            updated_at=updated_at
        )
    
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
    
    def age_seconds(self) -> float:
        """
        Calculate age of identity in seconds.
        
        Returns:
            Age in seconds since creation
        """
        if self.created_at is None:
            return 0.0
        
        now = datetime.now(timezone.utc)
        age_delta = now - self.created_at
        return age_delta.total_seconds()
    
    def decay_factor(self, tau_seconds: Optional[float] = None) -> float:
        """
        Calculate current decay factor based on age.
        
        Args:
            tau_seconds: Time decay constant (default: uses effective_tau)
            
        Returns:
            Decay factor between 0 and 1
        """
        if tau_seconds is None:
            tau_seconds = self.effective_tau()
        
        age = self.age_seconds()
        if tau_seconds <= 0:
            return 0.0
        
        return math.exp(-age / tau_seconds)
    
    def update_metadata(self, key: str, value: Any) -> None:
        """
        Update metadata and refresh updated_at timestamp.
        
        Args:
            key: Metadata key
            value: Metadata value
        """
        self.meta[key] = value
        self.updated_at = datetime.now(timezone.utc)
    
    def add_tag(self, tag: str) -> None:
        """
        Add a tag if not already present.
        
        Args:
            tag: Tag to add
        """
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now(timezone.utc)
    
    def remove_tag(self, tag: str) -> bool:
        """
        Remove a tag if present.
        
        Args:
            tag: Tag to remove
            
        Returns:
            True if tag was removed, False if not found
        """
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now(timezone.utc)
            return True
        return False


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