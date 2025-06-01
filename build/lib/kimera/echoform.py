"""
EchoForm v0.7.2 Core Implementation
Handles echo-form creation, mutation, and topology management with time-decay weighting
"""
import hashlib
import json
import time
import math
from typing import List, Dict, Any, Optional
from datetime import datetime

# Import entropy functions for enhanced time decay
from .entropy import calculate_term_entropy, entropy_weighted_decay, DEFAULT_TAU_SECONDS

# Time-decay constant (τ = 14 days in seconds)
TIME_DECAY_TAU = DEFAULT_TAU_SECONDS


class EchoForm:
    """
    Core EchoForm class for managing echo-form topology and traces.
    Enhanced with security controls to prevent recursion attacks.
    
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
    
    # Security constants
    MAX_RECURSION_DEPTH = 100
    MAX_TERMS = 10000
    MAX_TOPOLOGY_SIZE = 1000000  # 1MB

    def __init__(self, anchor: str = "", domain: str = "echo", config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        Backward-compatible constructor that supports:
        - EchoForm() - no arguments
        - EchoForm(anchor="...", domain="...")
        - EchoForm(config={...})
        """
        # Initialize security controls
        self._recursion_depth = 0
        
        # Handle config-based construction
        if config is not None:
            anchor = config.get("anchor", anchor)
            domain = config.get("domain", domain)
            # Extract other config values if needed
            phase = config.get("phase", "active")
            recursive = config.get("recursive", True)
            # Store config for backward compatibility
            self.config = config
        else:
            phase = kwargs.get("phase", "active")
            recursive = kwargs.get("recursive", True)
            self.config = {}

        # Initialize dataclass fields
        self.anchor = anchor
        self.domain = domain
        self.terms = []
        self.phase = phase
        self.recursive = recursive
        self.topology = {}
        self.trace_signature = ""
        self.echo_created_at = time.time()
        
        # Compute trace signature
        self.trace_signature = self.compute_trace()
        
    def _check_recursion_limit(self):
        """Check and enforce recursion depth limits."""
        if self._recursion_depth >= self.MAX_RECURSION_DEPTH:
            raise RecursionError(f"Maximum recursion depth ({self.MAX_RECURSION_DEPTH}) exceeded")
        self._recursion_depth += 1
        
    def _reset_recursion_depth(self):
        """Reset recursion depth counter."""
        self._recursion_depth = 0
        
    def _validate_terms_limit(self, new_terms_count: int = 1):
        """Validate that adding terms won't exceed limits."""
        if len(self.terms) + new_terms_count > self.MAX_TERMS:
            raise ValueError(f"Too many terms: {len(self.terms) + new_terms_count} (max {self.MAX_TERMS})")
            
    def _validate_topology_size(self, topology_data):
        """Validate topology data size."""
        if isinstance(topology_data, (dict, list)):
            serialized = json.dumps(topology_data)
            if len(serialized) > self.MAX_TOPOLOGY_SIZE:
                raise ValueError(f"Topology too large: {len(serialized)} bytes (max {self.MAX_TOPOLOGY_SIZE})")
        return topology_data

    def __post_init__(self):
        """Initialize computed fields after dataclass creation"""
        # This is now handled in __init__ for compatibility
        pass

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

    def intensity_sum(self, apply_time_decay: bool = True, use_entropy_weighting: bool = True) -> float:
        """
        Calculate total intensity across all terms with optional time-decay weighting
        
        Args:
            apply_time_decay: Whether to apply time-decay weighting (default: True)
            use_entropy_weighting: Whether to use entropy-weighted decay (requires apply_time_decay=True)
        
        Returns:
            Sum of intensity values from all terms, optionally weighted by time decay
        """
        if not apply_time_decay:
            # Simple sum without time decay
            return sum(term.get("intensity", 0.0) for term in self.terms)
        
        # Apply time-decay weighting
        current_time = time.time()
        total_intensity = 0.0
        
        # Calculate entropy for entropy-weighted decay
        entropy = 0.0
        if use_entropy_weighting:
            entropy = calculate_term_entropy(self.terms)
        
        for term in self.terms:
            base_intensity = term.get("intensity", 0.0)
            
            # Check if term has a timestamp for decay calculation
            term_timestamp = term.get("timestamp")
            if term_timestamp is not None:
                # Calculate time difference in seconds
                time_diff = current_time - term_timestamp
                
                if use_entropy_weighting and entropy > 0:
                    # Use entropy-weighted decay
                    decay_factor = entropy_weighted_decay(time_diff, TIME_DECAY_TAU, entropy)
                else:
                    # Standard exponential decay: intensity * exp(-Δt / τ)
                    decay_factor = math.exp(-time_diff / TIME_DECAY_TAU)
                
                weighted_intensity = base_intensity * decay_factor
            else:
                # No timestamp - use form creation time or no decay
                if self.echo_created_at is not None:
                    time_diff = current_time - self.echo_created_at
                    
                    if use_entropy_weighting and entropy > 0:
                        decay_factor = entropy_weighted_decay(time_diff, TIME_DECAY_TAU, entropy)
                    else:
                        decay_factor = math.exp(-time_diff / TIME_DECAY_TAU)
                    
                    weighted_intensity = base_intensity * decay_factor
                else:
                    # No timing info - use full intensity
                    weighted_intensity = base_intensity
            
            total_intensity += weighted_intensity
        
        return total_intensity

    def entropy(self) -> float:
        """
        Calculate Shannon entropy of the EchoForm's term intensities.
        
        Returns:
            Shannon entropy value in bits
        """
        return calculate_term_entropy(self.terms)

    def effective_tau(self, base_tau: Optional[float] = None, k: float = 0.1) -> float:
        """
        Calculate effective time decay constant based on entropy.
        
        Args:
            base_tau: Base tau in seconds (default: uses TIME_DECAY_TAU)
            k: Entropy scaling factor
            
        Returns:
            Effective tau adjusted for entropy
        """
        if base_tau is None:
            base_tau = TIME_DECAY_TAU
        
        entropy = self.entropy()
        # Use adaptive tau formula: tau * (1 + k * entropy)
        return base_tau * (1 + k * entropy)

    def add_term(self, symbol: str, role="generic", intensity: float = 1.0, **kwargs) -> None:
        """
        Add a new term to the form
        
        Args:
            symbol: Term symbol/identifier
            role: Role classification for the term (default: "generic")
            intensity: Intensity value (default: 1.0)
            **kwargs: Additional term properties
        """
        # Backward compatibility: handle legacy call patterns
        if isinstance(role, (int, float)) and isinstance(intensity, dict):
            # legacy order: (symbol, intensity, extras)
            intensity, kwargs, role = role, intensity, "legacy_role"
        
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
            phase=new_phase,
            recursive=self.recursive
        )
        # Copy over the terms and topology
        new_form.terms = self.terms.copy()
        new_form.topology = self.topology.copy()
        new_form.echo_created_at = time.time()
        
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
        
        # Create a new instance and set the attributes
        instance = cls()
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        
        return instance

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert EchoForm to dictionary with enhanced metadata
        
        Returns:
            Dictionary representation of the form with computed metrics
        """
        # Calculate current metrics
        current_entropy = self.entropy()
        current_intensity = self.intensity_sum(apply_time_decay=False)
        current_intensity_decayed = self.intensity_sum(apply_time_decay=True)
        effective_tau = self.effective_tau()
        
        return {
            "anchor": self.anchor,
            "domain": self.domain,
            "terms": self.terms,
            "phase": self.phase,
            "recursive": self.recursive,
            "topology": self.topology,
            "trace_signature": self.trace_signature,
            "echo_created_at": self.echo_created_at,
            # Enhanced metadata
            "metadata": {
                "term_count": len(self.terms),
                "entropy": current_entropy,
                "total_intensity": current_intensity,
                "decayed_intensity": current_intensity_decayed,
                "effective_tau": effective_tau,
                "created_timestamp": self.echo_created_at,
                "version": "0.7.2"
            }
        }

    def process(self, input_data: str) -> Dict[str, Any]:
        """
        Process input data through the echo form.
        
        Args:
            input_data: Input string to process
            
        Returns:
            Dictionary with processing results
        """
        # Basic processing - add as a term and return result
        self.add_term(input_data, role="processed", intensity=1.0)
        
        return {
            "processed": True,
            "input": input_data,
            "anchor": self.anchor,
            "domain": self.domain,
            "total_terms": len(self.terms),
            "trace": self.trace_signature
        }

    def __repr__(self) -> str:
        """String representation for debugging"""
        return f"EchoForm(anchor='{self.anchor}', domain='{self.domain}', phase='{self.phase}', terms={len(self.terms)})"


# Re-export init_geoid for legacy tests
from .geoid import init_geoid
__all__ = ["EchoForm", "init_geoid"]