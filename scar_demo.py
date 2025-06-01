#!/usr/bin/env python3
"""
Demonstration of Scar functionality in Kimera's unified Identity system.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from kimera.identity import Identity, create_scar_identity, create_geoid_identity
from kimera.storage import LatticeStorage


def main():
    """Demonstrate Scar functionality"""
    print("🔗 Kimera Scar Demonstration")
    print("=" * 50)
    
    # Use in-memory database for demo
    storage = LatticeStorage(":memory:")
    
    print("\n1. Creating content identities (former Geoids)...")
    
    # Create some content identities
    concept_a = create_geoid_identity(
        "Artificial Intelligence is transforming society",
        tags=["AI", "technology", "society"]
    )
    
    concept_b = create_geoid_identity(
        "Machine learning requires large datasets",
        tags=["ML", "data", "technology"]
    )
    
    concept_c = create_geoid_identity(
        "Privacy concerns in data collection",
        tags=["privacy", "data", "ethics"]
    )
    
    # Store the concepts
    storage.store_identity(concept_a)
    storage.store_identity(concept_b)
    storage.store_identity(concept_c)
    
    print(f"✅ Created concept A: {concept_a.raw[:40]}...")
    print(f"✅ Created concept B: {concept_b.raw[:40]}...")
    print(f"✅ Created concept C: {concept_c.raw[:40]}...")
    
    print("\n2. Creating relationship identities (Scars)...")
    
    # Create scars to represent relationships
    scar_1 = create_scar_identity(
        concept_a.id, concept_b.id, 
        weight=0.8
    )
    scar_1.meta = {
        "relationship_type": "supports",
        "description": "AI relies on ML techniques"
    }
    
    scar_2 = create_scar_identity(
        concept_b.id, concept_c.id,
        weight=0.6
    )
    scar_2.meta = {
        "relationship_type": "conflicts",
        "description": "ML data needs vs privacy concerns"
    }
    
    # Create a complex scar with multiple relationships
    complex_scar = Identity(
        identity_type="scar",
        related_ids=[concept_a.id, concept_b.id, concept_c.id],
        weight=0.9,
        meta={
            "relationship_type": "triangular_tension",
            "description": "AI-ML-Privacy triangle"
        }
    )
    
    # Store the scars
    storage.store_identity(scar_1)
    storage.store_identity(scar_2)
    storage.store_identity(complex_scar)
    
    print(f"✅ Created scar 1: {scar_1.meta['description']}")
    print(f"✅ Created scar 2: {scar_2.meta['description']}")
    print(f"✅ Created complex scar: {complex_scar.meta['description']}")
    
    print("\n3. Analyzing entropy and time decay...")
    
    # Calculate entropy for different identity types
    print(f"Concept A entropy: {concept_a.entropy():.3f}")
    print(f"Concept B entropy: {concept_b.entropy():.3f}")
    print(f"Simple scar entropy: {scar_1.entropy():.3f}")
    print(f"Complex scar entropy: {complex_scar.entropy():.3f}")
    
    # Calculate effective tau (time decay constants)
    print(f"\nTime decay constants:")
    print(f"Concept A tau: {concept_a.effective_tau():.1f} seconds")
    print(f"Simple scar tau: {scar_1.effective_tau():.1f} seconds")
    print(f"Complex scar tau: {complex_scar.effective_tau():.1f} seconds")
    
    print("\n4. Querying the unified storage...")
    
    # Get counts by type
    total_count = storage.get_identity_count()
    geoid_count = storage.get_identity_count("geoid")
    scar_count = storage.get_identity_count("scar")
    
    print(f"Total identities: {total_count}")
    print(f"Content identities (geoids): {geoid_count}")
    print(f"Relationship identities (scars): {scar_count}")
    
    # Find identities by entropy
    high_entropy = storage.find_identities_by_entropy(min_entropy=1.0)
    print(f"High entropy identities: {len(high_entropy)}")
    
    # List all scars
    all_scars = storage.list_identities(identity_type="scar")
    print(f"\nAll scars in storage:")
    for scar_info in all_scars:
        scar_obj = storage.fetch_identity(scar_info["id"])
        if scar_obj and "description" in scar_obj.meta:
            print(f"  - {scar_obj.meta['description']} (entropy: {scar_obj.entropy():.3f})")
    
    print("\n5. Demonstrating unified identity model benefits...")
    
    print("✅ Single storage system for both content and relationships")
    print("✅ Entropy-based intelligence (complex relationships decay slower)")
    print("✅ Unified querying and analytics")
    print("✅ Extensible metadata system")
    print("✅ Backward compatibility with legacy models")
    
    storage.close()
    
    print("\n" + "=" * 50)
    print("🎉 Scar demonstration complete!")
    print("\nScars enable Kimera to:")
    print("• Track relationships between concepts")
    print("• Apply entropy-based time decay to relationships")
    print("• Store relationship metadata and context")
    print("• Query across both content and relationships")
    print("• Scale relationship complexity with entropy")


if __name__ == "__main__":
    main()