# EchoForm Runtime Parameters

## Core Configuration

The EchoForm system uses the following runtime parameters:

### `extra_domains`
- **Type**: List of strings
- **Default**: `[]` (empty list)
- **Description**: Additional domains beyond the core three (scar, law, echo)
- **Usage**: Currently unused, reserved for future domain extensions

### `topology_backend`
- **Type**: String
- **Default**: `"json"`
- **Description**: Backend storage format for topology data
- **Options**: 
  - `"json"` - JSON blob storage (current implementation)
  - Future: `"graph"`, `"neo4j"`, etc.

### `trace_signature`
- **Type**: String (algorithm specification)
- **Default**: `"sha256(anchor+prev_sig)"`
- **Description**: Algorithm for computing trace signatures
- **Implementation**: SHA256 hash of anchor + previous signature, truncated to 16 chars

## Time-Decay Parameters

### `TIME_DECAY_TAU`
- **Type**: Float (seconds)
- **Default**: `1209600` (14 days)
- **Description**: Time constant for exponential decay weighting
- **Formula**: `intensity * exp(-Δt / τ)`
- **Location**: `src/kimera/echoform.py`

## Implementation Notes

- Parameters are currently hardcoded constants
- Future versions may support runtime configuration via environment variables
- Time-decay can be disabled by setting `apply_time_decay=False` in `intensity_sum()`

## Version History

- **v0.7.1**: Initial parameter documentation
- **v0.7.2**: Added time-decay weighting with τ = 14 days
- **v0.7.3**: CLS lattice integration with cls_event tracking