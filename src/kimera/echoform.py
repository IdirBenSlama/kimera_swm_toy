"""
EchoForm v0.7.2 Core Implementation
Handles echo-form creation, mutation, and topology management with time-decay weighting
"""
from dataclasses import dataclass, field
import hashlib
import json
import time
import math
from typing import List, Dict, Any, Optional

# Time-decay constant (τ = 14 days in seconds)
TIME_DECAY_TAU = 14 * 24 * 3600  # 14 days


@dataclass
class EchoForm:
    """
    Core EchoForm class for managing echo-form topology and traces.
    
    Attributes:
        anchor: Primary identifier for the form
        domain: Domain classification (default: "echo")
        terms: List of term dictionaries with symbol, role, intensity
        phase: Current phase of the form (default: "active")
        recursive: Whether form supports recursive operations
        topology: JSON-serializable topology data
        trace_signature: Cryptographic trace for form lineage
        echo_created_at: Timestamp of form creation
    """
    anchor: str
    domain: str = "echo"
    terms: List[Dict[str, Any]] = field(default_factory=list)
    phase: str = "active"
    recursive: bool = True
    topology: Dict[str, Any] = field(default_factory=dict)
    trace_signature: str = ""
    echo_created_at: Optional[float] = None

    def __post_init__(self):
        """Initialize computed fields after dataclass creation"""
        if self.echo_created_at is None:
            self.echo_created_at = time.time()
        
        if not self.trace_signature:
            self.trace_signature = self.compute_trace()

    def compute_trace(self, prev_sig: str = "") -> str:
        """
        Compute trace signature using sha256(anchor + prev_sig)
        
        Args:
            prev_sig: Previous signature for chaining (optional)
            
        Returns:
            16-character hex string from SHA256 hash
        """
        base_string = f"{self.anchor}:{self.phase}"
        if prev_sig:
            base_string += f":{prev_sig}"
        
        hash_obj = hashlib.sha256(base_string.encode('utf-8'))
        return hash_obj.hexdigest()[:16]

    def intensity_sum(self, apply_time_decay: bool = True) -> float:
        """
        Calculate total intensity across all terms with optional time-decay weighting
        
        Args:
            apply_time_decay: Whether to apply time-decay weighting (default: True)
        
        Returns:
            Sum of intensity values from all terms, optionally weighted by time decay
        """
        if not apply_time_decay:
            # Simple sum without time decay
            return sum(term.get("intensity", 0.0) for term in self.terms)
        
        # Apply time-decay weighting
        current_time = time.time()
        total_intensity = 0.0
        
        for term in self.terms:
            base_intensity = term.get("intensity", 0.0)
            
            # Check if term has a timestamp for decay calculation
            term_timestamp = term.get("timestamp")
            if term_timestamp is not None:
                # Calculate time difference in seconds
                time_diff = current_time - term_timestamp
                # Apply exponential decay: intensity * exp(-Δt / τ)
                decay_factor = math.exp(-time_diff / TIME_DECAY_TAU)
                weighted_intensity = base_intensity * decay_factor
            else:
                # No timestamp - use form creation time or no decay
                if self.echo_created_at is not None:
                    time_diff = current_time - self.echo_created_at
                    decay_factor = math.exp(-time_diff / TIME_DECAY_TAU)
                    weighted_intensity = base_intensity * decay_factor
                else:
                    # No timing info - use full intensity
                    weighted_intensity = base_intensity
            
            total_intensity += weighted_intensity
        
        return total_intensity

    def add_term(self, symbol: str, role: str, intensity: float = 1.0, **kwargs) -> None:
        """
        Add a new term to the form
        
        Args:
            symbol: Term symbol/identifier
            role: Role classification for the term
            intensity: Intensity value (default: 1.0)
            **kwargs: Additional term properties
        """
        term = {
            "symbol": symbol,
            "role": role,
            "intensity": intensity,
            **kwargs
        }
        self.terms.append(term)

    def mutate_phase(self, new_phase: str) -> 'EchoForm':
        """
        Create a new EchoForm with mutated phase
        
        Args:
            new_phase: New phase value
            
        Returns:
            New EchoForm instance with updated phase and trace
        """
        new_form = EchoForm(
            anchor=self.anchor,
            domain=self.domain,
            terms=self.terms.copy(),
            phase=new_phase,
            recursive=self.recursive,
            topology=self.topology.copy(),
            trace_signature="",  # Will be computed in __post_init__
            echo_created_at=time.time()
        )
        # Chain the trace signature
        new_form.trace_signature = new_form.compute_trace(self.trace_signature)
        return new_form

    def flatten(self) -> str:
        """
        Serialize the EchoForm to JSON string
        
        Returns:
            JSON string representation of the form
        """
        return json.dumps(self.__dict__, ensure_ascii=False, sort_keys=True)

    @classmethod
    def reinflate(cls, blob: str) -> 'EchoForm':
        """
        Deserialize EchoForm from JSON string
        
        Args:
            blob: JSON string representation
            
        Returns:
            EchoForm instance reconstructed from JSON
        """
        data = json.loads(blob)
        
        # Extract only fields that exist in the dataclass
        valid_fields = {k: v for k, v in data.items() if k in cls.__annotations__}
        
        return cls(**valid_fields)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert EchoForm to dictionary
        
        Returns:
            Dictionary representation of the form
        """
        return {
            "anchor": self.anchor,
            "domain": self.domain,
            "terms": self.terms,
            "phase": self.phase,
            "recursive": self.recursive,
            "topology": self.topology,
            "trace_signature": self.trace_signature,
            "echo_created_at": self.echo_created_at
        }

    def __repr__(self) -> str:
        """String representation for debugging"""
        return f"EchoForm(anchor='{self.anchor}', domain='{self.domain}', phase='{self.phase}', terms={len(self.terms)})"


# Re-export init_geoid for legacy tests
from .geoid import init_geoid
__all__ = ["EchoForm", "init_geoid"]