"""
CLS (Contradiction Lattice System) integration with EchoForm and Identity
Live lattice resolution with EchoForm storage and cls_event tracking
Now with persistent DuckDB storage backend and unified Identity model
Includes observability and entropy tracking
"""
from .echoform import EchoForm
from .geoid import Geoid  # Legacy support
from .identity import Identity, create_geoid_identity, create_scar_identity
from .storage import get_storage
import time
from typing import List, Dict, Any, Union

# Import observability hooks
try:
    from .observability import track_lattice_operation
    OBSERVABILITY_AVAILABLE = True
except ImportError:
    # Fallback if prometheus_client is not available
    OBSERVABILITY_AVAILABLE = False
    def track_lattice_operation(func):
        return func


@track_lattice_operation
def lattice_resolve(identity_a: Union[Identity, Geoid], identity_b: Union[Identity, Geoid]) -> float:
    """
    Live CLS lattice resolution with EchoForm storage and cls_event tracking
    Now uses persistent DuckDB storage backend and unified Identity model
    
    Args:
        identity_a: First identity (or legacy geoid) for lattice resolution
        identity_b: Second identity (or legacy geoid) for lattice resolution
        
    Returns:
        Intensity sum from the stored EchoForm
    """
    storage = get_storage()
    
    # Handle legacy Geoid objects by converting to Identity
    if isinstance(identity_a, Geoid):
        from .identity import geoid_to_identity
        identity_a = geoid_to_identity(identity_a)
    if isinstance(identity_b, Geoid):
        from .identity import geoid_to_identity
        identity_b = geoid_to_identity(identity_b)
    
    # Create unique anchor for this lattice pair
    anchor = f"{identity_a.id}_{identity_b.id}"
    
    # Check if we already have a form for this pair
    existing_form = storage.fetch_form(anchor)
    
    if existing_form:
        # Existing form - append cls_event term with entropy tracking
        entropy_a = identity_a.entropy()
        entropy_b = identity_b.entropy()
        avg_entropy = (entropy_a + entropy_b) / 2
        
        existing_form.add_term(
            symbol="cls_event",
            role="resonance_trigger",
            intensity=0.1 * (1 + avg_entropy),  # Entropy-weighted intensity
            timestamp=time.time(),
            event_type="lattice_resolve_repeat",
            entropy_a=entropy_a,
            entropy_b=entropy_b
        )
        storage.update_form(existing_form)
        
        # Store identity references if not already stored
        if not storage.fetch_identity(identity_a.id):
            storage.store_identity(identity_a)
        if not storage.fetch_identity(identity_b.id):
            storage.store_identity(identity_b)
            
        return existing_form.intensity_sum()
    else:
        # New form - create and store with identity references
        entropy_a = identity_a.entropy()
        entropy_b = identity_b.entropy()
        avg_entropy = (entropy_a + entropy_b) / 2
        
        echo = EchoForm(
            anchor=anchor,
            domain="cls",
            terms=[
                {
                    "symbol": "CLS", 
                    "role": "cls_seed", 
                    "intensity": 1.0
                },
                {
                    "symbol": "cls_event",
                    "role": "resonance_trigger",
                    "intensity": 0.1 * (1 + avg_entropy),  # Entropy-weighted
                    "timestamp": time.time(),
                    "event_type": "lattice_resolve_initial",
                    "entropy_a": entropy_a,
                    "entropy_b": entropy_b,
                    "identity_a_id": identity_a.id,
                    "identity_b_id": identity_b.id
                }
            ],
            phase="lattice_active"
        )
        
        # Store the identities and form
        storage.store_identity(identity_a)
        storage.store_identity(identity_b)
        storage.store_form(echo)
        
        return echo.intensity_sum()


def create_lattice_form(anchor: str, identity_a: Union[Identity, Geoid], identity_b: Union[Identity, Geoid]) -> EchoForm:
    """
    Create a full EchoForm for lattice operations and store it
    Now uses persistent DuckDB storage backend and unified Identity model
    
    Args:
        anchor: Custom anchor for the form
        identity_a: First identity (or legacy geoid)
        identity_b: Second identity (or legacy geoid)
        
    Returns:
        EchoForm configured for lattice operations
    """
    storage = get_storage()
    
    # Handle legacy Geoid objects by converting to Identity
    if isinstance(identity_a, Geoid):
        from .identity import geoid_to_identity
        identity_a = geoid_to_identity(identity_a)
    if isinstance(identity_b, Geoid):
        from .identity import geoid_to_identity
        identity_b = geoid_to_identity(identity_b)
    
    # Calculate entropy for adaptive intensity
    entropy_a = identity_a.entropy()
    entropy_b = identity_b.entropy()
    avg_entropy = (entropy_a + entropy_b) / 2
    
    form = EchoForm(
        anchor=anchor,
        domain="cls",
        terms=[
            {
                "symbol": f"∂{identity_a.id}", 
                "role": "identity_a", 
                "intensity": 0.5 * (1 + entropy_a),  # Entropy-weighted
                "identity_id": identity_a.id,
                "raw": identity_a.raw,
                "entropy": entropy_a
            },
            {
                "symbol": f"∂{identity_b.id}", 
                "role": "identity_b",
                "intensity": 0.5 * (1 + entropy_b),  # Entropy-weighted
                "identity_id": identity_b.id,
                "raw": identity_b.raw,
                "entropy": entropy_b
            },
            {
                "symbol": "cls_event",
                "role": "creation_event",
                "intensity": 0.1 * (1 + avg_entropy),
                "timestamp": time.time(),
                "event_type": "lattice_form_created",
                "avg_entropy": avg_entropy
            }
        ],
        phase="lattice_active",
        topology={
            "lattice_type": "contradiction",
            "identity_pair": [identity_a.id, identity_b.id],
            "created_from": "cls_lattice_resolve",
            "entropy_metrics": {
                "identity_a_entropy": entropy_a,
                "identity_b_entropy": entropy_b,
                "avg_entropy": avg_entropy
            }
        }
    )
    
    # Store the identities and form
    storage.store_identity(identity_a)
    storage.store_identity(identity_b)
    storage.store_form(form)
    return form


