# Thermodynamics in Kimera-SWM

## Overview

The thermodynamics module implements physics-inspired concepts for modeling knowledge dynamics in the Spherical Word Methodology (SWM). It treats knowledge units (Geoids) as thermodynamic systems that can accumulate pressure, undergo phase transitions, and exchange energy.

## Core Concepts

### 1. Semantic Pressure

Semantic pressure represents the accumulated tension within a Geoid due to contradictions, paradoxes, or incompatible information. Like physical pressure, it can drive transformations.

```python
from kimera import create_thermodynamic_system, init_geoid

# Create a thermodynamic system
thermo = create_thermodynamic_system(pressure_threshold=10.0)

# Create geoids
statement = init_geoid("Light is a wave", lang="en")
contradictions = [
    init_geoid("Light is a particle", lang="en"),
    init_geoid("Light cannot be both wave and particle", lang="en")
]

# Calculate pressure
pressure = thermo.calculate_pressure(statement, contradictions)
```

**Pressure Sources:**
- Direct contradictions (detected via contradiction module)
- Low resonance (semantic opposition)
- High resonance paradoxes (when contradictory statements also resonate)

### 2. Constructive Collapse and Voids

When semantic pressure exceeds a threshold, Geoids undergo "constructive collapse," creating conceptual voids. These voids represent spaces where old understanding has broken down, allowing new frameworks to emerge.

```python
# Check if collapse should occur
should_collapse, collapse_type = thermo.check_collapse_conditions(geoid)

if should_collapse:
    # Perform collapse
    void = thermo.constructive_collapse(geoid, collapse_type)
    
    # Void properties
    print(f"Collapse pressure: {void.collapse_pressure}")
    print(f"Potential energy: {void.potential_energy}")
    print(f"Dimensions: {void.dimensions}")
```

**Collapse Types:**
- **Transformation**: Standard collapse from moderate pressure
- **Fragmentation**: Multiple contradictions cause the concept to break apart
- **Implosion**: Extreme pressure causes deep restructuring

### 3. Phase Transitions

Geoids exist in different "phases" based on their pressure and coherence:

```python
# Classify geoids by phase
phases = thermo.phase_diagram(geoid_list)

# Phases:
# - Solid: Stable, low pressure, high coherence
# - Liquid: Flexible, moderate pressure/coherence  
# - Gas: Volatile, higher pressure, lower coherence
# - Plasma: Near collapse, extreme pressure
```

### 4. Energy Transfer

Geoids can exchange "energy" (representing attention, influence, or information flow):

```python
# Transfer energy between geoids
result = thermo.energy_transfer(source_geoid, target_geoid, amount=5.0)

print(f"Transfer efficiency: {result['efficiency']}")
print(f"Energy transferred: {result['transferred']}")
print(f"Pressure created: {result['pressure_created']}")
```

Transfer efficiency depends on resonance between geoids. Energy transfer to contradicting geoids creates pressure.

### 5. System Entropy

The module calculates Shannon entropy to measure information diversity:

```python
# Calculate system entropy
entropy = thermo.calculate_system_entropy(geoid_list)

# Higher entropy = more diverse information
# Lower entropy = more uniform/concentrated information
```

### 6. Equilibrium Analysis

Find stability points for geoids within their context:

```python
# Analyze equilibrium
equilibrium = thermo.find_equilibrium_point(geoid, context_geoids)

print(f"Pressure: {equilibrium['pressure']}")
print(f"Coherence: {equilibrium['coherence']}")
print(f"Stability: {equilibrium['stability']}")
print(f"In equilibrium: {equilibrium['equilibrium']}")
```

## Practical Applications

### 1. Paradox Resolution

The thermodynamic framework models how paradoxes create pressure that leads to new understanding:

```python
# The Liar's Paradox creates extreme pressure
liar = init_geoid("This statement is false")

# Pressure from logical analysis
sources = [
    init_geoid("If true then false"),
    init_geoid("If false then true"),
    init_geoid("Logic must be consistent")
]

# High pressure leads to collapse
# From the void emerges: multi-valued logic, paraconsistent logic, etc.
```

### 2. Scientific Revolutions

Model paradigm shifts as phase transitions:

```python
# Classical physics under pressure from quantum experiments
classical = init_geoid("Physics is deterministic")
quantum_evidence = [
    init_geoid("Quantum measurements are probabilistic"),
    init_geoid("Uncertainty principle limits knowledge"),
    init_geoid("Wave function collapse is random")
]

# Pressure builds until classical framework collapses
# Void allows quantum mechanics to emerge
```

### 3. Conceptual Evolution

Track how ideas evolve through phase space:

```python
# Monitor phase transitions over time
initial_phases = thermo.phase_diagram(concepts)

# Add new information/contradictions
# ...

evolved_phases = thermo.phase_diagram(concepts)

# Observe which concepts moved between phases
```

## Integration with SWM

The thermodynamic module enhances SWM by:

1. **Quantifying Conceptual Tension**: Semantic pressure provides a metric for internal contradictions
2. **Modeling Transformation**: Constructive collapse explains how new understanding emerges
3. **Energy Metaphors**: Energy transfer models influence and information flow
4. **Dynamic Evolution**: Phase transitions show how knowledge systems evolve

## Advanced Usage

### Custom Pressure Thresholds

```python
# Create system with custom threshold
thermo = create_thermodynamic_system(pressure_threshold=15.0)

# Lower thresholds = more sensitive to contradictions
# Higher thresholds = more resistant to collapse
```

### Monitoring Phase Transitions

```python
# Track transitions over time
transitions = thermo.phase_transitions

for transition in transitions:
    print(f"Time: {transition['timestamp']}")
    print(f"Geoid: {transition['geoid_gid']}")
    print(f"Type: {transition['transition_type']}")
    print(f"Pressure at transition: {transition['pressure']}")
```

### Void Utilization

```python
# Access created voids
for void in thermo.voids:
    print(f"Origin: {void.origin_gid}")
    print(f"Potential energy: {void.potential_energy}")
    
    # Use void properties to guide new concept formation
    if void.dimensions.get('coherence', 0) > 0.5:
        # Void is ready for structured emergence
        pass
```

## Best Practices

1. **Set Appropriate Thresholds**: Adjust pressure thresholds based on domain
2. **Monitor Pressure Buildup**: Track pressure to anticipate collapses
3. **Utilize Voids**: Use void properties to guide new concept development
4. **Consider Context**: Equilibrium depends on surrounding geoids
5. **Track Energy Flows**: Energy transfer reveals influence patterns

## Examples

See the example scripts for detailed demonstrations:
- `examples/thermodynamics_demo.py` - Basic thermodynamic concepts
- `examples/advanced_thermodynamics.py` - Complex scenarios and paradox resolution

## Future Directions

The thermodynamic framework opens possibilities for:
- Predictive models of conceptual evolution
- Optimization of learning sequences
- Automated paradox resolution
- Knowledge system stability analysis
- Conceptual "engineering" using thermodynamic principles