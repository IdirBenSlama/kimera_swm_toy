# Kimera SWM - Experimental Semantic Analysis System

**⚠️ IMPORTANT**: This is an experimental research prototype. Previous documentation contained unverified performance claims that have been removed. See [HONEST_README.md](docs/HONEST_README.md) for verified capabilities.

## What Kimera Actually Does

Kimera is an experimental system for analyzing semantic relationships between texts using geometric representations. It provides:

- **Semantic Similarity**: Measures how related two texts are (verified working)
- **Contradiction Detection**: Identifies opposing statements (use v2_fixed version)
- **Pattern Analysis**: Groups texts by relationships (experimental)
- **Spectral Analysis**: Mathematical analysis of text collections (small scale only)

## Verified Capabilities

✅ **Working Features**:
- Resonance calculation distinguishes similar (0.79) from different (0.07) texts
- Fixed contradiction detection achieves 90% accuracy on basic tests
- Spectral analysis works for collections < 100 texts
- Thermodynamic phase classification (after complete redesign)

❌ **Not Working**:
- Original contradiction.py (fails basic tests - use contradiction_v2_fixed.py)
- Original thermodynamics.py (produces only one phase - use thermodynamics_v3.py)
- Large-scale processing (memory/performance issues)

## Actual Performance

Based on empirical measurements:
- **Speed**: ~3,000 text pairs/second for similarity calculation
- **Memory**: ~1.5 MB per 1,000 texts (1.5 GB for 1M texts)
- **Scaling**: O(n²) for pairwise operations
- **Accuracy**: Varies by task, no comprehensive benchmarks exist

**Note**: Claims of "Efficient resonance calculation (~3,000 pairs/second)

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/kimera_swm_toy.git
cd kimera_swm_toy

# Install with poetry (recommended)
pip install poetry
poetry install

# Or with pip
pip install -r requirements.txt
```

## Quick Start (Using Working Components)

```python
from kimera.geoid import init_geoid
from kimera.resonance import resonance
from kimera.contradiction_v2_fixed import analyze_contradiction

# Create semantic representations
g1 = init_geoid("The sky is blue")
g2 = init_geoid("The sky is red")

# Measure similarity (working)
similarity = resonance(g1, g2)
print(f"Similarity: {similarity:.3f}")  # ~0.67

# Detect contradiction (use fixed version)
analysis = analyze_contradiction(g1, g2)
print(f"Contradiction: {analysis.is_contradiction}")  # True
print(f"Type: {analysis.contradiction_type}")  # "antonym"
```

## Important Migration Notes

If you have existing code, you must migrate from broken to working components:

```python
# ❌ OLD (broken)
from kimera.contradiction import detect_contradiction
from kimera.thermodynamics import ThermodynamicSystem

# ✅ NEW (working)
from kimera.contradiction_v2_fixed import analyze_contradiction
from kimera.thermodynamics_v3 import ThermodynamicSystemV3
```

See [MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md) for details.

## Limitations

- **Memory Intensive**: ~1.5 GB per million texts (not 12 MB as previously claimed)
- **Quadratic Scaling**: O(n²) for pairwise operations (not O(n log n))
- **No GPU Support**: CPU only
- **Limited Scale**: Spectral analysis practical only for n < 100
- **No Benchmarks**: No comparison with standard NLP systems

## Examples

Working examples:
```bash
# Test contradiction detection (fixed version)
python experiments/test_contradiction_fixed.py

# Test thermodynamics (v3)
python experiments/test_thermodynamics_v3.py

# Run honest benchmarks
python benchmarks/honest_benchmark.py
```

## Development Status

This is experimental research software. Many theoretical claims remain unproven:
- "Semantic manifolds" - mathematical metaphor, not proven theory
- "Thermodynamic pressure" - visualization technique, not physical quantity
- "Scar networks" - conceptual idea, limited implementation

## Contributing

We welcome contributions that:
- Fix broken components
- Add proper benchmarks
- Improve actual performance
- Document real capabilities

Please do not submit:
- Unverified performance claims
- Theoretical assertions without proof
- Marketing hype

## Citation

If you use Kimera in research, please note its experimental status:
```
@software{kimera_swm,
  title = {Kimera SWM: Experimental Semantic Analysis System},
  year = {2024},
  note = {Experimental research prototype with limited validation}
}
```

## License

MIT License - see LICENSE file

## Disclaimer

Previous versions of this documentation contained unverified performance claims. This version reflects actual measured capabilities. Always validate results independently for your use case.

For the original (unverified) claims, see the git history. For verified capabilities, see [benchmarks/honest_benchmark.py](benchmarks/honest_benchmark.py).