# ADR-001: Unified Identity Model (Geoids ⇆ Scars Convergence)

**Status:** DRAFT  
**Date:** 2024-12-19  
**Authors:** Development Team  

## Context

Currently, Kimera has two separate identity models:

1. **Geoids** (`src/kimera/geoid.py`): Rich semantic objects with embeddings, language axis, context layers, and VDR scores
2. **Scars** (`src/kimera/scar.py`): Lightweight relationship markers between geoid pairs with weights and timestamps

This dual-identity system creates several issues:
- **Code duplication**: Similar identity logic scattered across modules
- **Storage complexity**: Different persistence patterns for geoids vs scars
- **Analytics gaps**: Cross-form resonance analysis requires joining disparate data structures
- **Entropy calculation**: No unified way to compute information density across identity types

## Decision

We will **merge Geoids and Scars into a single `Identity` model** that:

1. **Unifies core identity fields** from both models
2. **Maintains backward compatibility** during transition
3. **Enables unified storage** in the existing `LatticeStorage` system
4. **Supports entropy-based analytics** across all identity types

### Unified Identity Schema

```python
@dataclass
class Identity:
    """Unified identity model replacing Geoids and Scars"""
    # Core identification
    id: str                          # Replaces gid (geoids) and scar_id (scars)
    identity_type: str               # "geoid", "scar", or "hybrid"
    
    # Content & semantics (from Geoids)
    raw: Optional[str] = None        # Original text content
    echo: Optional[str] = None       # Trimmed text for hashing/embedding
    lang_axis: str = "en"           # Language classification
    tags: List[str] = field(default_factory=list)  # Replaces context_layers
    
    # Vectors & scoring (from Geoids)
    sem_vec: Optional[np.ndarray] = None
    sym_vec: Optional[np.ndarray] = None
    vdr: float = 0.0
    
    # Relationships (from Scars)
    related_ids: List[str] = field(default_factory=list)  # Connected identities
    weight: float = 1.0              # Relationship strength
    
    # Metadata
    meta: Dict[str, Any] = field(default_factory=dict)  # Extensible metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
```

### Migration Strategy

| Current → Unified | Mapping |
|-------------------|---------|
| `Geoid.gid` → `Identity.id` | Direct copy |
| `Geoid.context_layers` → `Identity.tags` | Rename field |
| `Geoid.scars` → `Identity.related_ids` | Flatten scar references |
| `Scar.scar_id` → `Identity.id` | Direct copy |
| `Scar.gid_pair` → `Identity.related_ids` | Expand tuple to list |
| `Scar.weight` → `Identity.weight` | Direct copy |

## Consequences

### Positive
- **Simplified codebase**: Single identity model reduces complexity
- **Unified storage**: All identities use same `LatticeStorage` tables
- **Enhanced analytics**: Cross-form entropy and resonance calculations
- **Future-proof**: Extensible `meta` field supports new identity types

### Negative
- **Migration effort**: Existing data needs conversion
- **Temporary complexity**: Dual-path support during transition
- **Breaking changes**: Some API signatures will change

### Risks & Mitigations
- **Data loss during migration**: Mitigated by comprehensive backup and rollback procedures
- **Performance regression**: Mitigated by maintaining existing indexes and adding new ones for unified queries
- **API compatibility**: Mitigated by providing adapter functions for legacy code

## Implementation Plan

### Phase 1: Foundation (Week 1)
- [ ] Create `src/kimera/identity.py` with unified `Identity` dataclass
- [ ] Add migration utilities in `scripts/migrate_identity.py`
- [ ] Update storage schema to support unified identity table

### Phase 2: Storage Integration (Week 2)
- [ ] Extend `LatticeStorage` with identity-specific methods
- [ ] Add `scar_id` column to existing `echoforms` table
- [ ] Implement backward-compatible fetch/store methods

### Phase 3: Code Migration (Week 3)
- [ ] Update `cls.py` lattice functions to use `Identity`
- [ ] Refactor cache layers (embedding/resonance) for unified keys
- [ ] Update reactor & benchmarks to handle `Identity` objects

### Phase 4: Entropy Integration (Week 4)
- [ ] Add `entropy()` method to `Identity` class
- [ ] Implement adaptive τ based on identity entropy
- [ ] Create DuckDB UDF for entropy-based queries

## Acceptance Criteria

- [ ] All existing tests pass with unified identity model
- [ ] Migration script successfully converts sample data without loss
- [ ] Performance benchmarks show <10% regression
- [ ] New entropy-based analytics queries work correctly
- [ ] Legacy API compatibility maintained through adapters

## References

- [Kimera Storage Implementation](../../src/kimera/storage.py)
- [Current Geoid Model](../../src/kimera/geoid.py)
- [Current Scar Model](../../src/kimera/scar.py)
- [EchoForm Integration](../../src/kimera/echoform.py)