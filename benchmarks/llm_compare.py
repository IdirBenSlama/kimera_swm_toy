"""
GPT-4o vs Kimera Reactor Benchmark (Phase 1.3)
===============================================

Compares contradiction detection between:
- Kimera reactor (embedding-based resonance)
- GPT-4o (LLM-based reasoning)

Usage:
    python -m benchmarks.llm_compare [dataset.csv] [--api-key KEY] [--output results.csv]
"""

# ---- Begin emoji-safe logging -------------------------------------------
import os, sys
USE_EMOJI = "--no-emoji" not in sys.argv
if not USE_EMOJI:               # strip the flag so argparse ignores it
    sys.argv.remove("--no-emoji")

def log(txt):                   # emoji-aware print helper
    print(txt if USE_EMOJI else txt.encode('ascii', 'ignore').decode())
# ---- End emoji-safe logging ---------------------------------------------

import csv
import json
import time
import asyncio
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Iterator
import gc

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from kimera.dataset import load_toy_dataset
from kimera.geoid import Geoid, init_geoid
from kimera.resonance import resonance, THRESH

# Import async OpenAI client
try:
    from benchmarks.openai_async import run_async_benchmark
    ASYNC_AVAILABLE = True
except ImportError:
    try:
        from .openai_async import run_async_benchmark
        ASYNC_AVAILABLE = True
    except ImportError:
        ASYNC_AVAILABLE = False


