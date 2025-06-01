# Scar Implementation Guide

## Overview

Scars are now fully implemented as part of Kimera's unified Identity system. They represent **relationship-based identities** that track connections, contradictions, and associations between concepts.

## What Are Scars?

Scars are lightweight relationship markers that:
- **Connect multiple identities** through `related_ids`
- **Have weighted relationships** via the `weight` field
- **Calculate entropy** based on relationship complexity
- **Support metadata** for relationship context
- **Use entropy-based time decay** (complex relationships last longer)

## Key Features

### 1. Unified Storage
```python
# Both content and relationships use the same storage
storage = LatticeStorage("kimera.db")

# Store a content identity
geoid = create_geoid_identity("AI is transforming society")
storage.store_identity(geoid)

# Store a relationship identity
scar = create_scar_identity(geoid.id, "external_concept", weight=0.8)
storage.store_identity(scar)
```

### 2. Entropy-Based Intelligence
```python
# Simple relationship (2 connections)
simple_scar = create_scar_identity("id1", "id2")
print(f"Simple entropy: {simple_scar.entropy():.3f}")  # ~1.0

# Complex relationship (5 connections)
complex_scar = Identity(
    identity_type="scar",
    related_ids=["id1", "id2", "id3", "id4", "id5"],
    weight=1.0
)
print(f"Complex entropy: {complex_scar.entropy():.3f}")  # ~2.3
```

### 3. Adaptive Time Decay
```python
# Higher entropy = slower decay
simple_tau = simple_scar.effective_tau()  # ~14 days
complex_tau = complex_scar.effective_tau()  # ~16+ days

print(f"Simple scar decays in {simple_tau/86400:.1f} days")
print(f"Complex scar decays in {complex_tau/86400:.1f} days")
```

### 4. Rich Metadata Support
```python
scar = create_scar_identity("concept_a", "concept_b", weight=0.9)
scar.meta = {
    "relationship_type": "contradicts",
    "strength": "strong",
    "context": "philosophical debate",
    "discovered_at": "2024-12-19T10:30:00Z"
}
```

## Creating Scars

### Simple Binary Relationship
```python
from kimera.identity import create_scar_identity

# Create a scar between two concepts
scar = create_scar_identity(
    id1="concept_a_id",
    id2="concept_b_id", 
    weight=0.7
)
```

### Complex Multi-Way Relationship
```python
from kimera.identity import Identity

# Create a scar with multiple connections
complex_scar = Identity(
    identity_type="scar",
    related_ids=["id1", "id2", "id3", "id4"],
    weight=0.9,
    meta={
        "relationship_type": "cluster",
        "description": "Related concepts in AI ethics"
    }
)
```

### Relationship Types Examples
```python
# Contradiction
contradiction = create_scar_identity("thesis", "antithesis", weight=0.8)
contradiction.meta = {"type": "contradicts"}

# Support/Evidence
support = create_scar_identity("claim", "evidence", weight=0.9)
support.meta = {"type": "supports"}

# Reference/Citation
reference = create_scar_identity("paper", "cited_work", weight=0.6)
reference.meta = {"type": "references"}

# Similarity/Analogy
similarity = create_scar_identity("concept_x", "concept_y", weight=0.7)
similarity.meta = {"type": "similar_to"}
```

## Storage and Retrieval

### Storing Scars
```python
storage = LatticeStorage("kimera.db")

# Store individual scar
storage.store_identity(scar)

# Batch store multiple scars
scars = [scar1, scar2, scar3]
for scar in scars:
    storage.store_identity(scar)
```

### Querying Scars
```python
# Get all scars
all_scars = storage.list_identities(identity_type="scar")

# Find scars by entropy range
high_entropy_scars = storage.find_identities_by_entropy(
    min_entropy=1.5, 
    max_entropy=3.0
)

# Get specific scar
scar = storage.fetch_identity("scar_id")
```

### Mixed Queries
```python
# Get counts by type
total = storage.get_identity_count()
geoids = storage.get_identity_count("geoid")
scars = storage.get_identity_count("scar")

print(f"Total: {total}, Content: {geoids}, Relationships: {scars}")
```

## Entropy Calculation

Scars use **relationship entropy** based on the number of connections:

