# Phase 2 Implementation Plan: Core SWM Components

## Overview
Following the successful P0 fixes, we're ready to implement core SWM features according to the main roadmap (Phase 2: Prototype Development & Testing, Months 7-12).

## Current State vs SWM Vision

### What We Have ✅
- Basic semantic similarity detection (resonance)
- Simple pattern extraction (4 types)
- Storage system with Identity/Scar concepts
- Basic contradiction detection
- Performance benchmarking

### What SWM Requires ❌
- **Multi-dimensional Geoids** with 8 key dimensions
- **"1+3+1" linguistic rule** implementation
- **Deep pattern abstraction** beyond simple extraction
- **Cross-domain resonance** based on structural patterns
- **Symbolic/Chaos layer** for creative insights
- **Dynamic knowledge evolution** (scars, drift, voids)

## Implementation Phases

### Phase 2.1: Enhanced Geoid Implementation (Week 1-2)

#### Objective
Transform the current simple Identity model into full multi-dimensional Geoids as specified in SWM.

#### Tasks
1. **Extend Identity/Geoid Model**
   ```python
   class Geoid:
       dimensions = {
           'linguistic': {},      # Multi-language representations
           'cultural': {},        # Cultural contexts and values
           'metaphorical': {},    # Underlying metaphors/symbols
           'structural': {},      # Abstracted patterns
           'historical': {},      # Evolution over time
           'contextual': {},      # Variability across domains
           'sensory': {},         # Non-linguistic representations
           'emotional': {}        # Affective associations
       }
   ```

2. **Implement Dimension Extractors**
   - `linguistic_extractor.py` - Multi-language analysis
   - `cultural_extractor.py` - Cultural context detection
   - `metaphor_extractor.py` - Metaphor identification
   - `historical_extractor.py` - Temporal evolution tracking

3. **Create Geoid Factory**
   ```python
   def create_full_geoid(text, languages=['en', 'es', 'zh', 'ar'], 
                        extract_all_dimensions=True):
       """Create a fully-realized SWM Geoid"""
   ```

### Phase 2.2: "1+3+1" Linguistic Rule (Week 2-3)

#### Objective
Implement Idir Ben Slama's linguistic heuristic for deep multi-perspective analysis.

#### Tasks
1. **Language Selection Algorithm**
   ```python
   def select_analysis_languages(root_language, concept_domain):
       """Select 3 unrelated languages based on linguistic distance"""
       # Use language family trees
       # Maximize conceptual diversity
   ```

2. **Multi-Language Pattern Extraction**
   - Integrate translation APIs (with caching)
   - Extract patterns from each language
   - Identify unique insights per language

3. **Symbolic Layer (+1)**
   - Symbol database creation
   - Chaos pattern recognition
   - Paradox/contradiction handling

### Phase 2.3: Pattern Abstraction Engine (Week 3-4)

#### Objective
Move beyond simple pattern extraction to deep abstraction as per SWM methodology.

#### Tasks
1. **Formalized Pattern Templates**
   ```python
   class FunctionalPattern:
       attributes = {
           'purpose': str,
           'inputs': List[str],
           'outputs': List[str],
           'constraints': List[str],
           'goal': str
       }
   
   class StructuralPattern:
       attributes = {
           'components': List[str],
           'organization': str,  # hierarchical, network, etc.
           'relationships': Dict[str, str],
           'boundaries': str
       }
   ```

2. **Pattern Elicitation Protocols**
   - Question-based extraction
   - Multi-perspective analysis
   - Pattern validation criteria

3. **Pattern Storage & Indexing**
   - Extend storage for pattern data
   - Create pattern similarity metrics
   - Build pattern search capabilities

### Phase 2.4: Enhanced Resonance System (Week 4-5)

#### Objective
Implement true SWM resonance based on deep pattern matching, not just semantic similarity.

#### Tasks
1. **Pattern-Based Resonance**
   ```python
   def calculate_pattern_resonance(geoid1, geoid2):
       """Compare abstracted patterns, not surface content"""
       functional_match = compare_functional_patterns()
       structural_match = compare_structural_patterns()
       dynamic_match = compare_dynamic_patterns()
       relational_match = compare_relational_patterns()
       return weighted_resonance_score()
   ```

2. **Cross-Domain Detection**
   - Domain taxonomy system
   - Domain distance metrics
   - Novelty scoring for distant connections

3. **Resonance Visualization**
   - Network graphs of connections
   - Pattern overlap visualization
   - Resonance strength indicators

### Phase 2.5: Dynamic Knowledge Evolution (Week 5-6)

#### Objective
Implement SWM's dynamic aspects: memory scarring, conceptual drift, and constructive collapse.

#### Tasks
1. **Memory Scarring System**
   ```python
   def apply_memory_scar(geoid, experience):
       """Permanently modify geoid based on interaction"""
       geoid.scars.append({
           'timestamp': now(),
           'experience': experience,
           'structural_change': calculate_deformation()
       })
   ```

2. **Conceptual Drift Tracking**
   - Version control for geoids
   - Drift metrics and visualization
   - Drift-aware resonance calculation

3. **Void Formation**
   - Contradiction accumulation
   - Collapse detection algorithms
   - Void as creative space

## Success Metrics

### Technical Metrics
- [ ] 8 dimensional extractors implemented
- [ ] 4+ languages processed per geoid
- [ ] Pattern abstraction accuracy >80%
- [ ] Cross-domain resonance detection working
- [ ] Dynamic evolution tracking functional

### SWM Alignment Metrics
- [ ] Follows SWM methodology precisely
- [ ] Generates non-obvious insights
- [ ] Handles paradox/chaos gracefully
- [ ] Enables creative discovery

## Resources Needed

1. **Multi-language Support**
   - Translation API (Google Translate or similar)
   - Language analysis tools (spaCy for multiple languages)
   - Cultural context databases

2. **Pattern Analysis**
   - Advanced NLP models
   - Graph analysis libraries
   - Visualization tools

3. **Storage Enhancements**
   - Expand DuckDB schema
   - Add pattern tables
   - Implement versioning

## First Week Deliverables

1. **Enhanced Geoid Model** with 8 dimensions
2. **Linguistic Dimension Extractor** with basic multi-language support
3. **Updated Storage Schema** for dimensional data
4. **Basic Pattern Templates** for all 4 types
5. **Design Document** for full Phase 2 architecture

## Getting Started

```bash
# Create new branch for Phase 2
git checkout -b phase-2-swm-core

# Set up development structure
mkdir -p src/kimera/dimensions
mkdir -p src/kimera/patterns
mkdir -p src/kimera/linguistics

# Begin with Geoid enhancement
python -m kimera.dimensions.geoid_v2
```

Ready to transform Kimera from a simple similarity detector into a full SWM implementation!