def stream_dataset_pairs(dataset_path: Path, max_pairs: int, chunk_size: int = 1000) -> Iterator[List[Tuple[str, str]]]:
    """
    Stream dataset pairs in chunks to reduce memory usage.
    
    Args:
        dataset_path: Path to CSV dataset
        max_pairs: Maximum number of pairs to generate
        chunk_size: Number of geoids to load per chunk
    
    Yields:
        List of (text1, text2) pairs from each chunk
    """
    pairs_generated = 0
    
    try:
        # Try pandas for efficient chunked reading
        import pandas as pd
        
        for chunk_df in pd.read_csv(dataset_path, chunksize=chunk_size):
            if pairs_generated >= max_pairs:
                break
                
            # Convert chunk to geoids
            chunk_geoids = []
            for _, row in chunk_df.iterrows():
                if 'text' in row and pd.notna(row['text']):
                    geoid = init_geoid(
                        raw=str(row['text']),
                        lang=row.get('lang', 'en'),
                        tags=["benchmark"]
                    )
                    chunk_geoids.append(geoid)
            
            # Create pairs from this chunk
            chunk_pairs = create_test_pairs(chunk_geoids, min(max_pairs - pairs_generated, len(chunk_geoids) // 2))
            
            if chunk_pairs:
                pairs_generated += len(chunk_pairs)
                yield chunk_pairs
                
            # Force garbage collection after each chunk
            del chunk_geoids, chunk_df
            gc.collect()
            
    except ImportError:
        # Fallback to standard CSV reader
        log("⚠️  Pandas not available, using standard CSV reader (slower for large files)")
        
        with open(dataset_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            chunk_geoids = []
            for i, row in enumerate(reader):
                if pairs_generated >= max_pairs:
                    break
                    
                if 'text' in row and row['text'].strip():
                    geoid = init_geoid(
                        raw=row['text'],
                        lang=row.get('lang', 'en'),
                        tags=["benchmark"]
                    )
                    chunk_geoids.append(geoid)
                
                # Process chunk when it reaches chunk_size
                if len(chunk_geoids) >= chunk_size:
                    chunk_pairs = create_test_pairs(chunk_geoids, min(max_pairs - pairs_generated, len(chunk_geoids) // 2))
                    if chunk_pairs:
                        pairs_generated += len(chunk_pairs)
                        yield chunk_pairs
                    
                    chunk_geoids.clear()
                    gc.collect()
            
            # Process remaining geoids
            if chunk_geoids and pairs_generated < max_pairs:
                chunk_pairs = create_test_pairs(chunk_geoids, min(max_pairs - pairs_generated, len(chunk_geoids) // 2))
                if chunk_pairs:
                    yield chunk_pairs


def load_dataset_efficiently(dataset_path: Path, max_pairs: int) -> List[Tuple[str, str]]:
    """
    Load dataset pairs efficiently using streaming for large datasets.
    
    Args:
        dataset_path: Path to CSV dataset
        max_pairs: Maximum number of pairs to load
    
    Returns:
        List of (text1, text2) pairs
    """
    # For small datasets, use the original method
    if max_pairs <= 100:
        geoids = load_toy_dataset(dataset_path)
        return create_test_pairs(geoids, max_pairs)
    
    # For larger datasets, use streaming
    log(f"📊 Using streaming loader for {max_pairs} pairs (memory efficient)")
    
    all_pairs = []
    chunk_size = min(1000, max_pairs * 4)  # Load 4x pairs worth of geoids per chunk
    
    for chunk_pairs in stream_dataset_pairs(dataset_path, max_pairs, chunk_size):
        all_pairs.extend(chunk_pairs)
        print(f"  Loaded {len(all_pairs)}/{max_pairs} pairs...")
        
        if len(all_pairs) >= max_pairs:
            break
    
    return all_pairs[:max_pairs]

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class GPT4oBenchmark:
    """GPT-4o API client for contradiction detection with retry logic."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        if not OPENAI_AVAILABLE:
            raise ImportError("Install openai: pip install openai")
            
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY env var or pass --api-key")
        
        self.model = model
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def detect_contradiction(self, text1: str, text2: str, max_retries: int = 3) -> Tuple[bool, float, str]:
        """
        Returns (is_contradiction, confidence, reasoning) with exponential backoff retry.
        """
        prompt = f"""Analyze these two statements for logical contradiction:

Statement A: "{text1}"
Statement B: "{text2}"

Question: Do these statements contradict each other?

Respond with JSON only:
{{
    "contradiction": true/false,
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation"
}}"""
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=200,
                    timeout=30
                )
                
                content = response.choices[0].message.content.strip()
                
                # Try to extract JSON from response
                if content.startswith("```json"):
                    content = content.split("```json")[1].split("```")[0].strip()
                elif content.startswith("```"):
                    content = content.split("```")[1].split("```")[0].strip()
                
                result = json.loads(content)
                return (
                    bool(result["contradiction"]),
                    float(result["confidence"]),
                    str(result["reasoning"])
                )
                
            except json.JSONDecodeError as e:
                if attempt == max_retries - 1:
                    return False, 0.0, f"JSON Parse Error: {str(e)}"
                time.sleep(2 ** attempt)  # Exponential backoff
                
            except Exception as e:
                if attempt == max_retries - 1:
                    return False, 0.0, f"API Error: {str(e)}"
                time.sleep(2 ** attempt)  # Exponential backoff
        
        return False, 0.0, "Max retries exceeded"


class KimeraBenchmark:
    """Kimera reactor benchmark wrapper."""
    
    @staticmethod
    def detect_contradiction(text1: str, text2: str) -> Tuple[bool, float, str]:
        """
        Returns (is_contradiction, confidence, reasoning)
        """
        # Create geoids for the texts
        geoid1 = init_geoid(text1, "en", ["benchmark"], raw=text1)
        geoid2 = init_geoid(text2, "en", ["benchmark"], raw=text2)
        
        resonance_score = resonance(geoid1, geoid2)
        is_contradiction = bool(resonance_score < THRESH)  # Cast numpy.bool_ to bool
        confidence = 1.0 - resonance_score if is_contradiction else resonance_score
        reasoning = f"Resonance: {resonance_score:.3f}, Threshold: {THRESH}"
        
        return is_contradiction, confidence, reasoning


def create_test_pairs(geoids: List[Geoid], max_pairs: int = 50) -> List[Tuple[str, str]]:
    """Create test pairs from geoids, mixing contradictory and non-contradictory."""
    import random
    
    pairs = []
    random.shuffle(geoids)
    
    # Take pairs sequentially (should include some contradictions from dataset)
    for i in range(0, min(len(geoids) - 1, max_pairs * 2), 2):
        pairs.append((geoids[i].raw, geoids[i + 1].raw))
    
    return pairs[:max_pairs]


def run_benchmark(dataset_path: Path, api_key: Optional[str] = None, model: str = "gpt-4o-mini", 
                 max_pairs: int = 50, kimera_only: bool = False, mp_workers: int = 0,
                 async_concurrent: int = 0) -> Dict:
    """Run full benchmark comparison."""
    
    log(f"📂 Loading dataset: {dataset_path}")
    
    # Use efficient loading for large datasets
    test_pairs = load_dataset_efficiently(dataset_path, max_pairs)
    log(f"✅ Testing {len(test_pairs)} pairs")
    
    # Initialize benchmarks
    kimera = KimeraBenchmark()
    gpt4o = None
    
    if not kimera_only:
        if not OPENAI_AVAILABLE:
            log("⚠️  OpenAI not available. Running Kimera-only mode.")
            kimera_only = True
        elif not api_key:
            log("⚠️  No API key provided. Running Kimera-only mode.")
            kimera_only = True
        else:
            try:
                gpt4o = GPT4oBenchmark(api_key, model)
                print(f"✓ GPT-4o benchmark initialized (model: {model})")
            except Exception as err:
                log(f"⚠️  GPT-4o initialization failed: {err}")
                print("Running Kimera-only mode.")
                kimera_only = True
    
    results = {
        "dataset": str(dataset_path),
        "model": model,
        "total_pairs": len(test_pairs),
        "kimera_only": kimera_only,
        "kimera_results": [],
        "gpt4o_results": [],
        "kimera_stats": {},
        "gpt4o_stats": {},
        "agreement_stats": {}
    }
    
    print("\n=== Running Kimera Benchmark ===")
    if mp_workers > 0:
        print(f"🚀 Multiprocessing enabled with {mp_workers} workers")
        print("   (Note: MP optimization applies to batch reactor processing,")
        print("    not individual pair comparisons in this benchmark)")
    kimera_start = time.perf_counter()
    
    for i, (text1, text2) in enumerate(test_pairs):
        is_contra, conf, reason = kimera.detect_contradiction(text1, text2)
        results["kimera_results"].append({
            "pair_id": i,
            "text1": text1,
            "text2": text2,
            "contradiction": is_contra,
            "confidence": conf,
            "reasoning": reason
        })
        if (i + 1) % 10 == 0:
            print(f"  Processed {i + 1}/{len(test_pairs)} pairs")
    
    kimera_time = time.perf_counter() - kimera_start
    results["kimera_stats"] = {
        "total_time_s": round(kimera_time, 2),
        "avg_time_per_pair_ms": round((kimera_time / len(test_pairs)) * 1000, 2),
        "contradictions_found": sum(1 for r in results["kimera_results"] if r["contradiction"]),
        "avg_confidence": round(sum(r["confidence"] for r in results["kimera_results"]) / len(test_pairs), 3)
    }
    
    if gpt4o and not kimera_only:
        # Choose sync or async mode based on flags
        if async_concurrent > 0 and ASYNC_AVAILABLE:
            print(f"\n=== Running GPT-4o Benchmark ({model}) - Async Mode ===")
            print(f"🚀 Using {async_concurrent} concurrent requests")
            
            # Run async benchmark
            async_results = asyncio.run(run_async_benchmark(
                test_pairs, api_key, model, async_concurrent
            ))
            
            results["gpt4o_results"] = async_results["results"]
            results["gpt4o_stats"] = async_results["stats"]
            
        else:
            if async_concurrent > 0 and not ASYNC_AVAILABLE:
                log("⚠️  Async mode requested but httpx not available. Using sync mode.")
            
            print(f"\n=== Running GPT-4o Benchmark ({model}) - Sync Mode ===")
            gpt4o_start = time.perf_counter()
            
            for i, (text1, text2) in enumerate(test_pairs):
                is_contra, conf, reason = gpt4o.detect_contradiction(text1, text2)
                results["gpt4o_results"].append({
                    "pair_id": i,
                    "text1": text1,
                    "text2": text2,
                    "contradiction": is_contra,
                    "confidence": conf,
                    "reasoning": reason
                })
                if (i + 1) % 5 == 0:  # Less frequent updates due to API latency
                    print(f"  Processed {i + 1}/{len(test_pairs)} pairs")
                time.sleep(0.1)  # Rate limiting
            
            gpt4o_time = time.perf_counter() - gpt4o_start
            results["gpt4o_stats"] = {
                "total_time_s": round(gpt4o_time, 2),
                "avg_time_per_pair_ms": round((gpt4o_time / len(test_pairs)) * 1000, 2),
                "contradictions_found": sum(1 for r in results["gpt4o_results"] if r["contradiction"]),
                "avg_confidence": round(sum(r["confidence"] for r in results["gpt4o_results"]) / len(test_pairs), 3),
                "mode": "sync"
            }
        
        # Calculate agreement
        agreements = 0
        for kr, gr in zip(results["kimera_results"], results["gpt4o_results"]):
            if kr["contradiction"] == gr["contradiction"]:
                agreements += 1
        
        results["agreement_stats"] = {
            "total_agreements": agreements,
            "agreement_rate": round(agreements / len(test_pairs), 3),
            "kimera_only_contradictions": sum(1 for kr, gr in zip(results["kimera_results"], results["gpt4o_results"]) 
                                            if kr["contradiction"] and not gr["contradiction"]),
            "gpt4o_only_contradictions": sum(1 for kr, gr in zip(results["kimera_results"], results["gpt4o_results"]) 
                                           if not kr["contradiction"] and gr["contradiction"])
        }
    
    return results


def save_results(results: Dict, output_path: Path):
    """Save benchmark results to CSV."""
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow([
            "pair_id", "text1", "text2",
            "kimera_contradiction", "kimera_confidence", "kimera_reasoning",
            "gpt4o_contradiction", "gpt4o_confidence", "gpt4o_reasoning",
            "agreement"
        ])
        
        # Data rows
        for i in range(len(results["kimera_results"])):
            kr = results["kimera_results"][i]
            gr = results["gpt4o_results"][i] if results["gpt4o_results"] else {}
            
            agreement = (kr["contradiction"] == gr.get("contradiction", False)) if gr else "N/A"
            
            writer.writerow([
                kr["pair_id"],
                kr["text1"][:100] + "..." if len(kr["text1"]) > 100 else kr["text1"],
                kr["text2"][:100] + "..." if len(kr["text2"]) > 100 else kr["text2"],
                kr["contradiction"],
                kr["confidence"],
                kr["reasoning"][:50] + "..." if len(kr["reasoning"]) > 50 else kr["reasoning"],
                gr.get("contradiction", "N/A"),
                gr.get("confidence", "N/A"),
                gr.get("reasoning", "N/A")[:50] + "..." if gr.get("reasoning") and len(gr["reasoning"]) > 50 else gr.get("reasoning", "N/A"),
                agreement
            ])


def create_metrics_csv(results: Dict, output_path: Path) -> Path:
    """Create CSV in format expected by metric_runner."""
    metrics_csv_path = output_path.with_name(output_path.stem + "_metrics.csv")
    
    with open(metrics_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Header for metrics analysis
        header = ["pair_id", "text1", "text2", "label", "kimera_conf"]
        if not results["kimera_only"] and results["gpt4o_results"]:
            header.append("gpt_conf")
        writer.writerow(header)
        
        # Data rows - we need to create ground truth labels
        # For now, we'll use a heuristic: if both models agree, use that as truth
        # Otherwise, mark as uncertain (this is a limitation of not having ground truth)
        for i in range(len(results["kimera_results"])):
            kr = results["kimera_results"][i]
            gr = results["gpt4o_results"][i] if results["gpt4o_results"] else None
            
            # Create a synthetic label based on agreement or high confidence
            if gr and kr["contradiction"] == gr["contradiction"]:
                # Both agree - use their consensus
                label = 1 if kr["contradiction"] else 0
            elif kr["confidence"] > 0.8:
                # High confidence Kimera prediction
                label = 1 if kr["contradiction"] else 0
            elif gr and gr["confidence"] > 0.8:
                # High confidence GPT prediction
                label = 1 if gr["contradiction"] else 0
            else:
                # Default to no contradiction for uncertain cases
                label = 0
            
            row = [
                kr["pair_id"],
                kr["text1"][:50] + "..." if len(kr["text1"]) > 50 else kr["text1"],
                kr["text2"][:50] + "..." if len(kr["text2"]) > 50 else kr["text2"],
                label,
                kr["confidence"] if kr["contradiction"] else 1.0 - kr["confidence"]
            ]
            
            if gr:
                gpt_conf = gr["confidence"] if gr["contradiction"] else 1.0 - gr["confidence"]
                row.append(gpt_conf)
            
            writer.writerow(row)
    
    return metrics_csv_path


def create_visualization(results: Dict, output_path: Path):
    """Create matplotlib bar chart comparing Kimera vs GPT-4o."""
    
    if not MATPLOTLIB_AVAILABLE:
        log("⚠️  Matplotlib not available. Skipping visualization.")
        return
    
    if results["kimera_only"]:
        log("⚠️  Kimera-only mode. Skipping comparison visualization.")
        return
    
    # Prepare data
    methods = ['Kimera', 'GPT-4o']
    contradictions = [
        results["kimera_stats"]["contradictions_found"],
        results["gpt4o_stats"]["contradictions_found"]
    ]
    avg_times = [
        results["kimera_stats"]["avg_time_per_pair_ms"],
        results["gpt4o_stats"]["avg_time_per_pair_ms"]
    ]
    avg_confidence = [
        results["kimera_stats"]["avg_confidence"],
        results["gpt4o_stats"]["avg_confidence"]
    ]
    
    # Create subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Kimera vs GPT-4o Benchmark Comparison', fontsize=16, fontweight='bold')
    
    # Contradictions found
    bars1 = ax1.bar(methods, contradictions, color=['#2E86AB', '#A23B72'])
    ax1.set_title('Contradictions Detected')
    ax1.set_ylabel('Count')
    for i, v in enumerate(contradictions):
        ax1.text(i, v + 0.1, str(v), ha='center', va='bottom')
    
    # Average time per pair
    bars2 = ax2.bar(methods, avg_times, color=['#2E86AB', '#A23B72'])
    ax2.set_title('Average Time per Pair')
    ax2.set_ylabel('Milliseconds')
    ax2.set_yscale('log')  # Log scale for time comparison
    for i, v in enumerate(avg_times):
        ax2.text(i, v * 1.1, f'{v:.1f}ms', ha='center', va='bottom')
    
    # Average confidence
    bars3 = ax3.bar(methods, avg_confidence, color=['#2E86AB', '#A23B72'])
    ax3.set_title('Average Confidence')
    ax3.set_ylabel('Confidence Score')
    ax3.set_ylim(0, 1)
    for i, v in enumerate(avg_confidence):
        ax3.text(i, v + 0.02, f'{v:.3f}', ha='center', va='bottom')
    
    # Agreement analysis
    if results["agreement_stats"]:
        agreement_data = [
            results["agreement_stats"]["total_agreements"],
            results["agreement_stats"]["kimera_only_contradictions"],
            results["agreement_stats"]["gpt4o_only_contradictions"]
        ]
        agreement_labels = ['Both Agree', 'Kimera Only', 'GPT-4o Only']
        colors = ['#F18F01', '#2E86AB', '#A23B72']
        
        ax4.pie(agreement_data, labels=agreement_labels, colors=colors, autopct='%1.1f%%')
        ax4.set_title('Agreement Analysis')
    else:
        ax4.text(0.5, 0.5, 'No comparison data', ha='center', va='center', transform=ax4.transAxes)
        ax4.set_title('Agreement Analysis')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Visualization saved to: {output_path}")


def print_summary(results: Dict):
    """Print benchmark summary."""
    
    print("\n" + "="*60)
    print("BENCHMARK SUMMARY")
    print("="*60)
    
    print(f"Dataset: {results['dataset']}")
    print(f"Total pairs tested: {results['total_pairs']}")
    
    if not results["kimera_only"]:
        print(f"Model: {results['model']}")
    
    print(f"\nKimera Results:")
    print(f"  Time: {results['kimera_stats']['total_time_s']}s")
    print(f"  Avg per pair: {results['kimera_stats']['avg_time_per_pair_ms']}ms")
    print(f"  Contradictions found: {results['kimera_stats']['contradictions_found']}")
    print(f"  Avg confidence: {results['kimera_stats']['avg_confidence']}")
    
    if not results["kimera_only"] and results["gpt4o_stats"]:
        print(f"\nGPT-4o Results:")
        print(f"  Time: {results['gpt4o_stats']['total_time_s']}s")
        print(f"  Avg per pair: {results['gpt4o_stats']['avg_time_per_pair_ms']}ms")
        print(f"  Contradictions found: {results['gpt4o_stats']['contradictions_found']}")
        print(f"  Avg confidence: {results['gpt4o_stats']['avg_confidence']}")
        
        if results["agreement_stats"]:
            print(f"\nAgreement Analysis:")
            print(f"  Total agreements: {results['agreement_stats']['total_agreements']}/{results['total_pairs']}")
            print(f"  Agreement rate: {results['agreement_stats']['agreement_rate']*100:.1f}%")
            print(f"  Kimera-only contradictions: {results['agreement_stats']['kimera_only_contradictions']}")
            print(f"  GPT-4o-only contradictions: {results['agreement_stats']['gpt4o_only_contradictions']}")
            
            # Performance comparison
            kimera_speed = results['kimera_stats']['avg_time_per_pair_ms']
            gpt4o_speed = results['gpt4o_stats']['avg_time_per_pair_ms']
            speedup = gpt4o_speed / kimera_speed
            
            print(f"\nPerformance:")
            print(f"  Kimera is {speedup:.1f}x faster than GPT-4o")
    else:
        print(f"\nPerformance:")
        print(f"  Ready for GPT-4o comparison with API key!")
    
    print("="*60)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Benchmark Kimera vs GPT-4o contradiction detection")
    parser.add_argument("dataset", nargs="?", 
                       default="data/toy_contradictions.csv",
                       help="Path to CSV dataset")
    parser.add_argument("--api-key", help="OpenAI API key (or set OPENAI_API_KEY env var)")
    parser.add_argument("--model", default="gpt-4o-mini",
                       help="OpenAI model to use (default: gpt-4o-mini)")
    parser.add_argument("--outfile", default="benchmark_results.csv", 
                       help="Output CSV file")
    parser.add_argument("--max-pairs", type=int, default=50,
                       help="Maximum number of pairs to test")
    parser.add_argument("--kimera-only", action="store_true",
                       help="Run only Kimera benchmark (skip GPT-4o)")
    parser.add_argument("--no-viz", action="store_true",
                       help="Skip matplotlib visualization")
    parser.add_argument("--mp", type=int, default=0,
                       help="Use multiprocessing with N workers for Kimera (0=off)")
    parser.add_argument("--async", type=int, default=0, dest="async_concurrent",
                       help="Use async OpenAI calls with N concurrent requests (0=sync)")
    parser.add_argument("--no-cache", action="store_true",
                       help="Disable embedding cache for Kimera")
    parser.add_argument("--stats", action="store_true",
                       help="Generate comprehensive metrics and plots after benchmark")
    
    args = parser.parse_args()
    
    # Handle cache disabling for Kimera
    if args.no_cache:
        os.environ["KIMERA_CACHE_DIR"] = "_nocache_benchmark"
    
    # Validate dataset path
    dataset_path = Path(args.dataset)
    if not dataset_path.exists():
        log(f"❌ Dataset not found: {dataset_path}")
        print("Available datasets:")
        data_dir = Path("data")
        if data_dir.exists():
            for csv_file in data_dir.glob("*.csv"):
                print(f"  - {csv_file}")
        return 1
    
    try:
        # Run benchmark
        results = run_benchmark(
            dataset_path=dataset_path,
            api_key=args.api_key,
            model=args.model,
            max_pairs=args.max_pairs,
            kimera_only=args.kimera_only,
            mp_workers=args.mp,
            async_concurrent=args.async_concurrent
        )
        
        # Print summary
        print_summary(results)
        
        # Save results
        output_path = Path(args.outfile)
        save_results(results, output_path)
        print(f"\n✓ Results saved to: {output_path}")
        
        # Generate comprehensive metrics if requested
        if args.stats:
            print("\n=== Generating Comprehensive Metrics ===")
            try:
                # Convert results to CSV format expected by metric_runner
                csv_for_metrics = create_metrics_csv(results, output_path)
                
                # Import and run metric_runner
                from benchmarks.metric_runner import main as metric_main
                import sys
                
                # Temporarily modify sys.argv to pass arguments to metric_runner
                original_argv = sys.argv
                sys.argv = ["metric_runner", str(csv_for_metrics)]
                if args.outfile != "benchmark_results.csv":
                    # Use same directory as output file
                    sys.argv.extend(["--out", str(output_path.parent)])
                
                metric_main()
                sys.argv = original_argv
                
                print("✓ Comprehensive metrics generated!")
                
            except Exception as err:
                log(f"⚠️  Failed to generate metrics: {err}")
        
        # Create visualization
        if not args.no_viz and not results["kimera_only"]:
            viz_path = output_path.with_suffix('.png')
            create_visualization(results, viz_path)
        
        return 0
        
    except KeyboardInterrupt:
        log("\n❌ Benchmark interrupted by user")
        return 1
    except Exception as err:
        log(f"❌ Benchmark failed: {err}")
        return 1


if __name__ == "__main__":
    exit(main())