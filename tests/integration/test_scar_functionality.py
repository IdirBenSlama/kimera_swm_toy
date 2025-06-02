#!/usr/bin/env python3
"""
Integration tests for SCAR functionality
"""
import sys
import os
sys.path.insert(0, 'src')

import pytest
from kimera.identity import Identity
from kimera.storage import LatticeStorage

@pytest.fixture
def scar_storage():
    """Create a temporary storage instance for SCAR testing"""
    test_db = "test_scar.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    storage = LatticeStorage(db_path=test_db)
    yield storage
    
    # Cleanup - close connection first
    storage.close()
    if os.path.exists(test_db):
        os.remove(test_db)

def test_scar_creation_and_storage(scar_storage):
    """Test creating and storing scars"""
    # Create base identities
    id1 = Identity(content="concept A")
    id2 = Identity(content="concept B")
    
    scar_storage.store_identity(id1)
    scar_storage.store_identity(id2)
    
    # Create scar connecting them
    scar = Identity.create_scar(
        content="contradiction between A and B",
        related_ids=[id1.id, id2.id],
        metadata={
            "relationship_type": "contradiction",
            "strength": 0.8,
            "context": "logical inconsistency"
        }
    )
    
    # Store scar
    scar_storage.store_identity(scar)
    
    # Verify scar was stored correctly
    retrieved_scar = scar_storage.get_identity(scar.id)
    assert retrieved_scar is not None
    assert retrieved_scar.identity_type == "scar"
    assert retrieved_scar.metadata["relationship_type"] == "contradiction"
    assert retrieved_scar.metadata["strength"] == 0.8

def test_scar_relationship_queries(scar_storage):
    """Test querying relationships through scars"""
    # Create test identities
    concept_a = Identity(content="concept A")
    concept_b = Identity(content="concept B") 
    concept_c = Identity(content="concept C")
    
    scar_storage.store_identity(concept_a)
    scar_storage.store_identity(concept_b)
    scar_storage.store_identity(concept_c)
    
    # Create scars
    scar1 = Identity.create_scar(
        content="A contradicts B",
        related_ids=[concept_a.id, concept_b.id],
        metadata={"relationship_type": "contradiction"}
    )
    
    scar2 = Identity.create_scar(
        content="A similar to C",
        related_ids=[concept_a.id, concept_c.id],
        metadata={"relationship_type": "similarity"}
    )
    
    scar_storage.store_identity(scar1)
    scar_storage.store_identity(scar2)
    
    # Query for scars related to concept A
    related_scars = scar_storage.get_related_scars(concept_a.id)
    assert len(related_scars) >= 2
    
    # Verify relationship types
    relationship_types = [scar.metadata.get("relationship_type") for scar in related_scars]
    assert "contradiction" in relationship_types
    assert "similarity" in relationship_types

def test_scar_contradiction_detection(scar_storage):
    """Test detecting contradictions through scars"""
    # Create contradictory concepts
    statement1 = Identity(content="The sky is blue")
    statement2 = Identity(content="The sky is red")
    
    scar_storage.store_identity(statement1)
    scar_storage.store_identity(statement2)
    
    # Create contradiction scar
    contradiction = Identity.create_scar(
        content="Color contradiction",
        related_ids=[statement1.id, statement2.id],
        metadata={
            "relationship_type": "contradiction",
            "strength": 0.9,
            "reason": "mutually exclusive color claims"
        }
    )
    
    scar_storage.store_identity(contradiction)
    
    # Find contradictions
    contradictions = scar_storage.get_scars_by_type("contradiction")
    assert len(contradictions) >= 1
    
    # Verify contradiction details
    found_contradiction = next(
        (s for s in contradictions if s.id == contradiction.id), 
        None
    )
    assert found_contradiction is not None
    assert found_contradiction.metadata["strength"] == 0.9
    assert "mutually exclusive" in found_contradiction.metadata["reason"]

def test_scar_graph_traversal(scar_storage):
    """Test traversing relationships through scars"""
    # Create a chain of related concepts
    concepts = [
        Identity(content=f"concept {i}") 
        for i in range(5)
    ]
    
    # Store concepts
    for concept in concepts:
        scar_storage.store_identity(concept)
    
    # Create chain of relationships
    scars = []
    for i in range(len(concepts) - 1):
        scar = Identity.create_scar(
            content=f"link {i} to {i+1}",
            related_ids=[concepts[i].id, concepts[i+1].id],
            metadata={"relationship_type": "sequence"}
        )
        scars.append(scar)
        scar_storage.store_identity(scar)
    
    # Test traversal from first concept
    start_concept = concepts[0]
    related_scars = scar_storage.get_related_scars(start_concept.id)
    
    # Should find at least one relationship
    assert len(related_scars) >= 1
    
    # Verify we can follow the chain
    sequence_scars = [
        s for s in related_scars 
        if s.metadata.get("relationship_type") == "sequence"
    ]
    assert len(sequence_scars) >= 1

if __name__ == "__main__":
    print("Run these tests with: python -m pytest tests/integration/test_scar_functionality.py -v")