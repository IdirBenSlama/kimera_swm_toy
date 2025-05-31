#!/usr/bin/env python3
"""
Validate that the setup is working correctly
"""
import sys
import os
from pathlib import Path

def validate_setup():
    """Validate the research loop setup"""
    print("🔍 Validating Research Loop Setup")
    print("=" * 40)
    
    # Check Python path
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    
    # Check current directory
    cwd = Path.cwd()
    print(f"Current directory: {cwd}")
    
    # Check key files exist
    key_files = [
        "src/kimera/__init__.py",
        "src/kimera/resonance.py", 
        "src/kimera/geoid.py",
        "benchmarks/llm_compare.py",
        "data/mixed_quick.csv",
        "compare_results.py",
        "tools/explorer.html"
    ]
    
    print("\n📁 File Check:")
    all_good = True
    for file_path in key_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")
            all_good = False
    
    # Check imports
    print("\n📦 Import Check:")
    sys.path.insert(0, 'src')
    
    try:
        import kimera
        print("  ✅ kimera")
    except Exception as e:
        print(f"  ❌ kimera: {e}")
        all_good = False
    
    try:
        from kimera.geoid import init_geoid
        print("  ✅ kimera.geoid.init_geoid")
    except Exception as e:
        print(f"  ❌ kimera.geoid.init_geoid: {e}")
        all_good = False
    
    try:
        from kimera.resonance import resonance, ENABLE_NEGATION_FIX
        print(f"  ✅ kimera.resonance (negation fix: {ENABLE_NEGATION_FIX})")
    except Exception as e:
        print(f"  ❌ kimera.resonance: {e}")
        all_good = False
    
    # Test basic functionality
    print("\n🧪 Basic Function Test:")
    try:
        g1 = init_geoid(text="Test text 1", lang="en", tags=["test"])
        g2 = init_geoid(text="Test text 2", lang="en", tags=["test"])
        score = resonance(g1, g2)
        print(f"  ✅ Basic resonance: {score:.3f}")
    except Exception as e:
        print(f"  ❌ Basic resonance: {e}")
        all_good = False
    
    # Check data
    print("\n📊 Data Check:")
    data_file = "data/mixed_quick.csv"
    if Path(data_file).exists():
        with open(data_file, 'r') as f:
            lines = f.readlines()
        print(f"  ✅ {data_file}: {len(lines)-1} data rows")
    else:
        print(f"  ❌ {data_file}: not found")
        all_good = False
    
    # Final status
    print(f"\n{'='*40}")
    if all_good:
        print("🎉 Setup validation PASSED!")
        print("Ready to run experiments!")
    else:
        print("❌ Setup validation FAILED!")
        print("Please fix the issues above before running experiments.")
    
    return all_good

if __name__ == "__main__":
    validate_setup()