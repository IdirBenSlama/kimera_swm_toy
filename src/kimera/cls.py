"""
CLS (Contradiction Lattice System) integration with EchoForm
Live lattice resolution with EchoForm storage and cls_event tracking
"""
from .echoform import EchoForm
from .geoid import Geoid
import time
from typing import List, Dict, Any

# In-memory storage for EchoForms (in production this would be persistent)
_lattice_forms: Dict[str, EchoForm] = {}


def lattice_resolve(geo_a: Geoid, geo_b: Geoid) -> float:
    """
    Live CLS lattice resolution with EchoForm storage and cls_event tracking
    
    Args:
        geo_a: First geoid for lattice resolution
        geo_b: Second geoid for lattice resolution
        
    Returns:
        Intensity sum from the stored EchoForm
    """
    # Create unique anchor for this lattice pair
    anchor = f"{geo_a.gid}_{geo_b.gid}"
    
    # Check if we already have a form for this pair
    if anchor in _lattice_forms:
        # Existing form - append cls_event term
        existing_form = _lattice_forms[anchor]
        existing_form.add_term(
            symbol="cls_event",
            role="resonance_trigger",
            intensity=0.1,
            timestamp=time.time(),
            event_type="lattice_resolve_repeat"
        )
        _lattice_forms[anchor] = existing_form
        return existing_form.intensity_sum()
    else:
        # New form - create and store
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
                    "intensity": 0.1,
                    "timestamp": time.time(),
                    "event_type": "lattice_resolve_initial"
                }
            ],
            phase="lattice_active"
        )
        
        # Store the form
        _lattice_forms[anchor] = echo
        
        return echo.intensity_sum()


def create_lattice_form(anchor: str, geo_a: Geoid, geo_b: Geoid) -> EchoForm:
    """
    Create a full EchoForm for lattice operations and store it
    
    Args:
        anchor: Custom anchor for the form
        geo_a: First geoid
        geo_b: Second geoid
        
    Returns:
        EchoForm configured for lattice operations
    """
    form = EchoForm(
        anchor=anchor,
        domain="cls",
        terms=[
            {
                "symbol": f"∂{geo_a.gid}", 
                "role": "geoid_a", 
                "intensity": 0.5,
                "gid": geo_a.gid,
                "raw": geo_a.raw
            },
            {
                "symbol": f"∂{geo_b.gid}", 
                "role": "geoid_b", 
                "intensity": 0.5,
                "gid": geo_b.gid,
                "raw": geo_b.raw
            },
            {
                "symbol": "cls_event",
                "role": "creation_event",
                "intensity": 0.1,
                "timestamp": time.time(),
                "event_type": "lattice_form_created"
            }
        ],
        phase="lattice_active",
        topology={
            "lattice_type": "contradiction",
            "geoid_pair": [geo_a.gid, geo_b.gid],
            "created_from": "cls_lattice_resolve"
        }
    )
    
    # Store the form
    _lattice_forms[anchor] = form
    return form


def get_stored_forms() -> Dict[str, EchoForm]:
    """
    Get all stored lattice forms (for testing/debugging)
    
    Returns:
        Dictionary of stored EchoForms keyed by anchor
    """
    return _lattice_forms.copy()


def clear_stored_forms() -> None:
    """
    Clear all stored lattice forms (for testing)
    """
    global _lattice_forms
    _lattice_forms.clear()


def get_form_by_anchor(anchor: str) -> EchoForm:
    """
    Retrieve a specific stored form by anchor
    
    Args:
        anchor: The anchor key for the form
        
    Returns:
        The stored EchoForm
        
    Raises:
        KeyError: If anchor not found
    """
    return _lattice_forms[anchor]