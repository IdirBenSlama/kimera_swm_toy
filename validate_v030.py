#!/usr/bin/env python3
"""Quick validation script for v0.3.0 benchmark system."""

import subprocess
import sys
from pathlib import Path

def test_import():
    """Test that benchmark module imports correctly."""
    try:
        import benchmarks.llm_compare
        print("✅ Benchmark module imports successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_help():
    """Test CLI help message."""
    try:
        result = subprocess.run([
            sys.executable, "-m", "benchmarks.llm_compare", "--help"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and "Benchmark Kimera vs GPT-4o" in result.stdout:
            print("✅ CLI help works correctly")
            return True
        else:
            print(f"❌ CLI help failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False

def test_kimera_only():
    """Test Kimera-only mode with minimal data."""
    try:
        result = subprocess.run([
            sys.executable, "-m", "benchmarks.llm_compare",
            "--kimera-only", "--max-pairs", "3", "--no-viz"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Kimera-only benchmark runs successfully")
            return True
        elif "Dataset not found" in result.stdout:
            print("⚠️  No test dataset found (expected for fresh install)")
            return True
        else:
            print(f"❌ Kimera-only test failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Kimera-only test failed: {e}")
        return False

def test_streaming_functionality():
    """Test that streaming dataset loading works."""
    try:
        # Import the streaming functions
        from benchmarks.llm_compare import stream_dataset_pairs, load_dataset_efficiently
        
        # Create a minimal test dataset
        import tempfile
        import csv
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'lang', 'text', 'label_contradict_id'])
            writer.writerow([1, 'en', 'The sky is blue', ''])
            writer.writerow([2, 'en', 'The sky is red', ''])
            writer.writerow([3, 'en', 'Water is wet', ''])
            writer.writerow([4, 'en', 'Fire is cold', ''])
            test_path = Path(f.name)
        
        try:
            # Test streaming functionality
            pairs = load_dataset_efficiently(test_path, 2)
            
            if len(pairs) == 2 and isinstance(pairs[0][0], str):
                print("✅ Streaming dataset loading works")
                return True
            else:
                print(f"❌ Streaming test failed: got {len(pairs)} pairs")
                return False
        finally:
            test_path.unlink(missing_ok=True)
            
    except Exception as e:
        print(f"❌ Streaming test failed: {e}")
        return False

def check_dependencies():
    """Check if key dependencies are available."""
    deps = {
        "matplotlib": "Visualization support",
        "openai": "GPT-4o comparison", 
        "pandas": "Efficient CSV streaming",
        "tqdm": "Progress bars",
        "kimera": "Core functionality"
    }
    
    all_good = True
    for dep, desc in deps.items():
        try:
            __import__(dep)
            print(f"✅ {dep}: {desc}")
        except ImportError:
            print(f"❌ {dep}: Missing - {desc}")
            all_good = False
    
    return all_good


if __name__ == "__main__":
    print("🧪 Validating Kimera v0.3.0 Benchmark System\n")
    
    tests = [
        ("Dependencies", check_dependencies),
        ("Module Import", test_import),
        ("CLI Help", test_help),
        ("Streaming Functionality", test_streaming_functionality),
        ("Kimera-Only Mode", test_kimera_only)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n--- {name} ---")
        results.append(test_func())
    
    print(f"\n{'='*50}")
    if all(results):
        print("🎉 All validation tests passed!")
        print("✨ v0.3.0 benchmark system is ready for use")
    else:
        print("⚠️  Some validation tests failed")
        print("📋 Check the output above for specific issues")
    
    print(f"{'='*50}")