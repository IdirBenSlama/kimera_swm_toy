#!/usr/bin/env python3
"""
Test the new metrics infrastructure with actual data.
This will run Kimera-only first, then show how to add GPT comparison safely.
"""
import sys
import os
from pathlib import Path
import tempfile

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_kimera_only_metrics():
    """Test metrics with Kimera-only benchmark."""
    print("🧪 Testing Kimera-SWM v0.7.0 Metrics with Real Data")
    print("=" * 60)
    print("⚠️  Running Kimera-only mode (no API key needed)")
    print()
    
    try:
        # Check if we have test data
        data_files = [
            "data/toy_contradictions.csv",
            "data/contradictions_2k.csv",
            "/c:/Users/bensl/Downloads/kimera_swm_toy/data/toy_contradictions.csv"
        ]
        
        dataset_path = None
        for path in data_files:
            if Path(path).exists():
                dataset_path = Path(path)
                break
        
        if not dataset_path:
            print("📝 Creating synthetic test dataset...")
            dataset_path = create_test_dataset()
        
        print(f"📂 Using dataset: {dataset_path}")
        
        # Import benchmark
        sys.path.insert(0, str(Path(__file__).parent / "benchmarks"))
        from llm_compare import run_benchmark, create_metrics_csv, save_results
        
        # Run Kimera-only benchmark
        print("\n🚀 Running Kimera benchmark...")
        results = run_benchmark(
            dataset_path=dataset_path,
            api_key=None,  # No API key = Kimera-only mode
            model="gpt-4o-mini",
            max_pairs=20,  # Small test
            kimera_only=True,
            mp_workers=0,
            async_concurrent=0
        )
        
        print(f"✅ Benchmark completed: {len(results['kimera_results'])} pairs processed")
        
        # Save results and create metrics CSV
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            output_path = temp_path / "test_results.csv"
            
            save_results(results, output_path)
            metrics_csv = create_metrics_csv(results, output_path)
            
            print(f"✅ Results saved to: {output_path}")
            print(f"✅ Metrics CSV created: {metrics_csv}")
            
            # Test metric runner
            print("\n📊 Running comprehensive metrics analysis...")
            
            from benchmarks.metric_runner import main as metric_main
            import sys
            
            # Temporarily modify sys.argv
            original_argv = sys.argv
            sys.argv = ["metric_runner", str(metrics_csv), "--out", str(temp_path)]
            
            try:
                metric_main()
                print("✅ Metrics analysis completed!")
                
                # Check generated files
                yaml_file = temp_path / "metrics.yaml"
                plot_file = temp_path / "metrics_plots.png"
                report_file = temp_path / "summary_report.md"
                
                if yaml_file.exists():
                    print(f"✅ Metrics YAML generated: {yaml_file}")
                    # Show a snippet
                    with open(yaml_file) as f:
                        content = f.read()
                        print("\n📄 Metrics snippet:")
                        print(content[:300] + "..." if len(content) > 300 else content)
                
                if plot_file.exists():
                    print(f"✅ Plots generated: {plot_file}")
                
                if report_file.exists():
                    print(f"✅ Summary report generated: {report_file}")
                
            finally:
                sys.argv = original_argv
        
        print("\n" + "=" * 60)
        print("🎉 Metrics infrastructure test PASSED!")
        print("\nNext steps for full GPT comparison:")
        print("1. Revoke the API key you shared (security risk!)")
        print("2. Generate a new OpenAI API key")
        print("3. Set it as environment variable:")
        print("   export OPENAI_API_KEY='your-new-key-here'")
        print("4. Run with GPT comparison:")
        print("   poetry run python -m benchmarks.llm_compare data/toy_contradictions.csv --stats")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_test_dataset():
    """Create a small test dataset if none exists."""
    import pandas as pd
    
    # Create contradictory pairs
    data = [
        {"text": "The sky is blue", "lang": "en", "source": "test"},
        {"text": "The sky is red", "lang": "en", "source": "test"},
        {"text": "Water boils at 100°C", "lang": "en", "source": "test"},
        {"text": "Water boils at 50°C", "lang": "en", "source": "test"},
        {"text": "Paris is in France", "lang": "en", "source": "test"},
        {"text": "Paris is in Germany", "lang": "en", "source": "test"},
        {"text": "Dogs are mammals", "lang": "en", "source": "test"},
        {"text": "Cats are mammals", "lang": "en", "source": "test"},
        {"text": "The sun is hot", "lang": "en", "source": "test"},
        {"text": "Fire is hot", "lang": "en", "source": "test"},
    ]
    
    df = pd.DataFrame(data)
    
    # Ensure data directory exists
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    dataset_path = data_dir / "test_contradictions.csv"
    df.to_csv(dataset_path, index=False)
    
    return dataset_path

def show_api_key_security_warning():
    """Show important security information."""
    print("\n" + "🔒" * 60)
    print("SECURITY WARNING")
    print("🔒" * 60)
    print("You shared an API key in plain text. This is a security risk!")
    print()
    print("IMMEDIATE ACTIONS REQUIRED:")
    print("1. Go to https://platform.openai.com/api-keys")
    print("2. Find the key starting with 'sk-or-v1-a54f091e...'")
    print("3. Click 'Revoke' to disable it immediately")
    print("4. Generate a new API key")
    print("5. Store it securely as an environment variable")
    print()
    print("SECURE USAGE:")
    print("# On Windows:")
    print("set OPENAI_API_KEY=your-new-key-here")
    print()
    print("# On Linux/Mac:")
    print("export OPENAI_API_KEY='your-new-key-here'")
    print()
    print("# Then run benchmarks:")
    print("poetry run python -m benchmarks.llm_compare data/toy_contradictions.csv --stats")
    print("🔒" * 60)

if __name__ == "__main__":
    show_api_key_security_warning()
    success = test_kimera_only_metrics()
    sys.exit(0 if success else 1)