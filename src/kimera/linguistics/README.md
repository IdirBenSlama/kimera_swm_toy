# Kimera Linguistics Module

The linguistics module provides translation and multi-language analysis capabilities for the Spherical Word Methodology (SWM) implementation.

## Features

### Translation Service Abstraction
- **Unified Interface**: Common API for different translation backends
- **Multiple Backends**: Support for Google Translate, Hugging Face, and mock services
- **Automatic Caching**: Built-in caching for performance optimization
- **Batch Processing**: Efficient translation of multiple texts
- **Language Detection**: Automatic source language identification

### Advanced Caching System
- **Multi-tier Cache**: In-memory LRU cache with persistent disk storage
- **Performance Optimization**: Dramatic speedup for repeated translations
- **Cache Management**: Export/import, statistics, and cleanup utilities
- **Configurable TTL**: Customizable cache expiration times

## Quick Start

### Basic Translation

```python
from kimera.linguistics import create_translation_service

# Create a translation service
translator = create_translation_service('mock', enable_cache=True)

# Translate text
result = await translator.translate("hello", "es")
print(f"{result.source_text} -> {result.translated_text}")
# Output: hello -> hola
```

### Batch Translation

```python
# Translate multiple texts efficiently
texts = ["hello", "world", "peace"]
results = await translator.batch_translate(texts, "fr")

for text, result in zip(texts, results):
    print(f"{text} -> {result.translated_text}")
```

### Language Detection

```python
# Detect language automatically
language, confidence = await translator.detect_language("Bonjour le monde")
print(f"Detected: {language} (confidence: {confidence:.2f})")
# Output: Detected: fr (confidence: 0.90)
```

## Advanced Usage

### Custom Cache Configuration

```python
from kimera.linguistics import TranslationCache, CachedTranslationService

# Create custom cache
cache = TranslationCache(
    cache_dir=Path("./my_cache"),
    max_memory_items=5000,
    max_disk_items=50000,
    ttl_seconds=86400 * 30  # 30 days
)

# Use with translation service
base_service = create_translation_service('mock', enable_cache=False)
cached_service = CachedTranslationService(base_service)
```

### SWM Integration

```python
from kimera.geoid import Geoid
from kimera.linguistics import create_translation_service

# Translate and create geoids for multi-language analysis
translator = create_translation_service('mock')
languages = ['es', 'fr', 'de', 'ja']

geoids = {}
for lang in languages:
    result = await translator.translate("consciousness", lang)
    geoids[lang] = Geoid(
        word=result.translated_text,
        metadata={'language': lang, 'original': 'consciousness'}
    )
```

## Configuration

The module uses a YAML configuration file (`config/translation_config.yaml`) for settings:

```yaml
default_service: mock

services:
  google:
    api_key: ${GOOGLE_TRANSLATE_API_KEY}
    max_retries: 3
    timeout: 30.0
    
  huggingface:
    model_name: "Helsinki-NLP/opus-mt-en-es"
    device: "cpu"

cache:
  enabled: true
  memory:
    max_items: 10000
    ttl_seconds: 86400
  disk:
    enabled: true
    max_items: 100000
```

## API Reference

### TranslationService (Abstract Base Class)

```python
async def translate(
    text: str, 
    target_language: str,
    source_language: Optional[str] = None
) -> TranslationResult
```

Translate text to the target language.

**Parameters:**
- `text`: Text to translate
- `target_language`: Target language code (e.g., 'es', 'fr')
- `source_language`: Source language code (auto-detect if None)

**Returns:**
- `TranslationResult` object with translation details

### TranslationResult

```python
@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str
    target_language: str
    confidence: float = 1.0
    metadata: Dict[str, Any] = None
```

### TranslationCache

Advanced caching system with persistence support.

**Key Methods:**
- `get(cache_key)`: Retrieve from cache
- `put(cache_key, result)`: Store in cache
- `export_cache(path)`: Export cache to file
- `import_cache(path)`: Import cache from file
- `get_stats()`: Get cache statistics
- `clear()`: Clear all cache entries

## Performance Considerations

1. **Caching**: Always enable caching for production use
2. **Batch Processing**: Use batch translation for multiple texts
3. **Cache Warming**: Pre-populate cache with common translations
4. **TTL Settings**: Balance freshness vs. performance

## Future Enhancements

### Google Translate Integration
```python
# Coming soon
translator = create_translation_service(
    'google',
    api_key=os.getenv('GOOGLE_TRANSLATE_API_KEY')
)
```

### Hugging Face Models
```python
# Coming soon
translator = create_translation_service(
    'huggingface',
    model_name='Helsinki-NLP/opus-mt-en-es'
)
```

### Advanced NLP Features
- Dependency parsing with spaCy
- Named entity recognition
- Sentiment analysis
- Temporal pattern detection

## Examples

See the `examples/` directory for complete examples:
- `translation_demo.py`: Basic translation features
- `swm_translation_integration.py`: Integration with SWM components

## Testing

Run the test suite:

```bash
pytest tests/unit/test_translation_service.py -v
```

## Contributing

When adding new translation backends:

1. Inherit from `TranslationService` base class
2. Implement all abstract methods
3. Add configuration support
4. Include comprehensive tests
5. Update documentation

## License

Part of the Kimera SWM project. See main LICENSE file.