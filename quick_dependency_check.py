#!/usr/bin/env python3
"""
Quick dependency check to identify missing packages.
"""

import sys
import importlib

def check_dependency(name, module_name=None):
    """Check if a dependency can be imported."""
    if module_name is None:
        module_name = name
    
    try:
        importlib.import_module(module_name)
        print(f"✓ {name}")
        return True
    except ImportError as e:
        print(f"✗ {name}: {e}")
        return False

def main():
    print("Checking dependencies...")
    print("=" * 40)
    
    dependencies = [
        ("pandas", "pandas"),
        ("matplotlib", "matplotlib.pyplot"),
        ("numpy", "numpy"),
        ("scikit-learn", "sklearn"),
        ("sentence-transformers", "sentence_transformers"),
        ("pytest", "pytest"),
        ("pytest-asyncio", "pytest_asyncio"),
        ("requests", "requests"),
        ("psutil", "psutil"),
        ("tqdm", "tqdm"),
        ("openai", "openai"),
        ("httpx", "httpx"),
        ("joblib", "joblib"),
        ("pyyaml", "yaml"),
    ]
    
    passed = 0
    total = len(dependencies)
    
    for name, module in dependencies:
        if check_dependency(name, module):
            passed += 1
    
    print("=" * 40)
    print(f"Dependencies: {passed}/{total} available")
    
    if passed < total:
        print("\nMissing dependencies detected!")
        print("Run: poetry install")
        return 1
    else:
        print("\nAll dependencies available!")
        return 0

if __name__ == "__main__":
    sys.exit(main())