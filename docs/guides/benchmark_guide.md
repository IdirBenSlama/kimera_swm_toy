# Kimera Benchmark Guide

## Overview
The Kimera benchmark system provides comprehensive comparison capabilities between Kimera and GPT-4o for contradiction detection tasks.

## Features

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

## Running Benchmarks

### Basic Usage
```bash
python benchmarks/llm_compare.py --dataset data/mixed_quick.csv --mode kimera_only
```

### With OpenAI Comparison
```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-key-here"

# Run comparison
python benchmarks/llm_compare.py --dataset data/mixed_5k.csv --model gpt-4o-mini
```

### Custom Output
```bash
python benchmarks/llm_compare.py \
  --dataset data/contradictions_2k.csv \
  --model gpt-4o \
  --outfile my_benchmark_results.csv \
  --no-viz
```

## Installation Requirements

Add the benchmark dependencies to your environment:

```bash
pip install .[benchmarks]
```

Or install manually:
```bash
pip install matplotlib pandas duckdb
```

## Metrics Computed

The benchmark system computes:

- **ROC AUC**: Area under the ROC curve
- **PR AUC**: Area under the Precision-Recall curve  
- **Accuracy**: Overall classification accuracy
- **Precision/Recall**: For contradiction detection
- **Processing Time**: Average time per sample
- **Confidence Scores**: Model confidence in predictions

## Output Format

Results are saved as CSV with columns:
- `model`: Model name (kimera, gpt-4o, etc.)
- `contradictions_detected`: Number of contradictions found
- `avg_processing_time`: Average time per sample (seconds)
- `avg_confidence`: Average confidence score
- `accuracy`: Classification accuracy
- `precision`: Precision for contradiction detection
- `recall`: Recall for contradiction detection
- `roc_auc`: ROC AUC score
- `pr_auc`: PR AUC score

## Visualization

When matplotlib is available, the benchmark automatically generates:

1. **Detection Comparison**: Bar chart showing contradictions detected by each model
2. **Performance Timing**: Log-scale comparison of processing times
3. **Confidence Analysis**: Average confidence scores across models
4. **Agreement Matrix**: How often models agree on classifications

## Best Practices

1. **Use appropriate datasets**: Start with `mixed_quick.csv` for testing
2. **Monitor API costs**: Use `gpt-4o-mini` for cost-effective comparisons
3. **Run multiple iterations**: Results can vary, especially for smaller datasets
4. **Check agreement rates**: High disagreement may indicate dataset issues
5. **Save results**: Always specify `--outfile` for important benchmarks

## Troubleshooting

### Common Issues

**Missing API Key**:
```bash
export OPENAI_API_KEY="your-key-here"
```

**Matplotlib Not Available**:
```bash
pip install matplotlib
# Or run with --no-viz
```

**Dataset Not Found**:
```bash
# Check available datasets
ls data/
# Use full path if needed
python benchmarks/llm_compare.py --dataset /full/path/to/data.csv
```

**Memory Issues with Large Datasets**:
- Use smaller datasets for testing
- Consider chunking large datasets
- Monitor system memory usage