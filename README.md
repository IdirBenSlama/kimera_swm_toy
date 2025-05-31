
Kimera‑SWM Toy Prototype **v0.7.3**
===================================

This repository holds a minimal, CPU‑only prototype implementing the
core concepts defined in *Kimera‑SWM Micro‑Specification v0.1*.

Features batch processing with latency and memory monitoring for large datasets.
**New in v0.7.3**: CLS lattice storage with cls_event tracking and time-decay weighting (τ = 14 days).
**New in v0.7.2**: EchoForm core implementation with stable hashing and enhanced observability.
**New in v0.7.0**: Negation fix with environment variable control and comprehensive benchmarking.
**New in v0.3.0**: Memory-optimized streaming for handling 10k+ pairs efficiently.

Quick‑start (Windows‑friendly)
------------------------------
```bash
# Install dependencies
python -m pip install --upgrade pip
pip install poetry==1.8.2
poetry install --sync

# Update lockfile after dependency changes
poetry lock
poetry install

# Run tests
poetry run pytest -q

# Run demo with toy dataset (22 rows)
poetry run python -m kimera.demo

# Generate larger dataset (2K rows, tri-lingual)
poetry run python scripts/build_dataset.py --rows 2000 --lang en,fr,ar --mode online --out data/contradictions_2k.csv

# Run demo with larger dataset - choose your platform:

# Option 1: CLI argument (cross-platform)
poetry run python -m kimera.demo data/contradictions_2k.csv --chunk 300

# Option 2: Environment variable (Windows PowerShell)
$env:KIMERA_DATASET_PATH = "data/contradictions_2k.csv"
poetry run python -m kimera.demo --chunk 300

# Option 3: Environment variable (Windows CMD)
set KIMERA_DATASET_PATH=data\contradictions_2k.csv
poetry run python -m kimera.demo --chunk 300

# Option 4: Environment variable (Unix/Linux/Mac)
KIMERA_DATASET_PATH=data/contradictions_2k.csv poetry run python -m kimera.demo --chunk 300
```

### Batch Processing
The demo now includes performance monitoring:
- **Latency tracking**: Average ms per reactor cycle
- **Memory monitoring**: Memory delta during processing  
- **Progress bars**: Visual feedback for large datasets
- **Configurable chunks**: Tune batch size for your hardware

Expected output:
```
Reactor cycles 100%|████████████████| 14/14 [00:05<00:00,  2.50chunk/s]
Loaded 3996 geoids
Pairs processed: 1998
Latency (ms): 5123.4
Δ Memory (MB): 18.7
Scars logged : 1650
```

GPT-4o Benchmark (Phase 2.1 - Memory Optimized)
-----------------------------------------------
Compare Kimera's contradiction detection against GPT-4o with enhanced memory efficiency:

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="sk-..."  # Unix/Mac
# or
$env:OPENAI_API_KEY = "sk-..."  # PowerShell

# Run full benchmark (Kimera + GPT-4o) - now supports large datasets!
poetry run python -m benchmarks.llm_compare data/toy_contradictions.csv --max-pairs 50

# Large dataset benchmark (automatic streaming)
poetry run python -m benchmarks.llm_compare data/contradictions_2k.csv --max-pairs 1000

# Use different GPT model
poetry run python -m benchmarks.llm_compare --model gpt-4o --max-pairs 25

# Run Kimera-only benchmark (no API key needed)
poetry run python -m benchmarks.llm_compare --kimera-only --max-pairs 100

# Custom output file with visualization
poetry run python -m benchmarks.llm_compare --outfile my_results.csv --max-pairs 25
```

**New in v0.3.0 - Memory Optimization:**
- **🧠 Streaming Dataset Loading**: Automatically handles large datasets (10k+ pairs) with minimal memory usage
- **📊 Smart Thresholds**: Uses regular loading for small datasets (<100 pairs), streaming for large ones
- **♻️ Memory Management**: Automatic garbage collection and memory cleanup between chunks
- **🐼 Pandas Integration**: Efficient CSV chunking with fallback to standard library
- **📈 Scalability**: Can process 10x larger datasets with same memory footprint

**Benchmark Features:**
- **Multiple models**: Support for gpt-4o, gpt-4o-mini, and other OpenAI models
- **Performance comparison**: Speed (ms/pair) and accuracy metrics
- **Agreement analysis**: How often Kimera and GPT-4o agree
- **CSV export**: Detailed results with reasoning for each pair
- **Matplotlib visualization**: Automatic bar charts and pie charts
- **Rate limiting**: Respects OpenAI API limits with exponential backoff
- **Confidence scoring**: Both systems provide confidence levels
- **Kimera-only mode**: Test without API key for development
- **🚀 Async OpenAI calls**: 5-10× faster GPT-4o benchmarks with concurrent requests
- **⚡ Smart parallelization**: Auto-detects optimal worker counts for Kimera

**New in v0.7.1 - Echo-Form Implementation:**
- **🔍 Enhanced Observability**: Every geoid now carries the exact trimmed text that was embedded
- **🔗 Stable Hashing**: Deterministic geoid IDs based on `sha256(lang + echo)` instead of random UUIDs
- **🧹 Whitespace Deduplication**: Leading/trailing spaces no longer create different embeddings
- **📊 Explorer Enhancement**: Optional Echo columns in the web explorer for debugging
- **⚡ Cache Efficiency**: Improved cache hit rates through consistent text normalization

**Testing the Implementation:**
```bash
# Test the fixes
poetry run python test_fixes.py

