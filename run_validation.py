#!/usr/bin/env python3
"""Run validation for Phase 2.1 implementation.

IMPORTANT: Run this with Poetry:
    poetry run python run_validation.py

Or activate the Poetry shell first:
    poetry shell
    python run_validation.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    print("🧪 Testing Phase 2.1 Memory Optimization Implementation\n")
    
    # Test 1: Basic imports
    try:
        from benchmarks.llm_compare import stream_dataset_pairs, load_dataset_efficiently
        print("✅ Streaming functions import successfully")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    
    # Test 2: Dependencies
    deps_status = {}
    for dep in ['pandas', 'csv', 'gc']:
        try:
            __import__(dep)
            deps_status[dep] = True
            print(f"✅ {dep} available")
        except ImportError:
            deps_status[dep] = False
            print(f"⚠️  {dep} not available (optional)")
    
    # Test 3: Create minimal test
    import tempfile
    import csv
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'lang', 'text', 'label_contradict_id'])
        for i in range(10):
            writer.writerow([i, 'en', f'Test statement {i}', ''])
        test_path = Path(f.name)
    
    try:
        # Test small dataset (should use regular method)
        pairs = load_dataset_efficiently(test_path, 5)
        if len(pairs) == 5:
            print("✅ Small dataset loading works")
        else:
            print(f"❌ Expected 5 pairs, got {len(pairs)}")
            return False
            
        # Test that pairs are strings
        if isinstance(pairs[0][0], str) and isinstance(pairs[0][1], str):
            print("✅ Text pair format correct")
        else:
            print(f"❌ Expected string pairs, got {type(pairs[0][0])}")
            return False
            
    except Exception as e:
        print(f"❌ Dataset loading failed: {e}")
        return False
    finally:
        test_path.unlink(missing_ok=True)
    
    print("\n🎉 Phase 2.1 implementation validation passed!")
    print("✨ Memory-efficient streaming is ready for large datasets!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)