# Kimera SWM - Spherical Word Methodology Implementation

A Python implementation of the Spherical Word Methodology (SWM) for finding deep structural similarities and hidden connections across different domains of knowledge.

## What is Kimera?

Kimera is a knowledge analysis system that implements SWM principles to:
- **Find Resonance**: Discover deep structural similarities between concepts across different domains
- **Extract Patterns**: Identify functional, structural, dynamic, and relational patterns in text
- **Detect Contradictions**: Identify logical incompatibilities between statements
- **Generate Insights**: Find creative solutions by discovering analogies across domains

## Key Features

### 🔍 Resonance Detection
Find hidden connections between seemingly unrelated concepts:
```python
from kimera.api import Kimera

kimera = Kimera()
result = kimera.find_resonance(
    "The heart pumps blood through the body",
    "The router directs data through the network"
)
print(f"Resonance: {result['score']:.3f}")  # 0.7+ indicates strong similarity
```

### 🧩 Pattern Extraction
Extract four types of patterns aligned with SWM:
- **Functional**: What does it do? (actions, purposes)
- **Structural**: How is it organized? (components, hierarchy)
- **Dynamic**: How does it change? (processes, flows)
- **Relational**: How does it connect? (dependencies, similarities)

```python
patterns = kimera.extract_patterns("Information flows through the network")
# Returns functional and dynamic patterns
```

### ⚡ Contradiction Detection
Identify logical contradictions (separate from resonance):
```python
result = kimera.detect_contradiction(
    "The Earth is round",
    "The Earth is flat"
)
print(f"Contradiction: {result['is_contradiction']}")  # True
```

### 💡 Cross-Domain Insights
Discover insights by finding resonances across domains:
```python
insights = kimera.find_cross_domain_insights(
    "How to improve traffic flow",
    ["Blood flows through arteries", "Data flows through networks", ...]
)
```

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/kimera_swm_toy.git
cd kimera_swm_toy

# Install dependencies
pip install -r requirements.txt

# Optional: Install spaCy for advanced pattern extraction
pip install spacy
python -m spacy download en_core_web_sm
```

## Quick Start

```python
from kimera.api import Kimera

# Initialize Kimera
kimera = Kimera()

# Find resonance between concepts
result = kimera.find_resonance(
    "Plants grow towards sunlight",
    "Companies grow towards profit"
)
print(f"Resonance: {result['score']:.3f}")
print(f"Interpretation: {result['interpretation']}")

# Extract patterns
patterns = kimera.extract_patterns("The CEO leads the organization")
for p in patterns:
    print(f"Found {p['type']} pattern: {p.get('action', p.get('organization'))}")

# Detect contradictions
contra = kimera.detect_contradiction(
    "Fire is hot",
    "Fire is cold"
)
print(f"Is contradiction: {contra['is_contradiction']}")
```

## Architecture

Kimera implements a modular architecture aligned with SWM principles:

```
kimera/
├── geoid.py          # Knowledge unit representation
├── resonance.py      # Basic semantic resonance
├── enhanced_resonance.py  # Pattern-based resonance
├── advanced_patterns.py   # Four SWM pattern types
├── contradiction.py  # Logical contradiction detection
└── api.py           # Unified API interface
```

## Benchmarks

Run benchmarks to test Kimera's performance:

```bash
# Test resonance detection
python benchmarks/resonance_benchmark.py

# Test contradiction detection
python benchmarks/llm_compare.py --kimera-only

# Compare with GPT-4o (requires API key)
python benchmarks/llm_compare.py --api-key YOUR_KEY
```

## Examples

Explore Kimera's capabilities:

```bash
# Basic resonance demo
python examples/resonance_demo.py

# Advanced pattern extraction
python examples/advanced_resonance_demo.py

# Simple API usage
python examples/simple_api_demo.py
```

## Performance

- **Speed**: 700-1500x faster than GPT-4o for pattern analysis
- **Accuracy**: 
  - Resonance detection: Optimized for cross-domain similarity
  - Contradiction detection: 70% agreement with GPT-4o
  - Pattern extraction: Covers all four SWM pattern types

## Use Cases

1. **Innovation & Problem Solving**: Find analogies from nature or other domains
2. **Knowledge Discovery**: Identify hidden connections in research
3. **Creative Writing**: Discover unexpected metaphors and connections
4. **Education**: Help students understand concepts through analogies
5. **System Design**: Learn from patterns in other domains

## Development Roadmap

### ✅ Completed
- Basic resonance detection
- Pattern extraction (functional, structural, dynamic, relational)
- Contradiction detection module
- Unified API
- Comprehensive examples

### 🚧 In Progress
- Multi-language support (SWM "1+3+1" rule)
- Advanced pattern matching algorithms
- Web interface

### 📋 Planned
- Full Geoid implementation (all SWM dimensions)
- Dynamic knowledge evolution (scars, drift, voids)
- Kimera Kernel cognitive architecture
- Real-world application showcases

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests.

## Citation

If you use Kimera in your research, please cite:
```
@software{kimera2024,
  title = {Kimera: A Spherical Word Methodology Implementation},
  year = {2024},
  url = {https://github.com/yourusername/kimera_swm_toy}
}
```

## License

MIT License - see LICENSE file for details.

## Acknowledgments

Based on the Spherical Word Methodology (SWM) framework, which emphasizes finding deep structural patterns and connections across different domains of knowledge.