# Enhanced Benchmark System Features

## Overview
The Kimera benchmark system has been significantly enhanced to provide comprehensive comparison capabilities between Kimera and GPT-4o for contradiction detection tasks.

## New Features Added

### 1. **Multiple Model Support**
- Support for different OpenAI models (gpt-4o, gpt-4o-mini, gpt-3.5-turbo)
- Configurable via `--model` parameter
- Default: gpt-4o-mini (cost-effective)

### 2. **Enhanced CLI Interface**
```bash
# New command line options
--model MODEL          # Choose OpenAI model
--outfile FILE         # Custom output filename  
--no-viz               # Skip visualization generation
--kimera-only          # Run without API key
```

### 3. **Matplotlib Visualizations**
- Automatic generation of comparison charts
- 4-panel visualization:
  - Contradictions detected (bar chart)
  - Average processing time (log scale bar chart)
  - Average confidence scores (bar chart)
  - Agreement analysis (pie chart)
- High-resolution PNG output
- Graceful fallback if matplotlib unavailable

### 4. **Improved Error Handling**
- Exponential backoff for API rate limits
- Graceful handling of API failures
- Better error messages and user feedback
- Robust CSV parsing with fallback

### 5. **Enhanced Statistics**
- Detailed performance metrics
- Agreement rate analysis
- Speed comparison (Kimera vs GPT-4o)
- Confidence score analysis
- Per-model breakdown

### 6. **Better User Experience**
- Progress indicators with emoji
- Colored output for better readability
- Comprehensive help messages
- Dataset validation and suggestions
- Automatic file path resolution

## Usage Examples

### Basic Comparison
```bash
poetry run python -m benchmarks.llm_compare data/toy_contradictions.csv --max-pairs 25
```

### Development Mode (No API Key)
```bash
poetry run python -m benchmarks.llm_compare --kimera-only --max-pairs 100
```

### Custom Model and Output
```bash
poetry run python -m benchmarks.llm_compare --model gpt-4o --outfile results.csv --max-pairs 50
```

### Skip Visualization
```bash
poetry run python -m benchmarks.llm_compare --no-viz --max-pairs 25
```

## Output Files

### CSV Results
- Detailed per-pair results
- Both model outputs with reasoning
- Agreement analysis
- Truncated text for readability

### PNG Visualization
- Professional-quality charts
- Side-by-side comparison
- Performance and accuracy metrics
- Agreement breakdown

## Technical Improvements

### Code Quality
- Type hints throughout
- Comprehensive error handling
- Modular function design
- Clean separation of concerns

### Performance
- Efficient batch processing
- Rate limit compliance
- Memory-efficient CSV handling
- Progress tracking

### Reliability
- Robust API error handling
- Fallback mechanisms
- Input validation
- Graceful degradation

## Dependencies Added
- `matplotlib ^3.7` for visualizations
- Enhanced `openai ^1.0` integration
- Better CSV handling

## Testing
- Updated test suite
- Quick test script included
- CLI argument validation
- Error condition testing

This enhanced benchmark system provides a professional-grade tool for evaluating and comparing contradiction detection systems.