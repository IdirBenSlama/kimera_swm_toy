# Kimera NLP Module

Enhanced NLP pattern extraction module with spaCy integration for the Kimera project.

## Overview

The Kimera NLP module provides comprehensive pattern extraction capabilities using spaCy. It includes:

- **Basic Pattern Extraction**: Named entities, noun chunks
- **Advanced Pattern Matching**: Token-based and dependency-based patterns using spaCy's Matcher
- **Syntactic Analysis**: Extraction of noun phrases, verb phrases, and prepositional phrases
- **Semantic Analysis**: Similarity-based clustering, concept extraction, and analogies (requires medium/large models)
- **Visualization**: HTML reports and dependency/entity visualizations

## Installation

### Basic Setup (Small Model)

```bash
pip install spacy
python -m spacy download en_core_web_sm
```

### Full Setup (With Semantic Features)

```bash
pip install spacy scikit-learn
python -m spacy download en_core_web_md  # Medium model with word vectors
# or
python -m spacy download en_core_web_lg  # Large model for better accuracy
```

## Quick Start

### Basic Usage

```python
from kimera.nlp import extract_patterns

text = "Apple Inc. is planning to invest $1 billion in AI research."
patterns = extract_patterns(text)

print(patterns)
# Output: {'entities': [...], 'noun_chunks': [...]}
```

### Advanced Pattern Extraction

```python
from kimera.nlp import PatternExtractor

extractor = PatternExtractor()
text = "The CEO announced that the company will expand globally."

# Extract all patterns
patterns = extractor.extract_all_patterns(text)

# Access specific pattern types
token_patterns = patterns["token_patterns"]
syntactic_patterns = patterns["syntactic_patterns"]
semantic_roles = patterns["semantic_roles"]
```

### Comprehensive Analysis

```python
from kimera.nlp import extract_comprehensive_patterns

text = "Machine learning algorithms process complex data patterns."

# Extract all available patterns
patterns = extract_comprehensive_patterns(
    text, 
    include_semantic=True,  # Requires medium/large model
    semantic_model="en_core_web_md"
)
```

## Module Structure

```
kimera/nlp/
├── __init__.py          # Main module interface
├── patterns.py          # Advanced pattern matching with Matcher
├── similarity.py        # Semantic similarity and clustering
├── visualization.py     # Pattern visualization utilities
├── example.py          # Demonstration scripts
├── test_nlp.py         # Test suite
└── README.md           # This file
```

## Features

### 1. Basic Pattern Extraction

Extract named entities and noun chunks:

```python
from kimera.nlp import extract_patterns

# Extract all entities and noun chunks
patterns = extract_patterns("Google develops AI systems.")

# Extract specific entity types
patterns = extract_patterns(
    "Tim Cook is the CEO of Apple.", 
    patterns=["PERSON", "ORG"]
)
```

### 2. Advanced Pattern Matching

Use spaCy's Matcher for custom patterns:

```python
from kimera.nlp import PatternExtractor

extractor = PatternExtractor()

# Add custom token pattern
extractor.add_token_pattern(
    "TECH_TERM",
    [{"LOWER": {"IN": ["ai", "ml", "nlp"]}}, {"POS": "NOUN"}],
    "Technology terms"
)

# Extract patterns
patterns = extractor.extract_token_patterns("AI technology is advancing.")
```

### 3. Dependency Patterns

Extract grammatical relationships:

```python
# Extract subject-verb-object patterns
extractor = PatternExtractor()
dep_patterns = extractor.extract_dependency_patterns(
    "Scientists discovered new methods."
)
```

### 4. Semantic Analysis (Requires Medium/Large Model)

```python
from kimera.nlp import SemanticPatternExtractor

semantic_extractor = SemanticPatternExtractor("en_core_web_md")

# Find similar phrases
similar = semantic_extractor.find_similar_phrases(
    text="The company develops innovative products.",
    target_phrase="creates new technology",
    threshold=0.7
)

# Extract semantic clusters
clusters = semantic_extractor.extract_semantic_clusters(
    "AI and machine learning are related to data science."
)

# Find analogies
analogies = semantic_extractor.find_analogies(
    text="The king ruled the kingdom wisely.",
    pattern=("man", "king", "woman")  # man:king :: woman:?
)
```

