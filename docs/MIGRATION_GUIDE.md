# Migration Guide: Fixing Broken Components

This guide helps you migrate from broken components to working versions.

## 1. Contradiction Detection

### ❌ OLD (Broken)
```python
from kimera.contradiction import detect_contradiction

# This fails to detect "sky is blue" vs "sky is red"
is_contra, conf, reason = detect_contradiction(g1, g2)
```

### ✅ NEW (Working)
```python
from kimera.contradiction_v2_fixed import analyze_contradiction

# This correctly detects contradictions
analysis = analyze_contradiction(g1, g2)
if analysis.is_contradiction:
    print(f"Type: {analysis.contradiction_type}")
    print(f"Confidence: {analysis.confidence}")
```

## 2. Thermodynamic System

### ❌ OLD (Broken)
```python
from kimera.thermodynamics import ThermodynamicSystem

# This classifies everything as plasma
system = ThermodynamicSystem()
phases = system.phase_diagram(geoids)  # All plasma!
```

### ✅ NEW (Working)
```python
from kimera.thermodynamics_v3 import ThermodynamicSystemV3

# This produces meaningful phase distributions
system = ThermodynamicSystemV3()
phase_diagram, states = system.generate_phase_diagram(geoids)
```

## 3. Performance Claims

### ❌ OLD (False)
```python
# Documentation claims:
# - "Efficient resonance calculation (~3,000 pairs/second)
# - "O(n log n) complexity"
# - "~1.5 GB for 1M concepts
```

### ✅ NEW (Honest)
```python
# Actual measurements:
# - ~3,000 pairs/second resonance calculation
# - O(n²) for pairwise operations
# - ~1.5GB for 1M concepts
```

## 4. Import Structure

### Recommended Imports
```python
# Core (working)
from kimera.geoid import init_geoid
from kimera.resonance import resonance
from kimera.mathematics.spectral import resonance_spectrum

# Fixed versions
from kimera.contradiction_v2_fixed import analyze_contradiction
from kimera.thermodynamics_v3 import ThermodynamicSystemV3

# Avoid these
# from kimera.contradiction import detect_contradiction  # Broken
# from kimera.thermodynamics import ThermodynamicSystem  # Broken
```

## 5. Code Patterns

### Contradiction Checking
```python
def check_contradiction(text1, text2):
    """Use the fixed contradiction detection."""
    g1 = init_geoid(text1)
    g2 = init_geoid(text2)
    
    analysis = analyze_contradiction(g1, g2)
    
    return {
        'is_contradiction': analysis.is_contradiction,
        'confidence': analysis.confidence,
        'type': analysis.contradiction_type,
        'reasoning': analysis.reasoning
    }
```

### Phase Analysis
```python
def analyze_text_phases(texts):
    """Use the working thermodynamic system."""
    geoids = [init_geoid(t) for t in texts]
    system = ThermodynamicSystemV3()
    
    phase_diagram, states = system.generate_phase_diagram(geoids)
    
    # Count phases
    phase_counts = {
        phase: len(states_list) 
        for phase, states_list in phase_diagram.items()
    }
    
    return phase_counts, states
```

### Performance-Aware Processing
```python
def process_large_corpus(texts, batch_size=100):
    """Process in batches to manage memory."""
    results = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        geoids = [init_geoid(t) for t in batch]
        
        # Process batch
        # ... your processing here ...
        
        # Clear memory
        del geoids
        
    return results
```

## 6. Testing Your Migration

```python
def test_migration():
    """Verify the migration worked."""
    
    # Test contradiction detection
    g1 = init_geoid("The sky is blue")
    g2 = init_geoid("The sky is red")
    
    analysis = analyze_contradiction(g1, g2)
    assert analysis.is_contradiction == True, "Should detect color contradiction"
    
    # Test thermodynamics
    texts = ["Water is H2O", "Ice is frozen water", "The sky is blue", "The sky is red"]
    geoids = [init_geoid(t) for t in texts]
    
    system = ThermodynamicSystemV3()
    phase_diagram, _ = system.generate_phase_diagram(geoids)
    
    phases_with_content = sum(1 for states in phase_diagram.values() if states)
    assert phases_with_content >= 2, "Should produce multiple phases"
    
    print("✅ Migration successful!")
```

## 7. Updating Documentation

Replace false claims in your documentation:

| Old Claim | Reality |
|-----------|---------|
| "Efficient resonance calculation (~3,000 pairs/second)
| "O(n log n) complexity" | Actually O(n²) |
| "~1.5 GB for 1M concepts
| "94% accuracy" | No benchmark data |

## Summary

1. Use `contradiction_v2_fixed` instead of `contradiction`
2. Use `thermodynamics_v3` instead of `thermodynamics`
3. Remove false performance claims
4. Process large datasets in batches
5. Test everything empirically

Remember: **Honest assessment leads to better science**.