def get_stored_forms() -> Dict[str, EchoForm]:
    """
    Get all stored lattice forms (for testing/debugging)
    Now retrieves from persistent storage
    
    Returns:
        Dictionary of stored EchoForms keyed by anchor
    """
    storage = get_storage()
    forms_metadata = storage.list_forms(limit=1000, domain="cls")
    
    result = {}
    for meta in forms_metadata:
        form = storage.fetch_form(meta["anchor"])
        if form:
            result[meta["anchor"]] = form
    
    return result


def create_identity_lattice(raw_a: str, raw_b: str, tags_a: List[str] = None, tags_b: List[str] = None) -> float:
    """
    Create two identities and perform lattice resolution
    Convenience function for creating new identity pairs
    
    Args:
        raw_a: Raw content for first identity
        raw_b: Raw content for second identity
        tags_a: Optional tags for first identity
        tags_b: Optional tags for second identity
        
    Returns:
        Intensity sum from lattice resolution
    """
    identity_a = create_geoid_identity(raw_a, tags=tags_a or [])
    identity_b = create_geoid_identity(raw_b, tags=tags_b or [])
    
    return lattice_resolve(identity_a, identity_b)


def create_scar_lattice(identity_a: Identity, identity_b: Identity, relationship: str = "contradiction") -> float:
    """
    Create a scar-type identity from two existing identities and perform lattice resolution
    
    Args:
        identity_a: First identity
        identity_b: Second identity
        relationship: Type of relationship (default: "contradiction")
        
    Returns:
        Intensity sum from lattice resolution
    """
    # Create scar identity representing the relationship
    scar_identity = create_scar_identity(
        raw=f"Relationship: {relationship}",
        relationships=[
            {"target_id": identity_a.id, "type": relationship, "strength": 0.8},
            {"target_id": identity_b.id, "type": relationship, "strength": 0.8}
        ],
        tags=["lattice_scar", relationship]
    )
    
    # Perform lattice resolution between the scar and one of the original identities
    return lattice_resolve(scar_identity, identity_a)


def get_identity_lattice_metrics(identity_id: str) -> Dict[str, Any]:
    """
    Get lattice metrics for a specific identity
    
    Args:
        identity_id: ID of the identity to analyze
        
    Returns:
        Dictionary containing lattice metrics
    """
    storage = get_storage()
    
    # Get the identity
    identity = storage.fetch_identity(identity_id)
    if not identity:
        return {"error": "Identity not found"}
    
    # Find all forms that reference this identity
    forms_metadata = storage.list_forms(limit=1000, domain="cls")
    related_forms = []
    
    for meta in forms_metadata:
        form = storage.fetch_form(meta["anchor"])
        if form and identity_id in str(form.topology):
            related_forms.append(form)
    
    # Calculate metrics
    total_intensity = sum(form.intensity_sum() for form in related_forms)
    avg_entropy = identity.entropy()
    effective_tau = identity.effective_tau()
    
    return {
        "identity_id": identity_id,
        "entropy": avg_entropy,
        "effective_tau": effective_tau,
        "related_forms_count": len(related_forms),
        "total_lattice_intensity": total_intensity,
        "avg_form_intensity": total_intensity / len(related_forms) if related_forms else 0,
        "lattice_participation": len(related_forms)  # How many lattice operations this identity has participated in
    }


def clear_stored_forms() -> None:
    """
    Clear all stored lattice forms (for testing)
    Now clears from persistent storage
    """
    storage = get_storage()
    # For testing, we'll delete all CLS domain forms
    storage._conn.execute("DELETE FROM echoforms WHERE domain = 'cls'")


def get_form_by_anchor(anchor: str) -> EchoForm:
    """
    Retrieve a specific stored form by anchor
    Now retrieves from persistent storage
    
    Args:
        anchor: The anchor key for the form
        
    Returns:
        The stored EchoForm
        
    Raises:
        KeyError: If anchor not found
    """
    storage = get_storage()
    form = storage.fetch_form(anchor)
    if form is None:
        raise KeyError(f"No form found with anchor: {anchor}")
    return form