### 5. Visualization

Generate HTML reports and visualizations:

```python
from kimera.nlp import PatternVisualizer, PatternExtractor

visualizer = PatternVisualizer()
extractor = PatternExtractor()

text = "The AI system processes natural language efficiently."

# Extract patterns
patterns = extractor.extract_all_patterns(text)

# Generate HTML report
visualizer.generate_pattern_report(
    text, 
    patterns, 
    output_path="analysis_report.html"
)

# Visualize dependencies
dep_html = visualizer.visualize_dependencies(
    text, 
    output_path="dependencies.html"
)

# Export patterns as JSON
visualizer.export_patterns_json(patterns, "patterns.json")
```

## API Reference

### Main Functions

- `extract_patterns(text, patterns=None)`: Basic pattern extraction
- `extract_comprehensive_patterns(text, include_semantic=False)`: All-in-one extraction
- `ensure_spacy_model(model_name)`: Ensure a spaCy model is loaded

### Classes

#### PatternExtractor
- `add_token_pattern(name, pattern, description)`: Add custom token patterns
- `add_dependency_pattern(name, pattern, description)`: Add dependency patterns
- `extract_token_patterns(text)`: Extract token-based patterns
- `extract_dependency_patterns(text)`: Extract dependency patterns
- `extract_syntactic_patterns(text)`: Extract syntactic structures
- `extract_semantic_roles(text)`: Extract semantic roles
- `extract_all_patterns(text)`: Extract all pattern types

#### SemanticPatternExtractor
- `find_similar_phrases(text, target_phrase, threshold)`: Find semantically similar phrases
- `extract_semantic_clusters(text, n_clusters, min_similarity)`: Group similar phrases
- `find_analogies(text, pattern)`: Find analogical patterns
- `extract_concept_patterns(text, concept_seeds)`: Extract concept-related terms

#### PatternVisualizer
- `visualize_dependencies(text, output_path, style)`: Visualize dependency tree
- `visualize_entities(text, output_path)`: Visualize named entities
- `generate_pattern_report(text, patterns, output_path)`: Generate comprehensive report
- `export_patterns_json(patterns, output_path)`: Export patterns to JSON
- `generate_pattern_statistics(patterns)`: Generate pattern statistics

## Examples

### Running the Examples

```bash
# Run the example demonstrations
python -m kimera.nlp.example

# Run the test suite
python src/kimera/nlp/test_nlp.py
```

### Integration with Kimera

The NLP module can be integrated with other Kimera components:

```python
from kimera.nlp import extract_comprehensive_patterns
from kimera.resonance import Resonance

# Extract patterns from text
text = "Quantum computing will revolutionize cryptography."
patterns = extract_comprehensive_patterns(text)

# Use patterns with Kimera's resonance system
resonance = Resonance()
# ... integrate pattern data with resonance calculations
```

## Performance Considerations

1. **Model Selection**:
   - `en_core_web_sm`: Fast, no word vectors, basic features only
   - `en_core_web_md`: Balanced, includes word vectors, supports semantic features
   - `en_core_web_lg`: Most accurate, largest word vectors, slowest

2. **Batch Processing**: For multiple texts, process in batches:
   ```python
   texts = ["Text 1", "Text 2", "Text 3"]
   docs = list(nlp.pipe(texts))
   ```

3. **Disable Unused Components**: For faster processing:
   ```python
   nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
   ```

## Troubleshooting

### Model Not Found Error
```bash
# Install the required model
python -m spacy download en_core_web_sm
```

### No Word Vectors Error
```bash
# Install a model with vectors
python -m spacy download en_core_web_md
```

### Memory Issues with Large Texts
```python
# Process in chunks
nlp.max_length = 1000000  # Increase max length
# Or process in smaller chunks
```

## Future Enhancements

- [ ] Custom entity recognition training
- [ ] Multi-language support
- [ ] Integration with transformer models
- [ ] Real-time pattern streaming
- [ ] Pattern caching and optimization
- [ ] Advanced visualization options

## Contributing

When adding new pattern extraction features:

1. Add the implementation to the appropriate module
2. Update the `__init__.py` exports
3. Add tests to `test_nlp.py`
4. Update this README with examples
5. Ensure backward compatibility

## License

Part of the Kimera project. See main project license.