```python
def calculate_relationship_entropy(related_ids, weight=1.0):
    """
    Calculate entropy for relationship-based identity.
    More connections = higher entropy = slower decay
    """
    if not related_ids:
        return 0.0
    
    n_relations = len(related_ids)
    if n_relations <= 1:
        return 0.0
    
    # Shannon entropy for uniform distribution over relations
    base_entropy = math.log2(n_relations)
    
    # Weight adjustment
    return base_entropy * weight
```

## Time Decay Behavior

Scars with higher entropy decay more slowly:

```python
# Base tau = 14 days
base_tau = 14 * 24 * 3600  # seconds

# Entropy scaling factor
k = 0.1

# Effective tau calculation
effective_tau = base_tau * (1 + k * entropy)

# Examples:
# 2 connections: entropy ~1.0 → tau ~15.4 days
# 4 connections: entropy ~2.0 → tau ~16.8 days  
# 8 connections: entropy ~3.0 → tau ~18.2 days
```

## Integration with EchoForms

Scars can be created from EchoForm processing:

```python
from kimera.echoform import EchoForm

# Process text that contains relationships
form = EchoForm(
    anchor="ai_ethics_discussion",
    raw="AI development conflicts with privacy concerns but supports innovation"
)

# Extract relationships and create scars
# (This would be done by higher-level processing)
ai_privacy_conflict = create_scar_identity("ai_dev", "privacy", weight=0.8)
ai_privacy_conflict.meta = {"type": "conflicts", "source": form.anchor}

ai_innovation_support = create_scar_identity("ai_dev", "innovation", weight=0.9)
ai_innovation_support.meta = {"type": "supports", "source": form.anchor}
```

## Migration from Legacy Scars

If you have existing Scar objects, use the migration utilities:

```python
from kimera.identity import scar_to_identity

# Convert legacy scar to unified identity
legacy_scar = OldScar(gid_pair=("id1", "id2"), weight=0.7)
new_identity = scar_to_identity(legacy_scar)

# Store in unified system
storage.store_identity(new_identity)
```

## Best Practices

### 1. Use Meaningful Weights
```python
# Strong relationships
strong_scar = create_scar_identity("cause", "effect", weight=0.9)

# Weak relationships  
weak_scar = create_scar_identity("topic_a", "topic_b", weight=0.3)
```

### 2. Add Rich Metadata
```python
scar.meta = {
    "relationship_type": "contradicts",
    "confidence": 0.85,
    "source": "academic_paper_xyz",
    "context": "philosophical_debate",
    "discovered_by": "nlp_processor_v2"
}
```

### 3. Use Appropriate Granularity
```python
# Fine-grained: specific relationships
specific = create_scar_identity("concept_a", "concept_b", weight=0.8)

# Coarse-grained: cluster relationships
cluster = Identity(
    identity_type="scar",
    related_ids=["concept_a", "concept_b", "concept_c", "concept_d"],
    weight=0.7,
    meta={"type": "cluster", "theme": "ai_ethics"}
)
```

### 4. Monitor Entropy Distribution
```python
# Check entropy distribution in your dataset
scars = storage.list_identities(identity_type="scar")
entropies = []

for scar_info in scars:
    scar = storage.fetch_identity(scar_info["id"])
    entropies.append(scar.entropy())

print(f"Average scar entropy: {sum(entropies)/len(entropies):.3f}")
print(f"Entropy range: {min(entropies):.3f} - {max(entropies):.3f}")
```

## Testing Scars

Run the test suite to verify scar functionality:

```bash
# Run scar-specific tests
python test_scar_functionality.py

# Run the demonstration
python scar_demo.py

# Run full unified identity tests
python test_unified_identity.py
```

## Summary

Scars in Kimera's unified Identity system provide:

✅ **Relationship tracking** between any identities  
✅ **Entropy-based intelligence** for complex relationships  
✅ **Unified storage** with content identities  
✅ **Rich metadata** support for relationship context  
✅ **Adaptive time decay** based on relationship complexity  
✅ **Backward compatibility** with legacy systems  
✅ **Extensible design** for future relationship types  

The unified approach eliminates the complexity of managing separate Geoid and Scar models while providing more powerful relationship modeling capabilities.