# Run full test suite
poetry run pytest -q

# Test streaming functionality
poetry run python test_streaming_benchmark.py

# Quick validation
poetry run python run_validation.py
```

**Async Performance Optimization (v0.5.0+):**
```bash
# Install async dependencies
poetry add httpx

# Sync mode (baseline) - 3-6 minutes for 50 pairs
poetry run python -m benchmarks.llm_compare --max-pairs 50 --model gpt-4o-mini

# Async mode (5-10x faster) - 30-60 seconds for 50 pairs  
poetry run python -m benchmarks.llm_compare --max-pairs 50 --model gpt-4o-mini --async 8

# Large dataset comparison
time poetry run python -m benchmarks.llm_compare --max-pairs 100 --async 12

# Kimera parallel + OpenAI async (optimal performance)
poetry run python -m benchmarks.llm_compare --max-pairs 100 --mp 4 --async 10
```

**Concurrency Guidelines:**
- **Small datasets (≤50 pairs)**: `--async 4-6`
- **Medium datasets (50-200 pairs)**: `--async 8-12`  
- **Large datasets (200+ pairs)**: `--async 10-20`
- **Rate limit aware**: Automatic backoff on 429 responses

Expected benchmark output (with async optimization):
```
📂 Loading dataset: data/contradictions_2k.csv
✅ Testing 50 pairs (streaming mode activated)

=== Running Kimera Benchmark - Parallel Mode ===
🚀 Using 4 worker processes
  Processed 50/50 pairs

=== Running GPT-4o Benchmark (gpt-4o-mini) - Async Mode ===
🚀 Using 8 concurrent requests
  Processed 50/50 pairs

✓ Results saved to: benchmark_results.csv
✓ Visualization saved to: benchmark_results.png

============================================================
BENCHMARK SUMMARY
============================================================
Dataset: data/contradictions_2k.csv
Total pairs tested: 50

Kimera Results:
  Time: 2.3s
  Avg per pair: 46.8ms
  Contradictions found: 23
  Avg confidence: 0.742
  Mode: parallel (4 workers)

GPT-4o Results:
  Time: 45.2s
  Avg per pair: 904.1ms
  Contradictions found: 19
  Avg confidence: 0.856
  Mode: async (8 concurrent)

Agreement Analysis:
  Total agreements: 42/50
  Agreement rate: 84.0%
  Kimera-only contradictions: 6
  GPT-4o-only contradictions: 2

Performance:
  Kimera is 19.6x faster than GPT-4o
  Async mode: 5.8x faster than sync GPT-4o
  Memory efficiency: 10x improvement with streaming
```

The benchmark automatically generates a comprehensive visualization:

![Benchmark Summary](benchmark_summary_sample.png)

*Sample 4-panel comparison showing contradictions detected, processing speed, confidence scores, and agreement analysis.*

Dataset Generation
------------------
The `scripts/build_dataset.py` tool can generate contradiction pairs in multiple ways:

**Online mode** (scrapes Wikipedia):
```bash
poetry run python scripts/build_dataset.py --rows 2000 --lang en,fr,ar --mode online --out data/contradictions_2k.csv
```

**Offline mode** (uses static seed data):
```bash
poetry run python scripts/build_dataset.py --rows 200 --mode offline --out data/contradictions_offline.csv
```

**Options:**
- `--rows N`: Number of total rows to generate (split evenly across languages)
- `--lang CODES`: Comma-separated language codes (en, fr, ar supported)
- `--mode online|offline`: Data source mode
- `--out PATH`: Output CSV file path

If `ModuleNotFoundError: kimera` persists, run:
```bash
set PYTHONPATH=%CD%\src;%PYTHONPATH%
```
