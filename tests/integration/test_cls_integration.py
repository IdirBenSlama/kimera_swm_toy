#!/usr/bin/env python3
"""
Test CLS lattice integration with EchoForm storage and cls_event tracking
Now with persistent DuckDB storage backend
"""
import sys
import math
import os
sys.path.insert(0, 'src')

import pytest
from kimera.cls import (
    lattice_resolve, 
    create_lattice_form, 
    get_stored_forms,
    create_identity_lattice,
    create_scar_lattice,
    get_identity_lattice_metrics,
    clear_stored_forms
)
from kimera.storage import get_storage
from kimera.identity import Identity, create_geoid_identity

def test_cls_basic_integration():
    """Test basic CLS integration"""
    # Clear any existing forms
    clear_stored_forms()
    
    # Create two identities
    identity_a = create_geoid_identity("test content A", tags=["test"])
    identity_b = create_geoid_identity("test content B", tags=["test"])
    
    # Perform lattice resolution
    result = lattice_resolve(identity_a, identity_b)
    assert result > 0  # Should return intensity sum
    
    # Check that form was stored
    forms = get_stored_forms()
    assert len(forms) == 1
    
def test_cls_storage_integration():
    """Test CLS integration with storage"""
    clear_stored_forms()
    storage = get_storage()
    
    # Create identities and perform lattice resolution
    result = create_identity_lattice("content A", "content B", ["tag1"], ["tag2"])
    assert result > 0
    
    # Verify identities were stored
    # Note: We can't directly fetch by content, but we can check forms exist
    forms = get_stored_forms()
    assert len(forms) == 1

def test_cls_lattice_operations():
    """Test CLS lattice operations"""
    clear_stored_forms()
    
    # Create identities
    identity_a = create_geoid_identity("test A")
    identity_b = create_geoid_identity("test B")
    
    # Create custom lattice form
    form = create_lattice_form("custom_anchor", identity_a, identity_b)
    assert form is not None
    assert form.anchor == "custom_anchor"
    
    # Test scar lattice
    scar_result = create_scar_lattice(identity_a, identity_b, "contradiction")
    assert scar_result > 0
    
    # Test metrics
    metrics = get_identity_lattice_metrics(identity_a.id)
    assert "entropy" in metrics
    assert "lattice_participation" in metrics

if __name__ == "__main__":
    test_cls_basic_integration()
    test_cls_storage_integration()
    test_cls_lattice_operations()
    print("✅ All CLS integration tests passed!")